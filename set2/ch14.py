from Crypto.Cipher import AES
from Crypto.Random import random
import ch12
import ch9
import ch11

prefix = None
key = None
num = 0

def enc_oracle(plaintext):
    global key
    global prefix
    global num

    blk_sz = 16

    if key == None:
        key = ch11.rand_bytes(blk_sz)
    if prefix == None:
        num = random.randint(8, 32) 
        prefix = ch11.rand_bytes(num)

    cipher = AES.new(key, AES.MODE_ECB)

    plaintext = prefix + plaintext + ch12.postfix
    plaintext = ch9.pad_PCKS7(plaintext, blk_sz)

    return cipher.encrypt(plaintext)

def find_prefix_size(oracle, blk_sz):
    tests = [
        oracle(b''),
        oracle(b'a')
    ]
    blocks = [
        get_blocks(tests[0], blk_sz),
        get_blocks(tests[1], blk_sz)
    ]

    for i in range( len(blocks[0]) ):
        print(blocks[0][i])
        print(blocks[1][i])
        for j in range(blk_sz):
            if blocks[0][i][j] != blocks[1][i][j]:
                return i*blk_sz + j

def get_blocks(s, blk_sz):
    return [s[i : i+blk_sz] for i in range(0, len(s), blk_sz)]

def main():
    global prefix
    global num

    blk_sz = ch12.find_blk_sz(enc_oracle)

    print(num)
    print(prefix)
    print(enc_oracle(b'test'))
    print('--')

    pre_sz = find_prefix_size(enc_oracle, blk_sz)
    print(pre_sz)

if __name__ == "__main__":
    main()
