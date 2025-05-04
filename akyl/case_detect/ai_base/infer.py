import numpy as np
import tensorflow as tf
import json
import sys

# Пути к файлам (должны совпадать с train_model.py)
MODEL_WEIGHTS_FILE = "model_weights.h5"
CHAR_MAP_FILE = "char_map.json"

# Загрузка словаря символов и параметров модели
with open(CHAR_MAP_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)
char2idx = data["char2idx"]
idx2char = {int(k): v for k, v in data["idx2char"].items()} if isinstance(data["idx2char"], dict) else {i: ch for i, ch in enumerate(data["idx2char"])}
vocab_size = data["vocab_size"]
EMBED_DIM = data["embed_dim"]
LSTM_UNITS = data["lstm_units"]

# Функция кодирования строки в индексы
def text_to_seq(text):
    # неизвестные символы отобразим в PAD (можно иначе)
    return [char2idx.get(ch, char2idx["<PAD>"]) for ch in text]

# Функция декодирования списка индексов в строку (до символа конца или до конца списка)
def seq_to_text(seq):
    result = ""
    for idx in seq:
        if idx == char2idx["$"] or idx == char2idx["<PAD>"]:
            break
        # пропускаем символ начала '^' и неявные паддинги
        if idx == char2idx["^"]:
            continue
        result += idx2char[idx]
    return result

# Построение модели энкодера и декодера для инференса
# Энкодер (тот же, что в обучении)
encoder_inputs = tf.keras.Input(shape=(None,), name="encoder_input")
encoder_embed = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=EMBED_DIM, mask_zero=True)
encoder_lstm = tf.keras.layers.LSTM(LSTM_UNITS, return_state=True)
encoder_embed_out = encoder_embed(encoder_inputs)
_, state_h_enc, state_c_enc = encoder_lstm(encoder_embed_out)
encoder_model = tf.keras.Model(encoder_inputs, [state_h_enc, state_c_enc])

# Декодер
decoder_inputs = tf.keras.Input(shape=(1,), name="decoder_input")  # будем подавать по одному символу
dec_state_h_in = tf.keras.Input(shape=(LSTM_UNITS,), name="decoder_h")
dec_state_c_in = tf.keras.Input(shape=(LSTM_UNITS,), name="decoder_c")
decoder_embed = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=EMBED_DIM, mask_zero=True)
decoder_lstm = tf.keras.layers.LSTM(LSTM_UNITS, return_sequences=True, return_state=True)
decoder_dense = tf.keras.layers.Dense(vocab_size, activation='softmax')
# Пропускаем через слои
dec_embed_out = decoder_embed(decoder_inputs)
dec_outputs, dec_h_out, dec_c_out = decoder_lstm(dec_embed_out, initial_state=[dec_state_h_in, dec_state_c_in])
dec_probs = decoder_dense(dec_outputs)
# Модель декодера для получения следующего символа и новых состояний
decoder_model = tf.keras.Model([decoder_inputs, dec_state_h_in, dec_state_c_in],
                               [dec_probs, dec_h_out, dec_c_out])

# Загрузка весов в модель
# Так как мы строили заново Layers, загрузим веса через общий контейнер Sequential модели
# Создадим временную модель, чтобы использовать load_weights
inputs1 = tf.keras.Input(shape=(None,))
inputs2 = tf.keras.Input(shape=(None,))
temp_embed = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=EMBED_DIM, mask_zero=True)
temp_enc_lstm = tf.keras.layers.LSTM(LSTM_UNITS, return_state=True)
temp_dec_lstm = tf.keras.layers.LSTM(LSTM_UNITS, return_sequences=True, return_state=True)
temp_dense = tf.keras.layers.Dense(vocab_size, activation='softmax')
enc_out, enc_h, enc_c = temp_enc_lstm(temp_embed(inputs1))
dec_out, _, _ = temp_dec_lstm(temp_embed(inputs2), initial_state=[enc_h, enc_c])
temp_out = temp_dense(dec_out)
temp_model = tf.keras.Model([inputs1, inputs2], temp_out)
# Загрузим веса
temp_model.load_weights(MODEL_WEIGHTS_FILE)
# Переносим веса в наши модели энкодера/декодера
encoder_embed.set_weights(temp_embed.get_weights())
encoder_lstm.set_weights(temp_enc_lstm.get_weights())
decoder_embed.set_weights(temp_embed.get_weights())    # embedding общий
decoder_lstm.set_weights(temp_dec_lstm.get_weights())
decoder_dense.set_weights(temp_dense.get_weights())

# Готово: encoder_model и decoder_model имеют загруженные веса.

# Запуск интерактивного режима
print("Введите слово в любом падеже (или 'exit' для выхода):")
for line in sys.stdin:
    word = line.strip()
    if not word or word.lower() == "exit":
        break
    # Преобразуем входное слово в последовательность индексов и прогоняем через энкодер
    encoder_input_seq = np.array([text_to_seq(word)], dtype=np.int32)
    state_h, state_c = encoder_model.predict(encoder_input_seq, verbose=0)
    # Инициализируем генерацию: подаем в декодер символ начала '^'
    target_seq = np.array([[char2idx["^"]]], dtype=np.int32)
    output_indices = []  # здесь накопим индексы выходной последовательности
    # Генерируем по одному символу
    while True:
        probs, state_h, state_c = decoder_model.predict([target_seq, state_h, state_c], verbose=0)
        # probs.shape = (1, 1, vocab_size) — распределение вероятностей для следующего символа
        idx = int(np.argmax(probs[0, 0, :]))  # выбираем самый вероятный символ (greedy)
        if idx == char2idx["$"] or len(output_indices) >= 100:  # ограничимся макс. длиной
            # конец последовательности
            break
        output_indices.append(idx)
        # следующий вход декодера - предсказанный символ
        target_seq = np.array([[idx]], dtype=np.int32)
    # Преобразуем полученные индексы в строку и разделяем на формы
    output_text = seq_to_text(output_indices)
    forms = output_text.split("|")
    if len(forms) == 6:
        case_names = ["Атооч", "Илик", "Барыш", "Табыш", "Жатыш", "Чыгыш"]
        print("Результат склонения:")
        for name, form in zip(case_names, forms):
            print(f"{name}: {form}")
    else:
        # Если формат неожиданно неверный (не 6 частей), выведем всю строку для отладки
        print("Предсказанные формы:", output_text)
    print("\nВведите слово (или 'exit' для выхода):")
