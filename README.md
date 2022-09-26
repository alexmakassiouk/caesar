# Caesar Encryption/Decryption

main file: caesar.py

Feel free to use sample texts located in 'data' folder.

alphabets.py contains some supported alphabets

commonWords.py is used for decryption when the key/offset is unknown

encrypt(text, alphabet, offset) is the core of the application

decrypt_without_alphabet(text) is the most complex method. This calls alphabet_recognition(text) to find the closest alphabet used in text. Then it calls decrypt_without_offset(text, alphabet) which compares some common words used in associated alphabet to the encrypted text input. The text input is iterated over for each possible offset.
