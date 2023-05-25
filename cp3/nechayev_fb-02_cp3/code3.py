from nltk import FreqDist
from collections import Counter
from nltk.util import ngrams
from math import log2

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

with open("10.txt", "r", encoding="utf-8") as f:
    ciphertext = f.read()
    processed_text = ciphertext.replace("\n", "")
    f.close()
print(processed_text)

def calculate_entropy(text):  # ентропія тексту
    all_letters = [Counter(text)[i] / len(text) for i in Counter(text)]
    return sum(all_t / sum(all_letters) * log2(sum(all_letters) / all_t) for all_t in all_letters)

def inverse(a, b):  # обернене з розширеним алгоритмом евкліда
    if extended_gcd(a, b)[0] != 1:
        return None
    else:
        _, _, y = extended_gcd(b, a % b)
        return y

def extended_gcd(a, b):  # розширений алгоритм евкліда
    if a == 0:
        return b, 0, 1
    gcd, _, __ = extended_gcd(b % a, a)
    x = __ - (b // a) * _
    y = _
    return gcd, x, y

def find_most_frequent_bigrams(text):  # пошук 5 найчастіших біграм
    bigram_fdist = FreqDist()
    bigrams = ngrams(text, 2)
    bigram_fdist.update(bigrams)
    return [i[0][0] + i[0][1] for i in bigram_fdist.most_common()[:5]]

def bigram_to_number(bigram):  # перетворення біграми в число
    return alphabet.index(bigram[0]) * 31 + alphabet.index(bigram[1])

def generate_all_bigram_combinations(text):  # знаходження всіх можливих варіантів біграм
    top_5_bigrams = ['ст', 'но', 'то', 'на', 'ен']
    top_5_bigrams_text, all_bigrams = find_most_frequent_bigrams(text), []
    return [[[pair1_bigram1, pair1_bigram2], [pair2_bigram1, pair2_bigram2]] for pair1_bigram2 in top_5_bigrams_text for pair1_bigram1 in top_5_bigrams
            for pair2_bigram2 in top_5_bigrams_text if pair2_bigram2 != pair1_bigram2 for pair2_bigram1 in top_5_bigrams
            if pair2_bigram1 != pair1_bigram1]

def check_text(text):  # перевірка тексту
    unreal_bigrams = ['аы', 'аь', 'йь', 'оы', 'уы', 'уь', 'чщ', 'чэ', 'ьы', 'яь', 'оь', 'ыь', 'еь', 'юь',
                 'эь', 'ць', 'хь', 'кь', 'йь', 'иь', 'гь', 'еы', 'эы', 'иы', 'яы', 'юы', 'ыы', 'ьь']
    return 4.2 < calculate_entropy(text) < 4.5 and sorted(Counter(text).items(), key=lambda let:
    (let[1], let[0]), reverse=True)[0][0] in ["о", "е"] and not any(ext in text for ext in unreal_bigrams)

def find_solutions(a, b, n):
    x, result = extended_gcd(a, n)[0], []
    if x == 1:
        rev = inverse(a, n)
        if isinstance(rev, int):
            result.append((rev * b) % n)
    elif b % x == 0:
        if inverse(a / x, n / x) is not None:
            return [((inverse(a / x, n / x) * b / x) % (n / x) + i * n / x) for i in range(int(x))]

    return result

def find_possible_keys(text):
    all_keys, all_bigrams = [], generate_all_bigram_combinations(text)
    for bigram_pair in all_bigrams:
        x1 = bigram_to_number(bigram_pair[0][0])
        x2 = bigram_to_number(bigram_pair[1][0])
        y1 = bigram_to_number(bigram_pair[0][1])
        y2 = bigram_to_number(bigram_pair[1][1])
        a = find_solutions(x1 - x2, y1 - y2, pow(31, 2))
        for i in a:
            if extended_gcd(i, 31)[0] != 1:
                continue
            b = (y1 - i * x1) % pow(31, 2)
            all_keys.append([int(i), int(b)])
    return all_keys

def affine_decrypt(text, keys):
    decrypted_text = ""
    key1, key2 = keys
    for i in range(0, len(text), 2):
        part1 = (extended_gcd(key1, pow(31, 2))[1] * (bigram_to_number(text[i:i + 2]) - key2))
        decrypted_text += alphabet[part1 % pow(31, 2) // 31] + alphabet[part1 % 31]
    return decrypted_text


all_keys = find_possible_keys(processed_text)
print(all_keys)
keys = []
for i in all_keys:
    if check_text(affine_decrypt(processed_text, i)):
        keys = i
        break
print(keys)
print(affine_decrypt(processed_text, keys))