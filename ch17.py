from Crypto.Cipher import AES
from Crypto.Random import random
import binascii
import ch9
import ch10
import ch11
import ch15

strings = [
    b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
    b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
    b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
    b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
    b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
    b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
    b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
    b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
    b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
    b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
]

key = ch11.rand_bytes(16)
iv = ch11.rand_bytes(16)

def enc_oracle():
    global key
    global iv

    cipher = ch10.CBC(AES.new(key, AES.MODE_ECB), iv)

    plaintext = binascii.a2b_base64( random.choice(strings) )
    padded = ch9.pad_PCKS7(plaintext, 16)

    return cipher.encrypt(padded)

def decrypt_check_pad(ciphertext):
    global key
    global iv

    cipher = ch10.CBC(AES.new(key, AES.MODE_ECB), iv)
    plaintext = cipher.decrypt(ciphertext)

    return ch15.isValid_PKCS7(plaintext)

def break_block(cipherblock, blk_sz):
    print(cipherblock)
    intermediate = b''
    plaintext = b''
    for i in range(1, blk_sz + 1):
        zeros = bytes(blk_sz - i)
        for j in range(256):
            fake_ciphertext = zeros + bytes([j]) + bytes([(c^i) for c in intermediate])
            ret = decrypt_check_pad(fake_ciphertext + cipherblock)
            if ret:
                print(j)
                print(i)
                #print(j^i)
                #print(fake_ciphertext + bytes([j] * i) + cipherblock)
                #print('--')
                intermediate = bytes([j ^ i]) + intermediate
                #print(cipherblock[i - 1] ^ intermediate)
                plaintext = bytes([cipherblock[-i] ^ intermediate[-i]]) + plaintext
                break
            if j == 255:
                print(i)
                print(intermediate)
                print(fake_ciphertext[-1])
                raise Exception('No match found.')

    return plaintext

def break_oracle(ciphertext, blk_sz):
    plaintext = b''
    blocks = [ciphertext[i:i+blk_sz] for i in range(0, len(ciphertext), blk_sz)]

    #for j in range( len(blocks)-1, 1, -1 ):
    plaintext = break_block(blocks[ len(blocks) - 1 ], blk_sz) + plaintext

    return plaintext

def main():
    enc = enc_oracle()
    print(enc)
    print( break_oracle(enc, 16) )

if __name__ == '__main__':
    main()
