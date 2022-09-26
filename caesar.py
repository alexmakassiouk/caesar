from operator import indexOf
from alphabets import ALPHABETS, ENGLISH_ALPHABET, NORWEGIAN_ALPHABET, GREEK_ALPHABET, CYRILLIC_ALPHABET, HEBREW_ALPHABET
from commonWords import common_words
import re

### FILE HANDLING ###
def load_text(filename):
    with open('data/' + filename) as f:
        text = f.read()
        return text
def write_file(filename, data):
    with open('data/' + filename, 'w') as f:
        f.write(data)
###-----------------###

### CORE METHODS ###
def offset_alphabet(alphabet, offset):
    #If offset is greater than length of alphabet: Find the offset modulus the length of alphabet
    offset = offset%len(alphabet)
    shifted_alphabet = alphabet[offset:] + alphabet[:offset] #Permutates alphabet. Starts with character on index 'offset' in original alphabet and ends with character on index 'offset'-1
    return shifted_alphabet

def encrypt(text, alphabet, offset):
    special_chars = ['\n', ',', '.', '-', '_', '"', '\t', '/', '!', '?', '$', ':', ';', "'", '#', '%', '&', '(', ')', '=', '@', '*', '–']
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
###----------------###


### ADDITIONAL FUN ###
def decrypt_without_alphabet(text):
    alphabet_index = alphabet_recognition(text) #Runtime may be much better, but no practical implications on decently sized texts
    match alphabet_index:
        case 0:
            return decrypt_without_offset(text, ENGLISH_ALPHABET)
        case 1:
            return decrypt_without_offset(text, NORWEGIAN_ALPHABET)
        case _:
            return "No support for this alphabet yet!"

def decrypt_without_offset(text, alphabet): # Finds the offset for which shifted_text yields most amount of words in common_words
    matches = [0] * len(alphabet)
    for i in range(1,len(alphabet)):
        shifted_text = encrypt(text, alphabet, i)
        encrypted_words = re.split(', |\ |_|-|!', shifted_text)
        for word in common_words[alphabet_recognition(alphabet)]:
            if word in encrypted_words: #Biggest concern on runtime
                matches[i]+=1
    if max(matches) != 0:
        best_offset = indexOf(matches, max(matches))
        return encrypt(text, alphabet, best_offset)
    else:
        return decrypt_by_spaces(text, alphabet)

def decrypt_by_spaces(text, alphabet): # Finds the offset which yields most amount of spaces in shifted_text
    spaces = [0] * len(alphabet)
    for i in range(1, len(alphabet)):
        shifted_text = encrypt(text, alphabet, i)
        for char in shifted_text:
            if char == " ":
                spaces[i]+=1
    best_offset = indexOf(spaces, max(spaces))
    return encrypt(text, alphabet, best_offset)

# Enda flere ideer for å dekryptere: Telle forekomster av punktum etterfulgt av mellomrom og stor bokstav.

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
###-----------------###



###### TESTING ######


kryptertNorsk = load_text("encryptedVGArticle.txt")
print(decrypt_by_spaces(kryptertNorsk, NORWEGIAN_ALPHABET))


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

### MAIN ###
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
###-------------###

#main()
