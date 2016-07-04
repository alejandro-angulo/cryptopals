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

def break_block(cipherblocks, blk_sz):
    intermediate = b''
    plaintext = b''
    for i in range(1, blk_sz + 1):
        zeros = bytes(blk_sz - i)
        for j in range(256):
            fake_ciphertext = zeros + bytes([j]) + bytes([(c^i) for c in intermediate])
            ret = decrypt_check_pad(fake_ciphertext + cipherblocks[1])
            if ret:
                intermediate = bytes([j ^ i]) + intermediate
                plaintext = bytes([cipherblocks[0][-i] ^ intermediate[-i]]) + plaintext
                break

    return plaintext

def break_oracle(ciphertext, blk_sz):
    global iv

    plaintext = b''
    blocks = [ciphertext[i:i+blk_sz] for i in range(0, len(ciphertext), blk_sz)]

    for i in range( len(blocks), 1, -1 ):
        plaintext = break_block(blocks[i-2:i], blk_sz) + plaintext
    plaintext = break_block([iv, blocks[0]], blk_sz) + plaintext

    return plaintext

def main():
    enc = enc_oracle()
    print(enc)
    print( ch15.unpad_PKCS7(break_oracle(enc, 16)) )

if __name__ == '__main__':
    main()
