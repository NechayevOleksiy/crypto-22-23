import math
import re

alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"

def clear_text(text, spaces=True):
    text = text.replace("\n", " ").replace("\r", "").lower().replace("ё", "е").replace("ъ", "ь")
    text = re.sub(r"[^а-я ]", "", text)
    if spaces:
        text = text.replace(" ", "")
    return text

def calculate_frequencies(text):
    frequencies = {}
    for i in text:
        frequencies[i] = frequencies.get(i, 0) + 1
    total_characters = len(text)
    probabilities = {character: frequency / total_characters for character, frequency in frequencies.items()}
    return probabilities

def calculate_entropy(probabilities):
    entropy = -sum(probability * math.log2(probability) for probability in probabilities.values())
    return entropy

def calculate_redundancy(entropy, alphabet_size):
    maximum_entropy = math.log2(alphabet_size)
    redundancy = 1 - entropy / maximum_entropy
    return redundancy

filename = "brick.txt"
with open(filename, "r", encoding='utf-8') as file:
    text = file.read()

text_without_spaces = clear_text(text, spaces=False)
text_with_spaces = clear_text(text)

probabilities_no_spaces = calculate_frequencies(text_without_spaces)
entropy_no_spaces = calculate_entropy(probabilities_no_spaces)
redundancy_no_spaces = calculate_redundancy(entropy_no_spaces, len(alphabet))

probabilities_with_spaces = calculate_frequencies(text_with_spaces)
entropy_with_spaces = calculate_entropy(probabilities_with_spaces)
redundancy_with_spaces = calculate_redundancy(entropy_with_spaces, len(alphabet) + 1)

print("H1 без пробілів:", entropy_no_spaces)
print("R1 без пробілів:", redundancy_no_spaces)

print("H1 з пробілами:", entropy_with_spaces)
print("R1 з пробілами:", redundancy_with_spaces)

def calculate_bigram_frequencies(text, crossed):
    bigram_frequencies = {}
    text_length = len(text) if crossed else len(text) * 2
    step = 2 if crossed else 1
    for i in range(0, len(text) - 1, step):
        bigram = text[i] + text[i + 1]
        bigram_frequencies[bigram] = bigram_frequencies.get(bigram, 0) + 1
    bigram_probabilities = {bigram: frequency / text_length for bigram, frequency in bigram_frequencies.items()}
    return bigram_probabilities

def calculate_bigram_entropy(probabilities):
    entropy = -sum(probability * math.log2(probability) for probability in probabilities.values())
    return entropy



H2_no_spaces_cross = calculate_bigram_entropy(calculate_bigram_frequencies(text_without_spaces, crossed=True))
R2_no_spaces_cross = calculate_redundancy(H2_no_spaces_cross, len(alphabet))

H2_with_spaces_cross = calculate_bigram_entropy(calculate_bigram_frequencies(text_with_spaces, crossed=True))
R2_with_spaces_cross = calculate_redundancy(H2_with_spaces_cross, len(alphabet) + 1)

H2_no_spaces_no_cross = calculate_bigram_entropy(calculate_bigram_frequencies(text_without_spaces, crossed=False))
R2_no_spaces_no_cross = calculate_redundancy(H2_no_spaces_no_cross, len(alphabet))

H2_with_spaces_no_cross = calculate_bigram_entropy(calculate_bigram_frequencies(text_with_spaces, crossed=False))
R2_with_spaces_no_cross = calculate_redundancy(H2_with_spaces_no_cross, len(alphabet) + 1)

print("H2 без пробілів, з перетинами:", H2_no_spaces_cross)
print("R2 без пробілів, з перетинами:", R2_no_spaces_cross)

print("H2 з пробілами,  з перетинами:", H2_with_spaces_cross)
print("R2 з пробілами,  з перетинами:", R2_with_spaces_cross)

print("H2 без пробілів, без перетинів:", H2_no_spaces_no_cross)
print("R2 без пробілів, без перетинів:", R2_no_spaces_no_cross)

print("H2 з пробілами, без перетинів:", H2_with_spaces_no_cross)
print("R2 з пробілами, без перетинів:", R2_with_spaces_no_cross)

print("1.747 < H10 < 2.410")
print((1 - (1.747 / math.log2(len(alphabet) + 1))), "> R >", (1 - (2.410 / math.log2(len(alphabet) + 1))))

print("1.964 < H20 < 2.682")
print((1 - (1.964 / math.log2(len(alphabet) + 1))), "> R >", (1 - (2.682 / math.log2(len(alphabet) + 1))))

print("1.669 < H30 < 2.204")
print((1 - (1.669 / math.log2(len(alphabet) + 1))), "> R >", (1 - (2.204 / math.log2(len(alphabet) + 1))))