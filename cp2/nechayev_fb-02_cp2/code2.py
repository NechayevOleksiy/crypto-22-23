import os

alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'

keys = ['мы', 'мир', 'соло', 'белка', 'автомобиль', 'авиатопливо', 'адаптивность', 'администрация', 'автоинструктор', 'благополучность', 'гельминтоспориоз',
       'гражданственность', 'лесопромышленность', 'абонементодержатель', 'интровертированность']

def filter(text):      # фільтрація тексту 
    a = []
    text = text.lower()
    text = text.replace('ё', 'е')
    for letter in text:
        if letter in alphabet:
            a.append(letter)
    text = ''.join(a)
    return text

file = open(".\\lab2.txt", "r", encoding='UTF-8')
text = file.read()
file.close()

filtered_text = filter(text)
file = open(".//filtered.txt", "w")
file.write(filtered_text)
file.close()


def encrypt(text, key):      #шифрування
    a = []
    for i, letter in enumerate(text):
        indextext = alphabet.index(letter)
        indexkey = alphabet.index(key[(i % len(key))])
        encletter = alphabet[(indextext + indexkey) % len(alphabet)]
        a.append(encletter)

    return ''.join(a)


def indcom(text):    #знаходження індексів відповідності
    index = 0
    for i in range(0, len(alphabet)):
        N = text.count(alphabet[i])
        index += N * (N - 1)
    index = (len(text) * (len(text) - 1))
    return index


if os.path.exists(".//task1.txt"):
    os.remove(".//task1.txt")

# запис в файл індекса відкритого тексту
file = open(".//task1.txt", "w")
wrind = "Normal text index: " + str(indcom(filtered_text)) + "\n\n"
file.write(wrind)

# цикл шифрування з різними ключами
# і підрахунку і. відповідності
for key in keys:
    enctext = encrypt(filtered_text, key)
    wrind = "Text, encrypted with key length " + \
        str(len(key)) + " index = " + \
        str(indcom(enctext)) + "\n" + enctext + "\n\n"
    file.write(wrind)
file.close()


file = open(".//enclab2.txt", "r", encoding='UTF-8')
enctext = file.read()
enctext = enctext.replace('\n', '')
file.close()


def fkey(text):  # знаходження довжини ключа
    parts = []
    aindex = 0
    for i in range(2, len(alphabet)):
        for k in range(0, i):
            parts.append(text[k::i])
            aindex += indcom(parts[-1])
        aindex /= i
        wrind = "r" + "(" + str(i) + ")" + ": " + str(aindex) + "\n"
        file.write(wrind)
        aindex = 0

    parts = []
    for i in range(15):

        parts.append(text[i::15])

    # підрахунок букв які зустрічаються в отриманих частинах найчастіше
    a = []
    per = []
    max_per_letters = []
    for i in range(len(parts)):
        # створення масива з елемента масива
        for letter in parts[i]:
            a.append(letter)
        # підрахунок
        for letter in a:
            per.append(a.count(letter) / len(a))
        max_per = max(per)
        max_per_letters.append(a[per.index(max_per)])
        a = []
        per = []

    # знаходження ключа шифром цезаря з k = 14(о)
    key = []
    for letter in max_per_letters:
        key.append(alphabet[(alphabet.index(letter) - 14) % len(alphabet)])
    print(key) 
    return ''.join(key)


def decrypt(text, key):  #розшифрування
    a = []
    for i, letter in enumerate(text):
        indtext = alphabet.index(letter)
        indkey= alphabet.index(key[(i % len(key))])
        encletter = alphabet[(indtext - indkey) % len(alphabet)]
        a.append(encletter)
    return ''.join(a)

if os.path.exists(".\\indexes.txt"):
    os.remove(".\\indexes.txt")
file = open(".\\indexes.txt", "a")

fkey(enctext)
file.close()

print("Enter key to decode text:")
key = input()

dectext = decrypt(enctext, key)

file = open(".//declab2.txt", "w")
file.write(dectext)
file.close()