import ch9
import ch10
from Crypto.Cipher import AES
from Crypto.Random import random

def rand_bytes(key_sz):
    # 8 bits to a byte
    return random.getrandbits(key_sz * 8).to_bytes(key_sz, 'big')

def rand_padding(s):
    pre_padlen = random.randint(5, 10)
    post_padlen = random.randint(5, 10)

    prefix = random.getrandbits(8 * pre_padlen).to_bytes(pre_padlen, 'big')
    postfix = random.getrandbits(8 * post_padlen).to_bytes(post_padlen, 'big')

    return prefix + s + postfix

def oracle(plaintext, num_bytes):
    key = rand_bytes(num_bytes)
    cipher = AES.new(key, AES.MODE_ECB)
    
    plaintext = rand_padding(plaintext)
    plaintext = ch9.pad_PCKS7(plaintext, num_bytes)

    if random.randint(0, 1) == 1:
        print("Using CBC")
        IV = rand_bytes(num_bytes)
        cipher = ch10.CBC(cipher, IV)
    else:
        print("Using EBC")

    return cipher.encrypt(plaintext)

def detect(oracle, num_bytes):
    s = bytes(50)
    encrypted = oracle(s, num_bytes)

    if encrypted[num_bytes : 2*num_bytes] == encrypted[2*num_bytes : 3*num_bytes]:
        return 'ECB'

    return 'CBC'

def main():
    print( detect(oracle, 16) )

if __name__ == "__main__":
    main()
