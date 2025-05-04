import numpy as np
import tensorflow as tf
import csv
import json

# Гиперпараметры модели
EMBED_DIM = 128    # размерность символьных эмбеддингов
LSTM_UNITS = 256   # размер скрытого состояния LSTM

# Пути файлов
DATA_FILE = "word_forms.csv"           # CSV с формами слов (lemma, Атооч, Илик, ..., Чыгыш)
MODEL_WEIGHTS_FILE = "model_weights.h5"
CHAR_MAP_FILE = "char_map.json"

# 1. Загрузка и подготовка данных
forms_data = []  # список парадигм (списков из 6 форм слова)
with open(DATA_FILE, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)  # пропустим заголовок колонок
    for row in reader:
        # Каждая строка: [lemma, Атооч, Илик, Барыш, Табыш, Жатыш, Чыгыш]
        # Берем 6 форм (пропустив lemma, т.к. обычно lemma = Атооч)
        forms = row[1:7]
        # Пропускаем неполные записи, если есть
        if len(forms) < 6 or any(len(form) == 0 for form in forms):
            continue
        forms_data.append(forms)

# Соберём множество всех уникальных символов во всех формах
char_set = set()
for forms in forms_data:
    for form in forms:
        for ch in form:
            char_set.add(ch)
# Добавим специальные символы, которых нет в обычных словах
special_tokens = ["<PAD>", "^", "$", "|"]  # паддинг, начало последовательности, конец, разделитель
for token in special_tokens:
    char_set.add(token)
# Создаем словарь символов: индекс 0 зарезервирован под PAD (masking)
# Остальные символы разложим по индексам
# Убедимся, что <PAD> будет нулевым
char_list = sorted(char_set)
# Если <PAD> в списке не первый, переместим его вручную на начало
if "<PAD>" in char_list:
    char_list.remove("<PAD>")
char_list = ["<PAD>"] + char_list  # теперь индекс 0 = <PAD>
# Создаем отображения символ -> индекс и индекс -> символ
char2idx = {ch: i for i, ch in enumerate(char_list)}
idx2char = {i: ch for i, ch in enumerate(char_list)}
vocab_size = len(char2idx)

# Функция для кодирования строки в список индексов
def text_to_seq(text):
    return [char2idx[ch] if ch in char2idx else char2idx["<PAD>"] for ch in text]

# Подготавливаем обучающие примеры.
encoder_input_sequences = []
decoder_input_sequences = []
decoder_target_sequences = []

# Разделим данные на train/val по словам (чтобы все формы слова попали в одну выборку).
np.random.seed(42)
num_words = len(forms_data)
indices = np.arange(num_words)
np.random.shuffle(indices)
val_count = int(0.1 * num_words)
val_word_indices = set(indices[:val_count])
# Итерация по словам и их формам
for i, forms in enumerate(forms_data):
    # Конкатенируем 6 форм через разделитель и добавляем символ конца
    full_output = "|".join(forms) + "$"
    # Преобразуем в индексы выходную последовательность (для цели) и для декодера (со сдвигом)
    full_output_indices = text_to_seq(full_output)
    # Последовательность декодера (вход): символ начала + вся выходная последовательность без последнего символа
    decoder_input = "^" + "|".join(forms)  # без символа конца
    decoder_input_indices = text_to_seq(decoder_input)
    # Проверка длины: decoder_input и target должны совпадать по длине
    # Добавляем по одному примеру для каждой из 6 возможных входных форм
    for j, form in enumerate(forms):
        # form_indices — вход энкодера
        form_indices = text_to_seq(form)
        encoder_input_sequences.append(form_indices)
        decoder_input_sequences.append(decoder_input_indices)
        decoder_target_sequences.append(full_output_indices)
# Преобразуем списки в массивы одинаковой длины, дополнив <PAD> до максимальной длины
encoder_input_sequences = tf.keras.preprocessing.sequence.pad_sequences(
    encoder_input_sequences, padding='post', value=char2idx["<PAD>"])
decoder_input_sequences = tf.keras.preprocessing.sequence.pad_sequences(
    decoder_input_sequences, padding='post', value=char2idx["<PAD>"])
decoder_target_sequences = tf.keras.preprocessing.sequence.pad_sequences(
    decoder_target_sequences, padding='post', value=char2idx["<PAD>"])

# Определяем максимальную длину последовательностей
max_encoder_seq_len = encoder_input_sequences.shape[1]
max_decoder_seq_len = decoder_input_sequences.shape[1]

# 2. Построение модели seq2seq
# Энкодер
encoder_inputs = tf.keras.Input(shape=(None,), name="encoder_input")  # последовательность произвольной длины
# Символьный embedding с mask_zero, чтобы игнорировать PAD
encoder_embed = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=EMBED_DIM, 
                                         mask_zero=True, name="char_embedding")
encoder_embed_out = encoder_embed(encoder_inputs)
# LSTM энкодера (только последний скрытый и ячейковый состояния используем)
encoder_lstm = tf.keras.layers.LSTM(LSTM_UNITS, return_state=True, name="encoder_lstm")
_, state_h, state_c = encoder_lstm(encoder_embed_out)
encoder_states = [state_h, state_c]

# Декодер
decoder_inputs = tf.keras.Input(shape=(None,), name="decoder_input")
decoder_embed_out = encoder_embed(decoder_inputs)  # используем тот же embedding слой (общие веса)
decoder_lstm = tf.keras.layers.LSTM(LSTM_UNITS, return_sequences=True, return_state=True, name="decoder_lstm")
decoder_outputs, _, _ = decoder_lstm(decoder_embed_out, initial_state=encoder_states)
# Выходной плотный слой на весь словарь символов
decoder_dense = tf.keras.layers.Dense(vocab_size, activation='softmax', name="dense_output")
output_tokens = decoder_dense(decoder_outputs)

# Полная модель для обучения
model = tf.keras.Model([encoder_inputs, decoder_inputs], output_tokens)
model.compile(optimizer=tf.keras.optimizers.Adam(), 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

# 3. Обучение модели
# Подготовка целевых выходов в формате (samples, seq_len, 1) для sparse_categorical_crossentropy
decoder_targets = np.expand_dims(decoder_target_sequences, -1)
# Обучаем, используя 10% данных как validation
model.fit([encoder_input_sequences, decoder_input_sequences], decoder_targets,
          epochs=15, batch_size=64, validation_split=0.1, verbose=2)

# 4. Сохранение модели и словаря
model.save_weights(MODEL_WEIGHTS_FILE)
with open(CHAR_MAP_FILE, "w", encoding="utf-8") as f:
    json.dump({
        "vocab_size": vocab_size,
        "embed_dim": EMBED_DIM,
        "lstm_units": LSTM_UNITS,
        "char2idx": char2idx,
        "idx2char": idx2char
    }, f, ensure_ascii=False)

print("Модель и словарь символов сохранены.")
