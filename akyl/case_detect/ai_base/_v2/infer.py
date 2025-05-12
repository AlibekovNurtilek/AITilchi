# ✅ Google Colab блок для инференса модели (Атооч → 5 падежей)

import numpy as np
import tensorflow as tf
import json

# === Загрузка модели и словаря ===
model = tf.keras.models.load_model("akyl/case_detect/ai_base/_v2/atooch_to_cases_model.keras")
with open("akyl/case_detect/ai_base/_v2/atooch_char2idx.json", "r", encoding="utf-8") as f:
    char2idx = json.load(f)
idx2char = {i: ch for ch, i in char2idx.items()}
EOS = char2idx["<EOS>"]
PAD = char2idx["<PAD>"]

max_len_input = model.input_shape[1]
max_len_output = model.output_shape[0][1]

# === Вспомогательные функции ===
def encode(word):
    seq = [char2idx.get(ch, PAD) for ch in word] + [EOS]
    return np.array([seq + [PAD]*(max_len_input - len(seq))])

def decode(indices):
    return ''.join(idx2char.get(int(i), '') for i in indices if int(i) not in [EOS, PAD])

# === Интерактивный инференс ===
print("\n🔤 Введите слово в падеже Атооч:")
while True:
    word = input("Атооч (или 'exit'): ").strip()
    if word.lower() == "exit":
        break
    if not word:
        continue
    x = encode(word)
    preds = model.predict(x, verbose=0)
    cases = ["Илик", "Барыш", "Табыш", "Жатыш", "Чыгыш"]
    print(f"\nСлово: {word}")
    for i, p in enumerate(preds):
        pred_seq = np.argmax(p[0], axis=-1)
        print(f"{cases[i]}: {decode(pred_seq)}")
    print("\n---\n")
