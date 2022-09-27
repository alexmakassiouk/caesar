from alphabets import ENGLISH_ALPHABET, NORWEGIAN_ALPHABET
from caesar import alphabet_recognition, decrypt_without_offset

def decrypt_without_alphabet(text):
    alphabet_index = alphabet_recognition(text) #Runtime may be much better, but no practical implications on decently sized texts
    match alphabet_index:
        case 0:
            return decrypt_without_offset(text, ENGLISH_ALPHABET)
        case 1:
            return decrypt_without_offset(text, NORWEGIAN_ALPHABET)
        case _:
            return "No support for this alphabet yet!"