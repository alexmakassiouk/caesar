from operator import indexOf
from alphabets import ALPHABETS, ENGLISH_ALPHABET, NORWEGIAN_ALPHABET, GREEK_ALPHABET, CYRILLIC_ALPHABET, HEBREW_ALPHABET
from commonWords import common_words
import re


def load_text(filename):
    with open('data/' + filename) as f:
        text = f.read()
        return text

def write_file(filename, data):
    with open('data/' + filename, 'w') as f:
        f.write(data)

def offset_alphabet(alphabet, offset):
    #If offset is greater than length of alphabet: Find the offset modulus the length of alphabet
    offset = offset%len(alphabet)
    new_alphabet = alphabet[offset:] + alphabet[:offset]
    return new_alphabet

def offset_another_alphabet(original_alphabet, new_alphabet, offset):
    #TODO
    #Fungerer vel kanskje ikke å få en én-til-én mapping mellom alfabeter av ulik lengde
    pass


def encrypt(text, alphabet, offset):
    special_chars = ['\n', ',', '.', '-', '_', '"', '\t', '/', '!', '?', '$', ':', ';', "'", '#', '%', '&', '(', ')', '=', '@', '*']
    encryption_alphabet = offset_alphabet(alphabet, offset)
    encrypted_text = ""
    for char in text:
        char = char.lower()
        if char.isdigit():
            encrypted_text+=str((int(char)+offset)%10)
        elif char in special_chars:
            encrypted_text+=char
        else:
            index = indexOf(alphabet, char)
            encrypted_text+=encryption_alphabet[index]
    return encrypted_text

def decrypt(text, alphabet, offset):
    return encrypt(text, alphabet, -offset)


def decrypt_without_alphabet(text):
    alphabet_index = alphabet_recognition(text)
    alphabet = ALPHABETS[alphabet_index]
    match alphabet_index:
        case 0:
            return decrypt_without_offset(text, ENGLISH_ALPHABET)
        case 1:
            return decrypt_without_offset(text, NORWEGIAN_ALPHABET)
        case _:
            return "No support for this alphabet yet!"

def decrypt_without_offset(text, alphabet):
    matches = [0] * len(alphabet)
    for i in range(1,len(alphabet)):
        shifted_text = encrypt(text, alphabet, i)
        encrypted_words = re.split(', |\ |_|-|!', shifted_text)
        for word in common_words[alphabet_recognition(alphabet)]:
            if word in encrypted_words:
                matches[i]+=1
    best_offset = indexOf(matches, max(matches))
    return encrypt(text, alphabet, best_offset)


# Ideer for dekryptering uten å vite offset: 
# Se på antall mellomrom. Hvor mange gjennomsnittlige mellomrom ifht. antall bokstaver?
# Bruke de mest brukte ordene i ulike språk

def alphabet_recognition(text): 
    english_counter = norwegian_counter = greek_counter = cyrillic_counter = hebrew_counter = 0
    counters = [english_counter, norwegian_counter, greek_counter, cyrillic_counter ,hebrew_counter]
    for char in text:
        i=0
        for alphabet in ALPHABETS:
            if char in alphabet:
                counters[i]+=1
            i+=1
    return indexOf(counters, max(counters))

kryptertNorsk = load_text("kryptertFil.txt")
print(decrypt_without_alphabet(kryptertNorsk))

###### TESTING ######
#encryptedEnglish = load_text("encryptedEnglish.txt")
#print(decrypt_without_alphabet(encryptedEnglish))


#plaintext = loadText("plaintext.txt")
#greek_lorem_impsum = loadText("loremIpsumGreek.txt")
#russian_text = loadText("russianText.txt")
#englishPlaintext = loadText("englishPlaintext.txt")
#
#encrypted_text = encrypt(russian_text, CYRILLIC_ALPHABET, 17)
#print(encrypted_text)
#print(decrypt(encrypted_text, CYRILLIC_ALPHABET, 17))
#print(alphabet_recognition(encrypted_text))

#def main():
#    filename = input("Skriv inn filnavn: (.txt)")
#    encrypt_char = input("Kryptere eller dekryptere? (K/D)")
#    offset = int(input("Gi inn offset: "))
#    text = load_text(filename)
#    alphabet_in_file = ALPHABETS[alphabet_recognition(text)]
#    if encrypt_char == 'K':
#        new_text = encrypt(text, alphabet_in_file, offset)
#    else:
#        new_text = decrypt(text, alphabet_in_file, offset)
#        print(new_text)
#    write_char = input("Lagre til fil? (J/N)")
#    if write_char == 'J':
#        filename = input("filnavn: ") + ".txt"
#    write_file(filename, new_text)
#    print("Lagret til ", filename, "!")
#main()