from Crypto.Cipher import AES
from Crypto.Random import random
import ch12
import ch9
import ch11
import binascii
import math

prefix = None
key = None
num = 0

def gen_key(blk_sz):
    print("GENERATING KEY")
    return ch11.rand_bytes(blk_sz)

def gen_prefix(num):
    print("GENERATING PREFIX OF LENGTH {}".format(num))
    return ch11.rand_bytes(num)

def enc_oracle(plaintext):
    global key
    global prefix
    global num

    blk_sz = 16

    if key == None:
        key = gen_key(blk_sz)
    if prefix == None:
        num = random.randint(8, 64) 
        prefix = gen_prefix(num)

    cipher = AES.new(key, AES.MODE_ECB)

    plaintext = prefix + plaintext + binascii.a2b_base64(ch12.postfix)
    plaintext = ch9.pad_PCKS7(plaintext, blk_sz)

    return cipher.encrypt(plaintext)

def find_prefix_size(oracle, blk_sz):
    for i in range(2*blk_sz, 3*blk_sz):
        plain = bytes(i)
        encrypted = enc_oracle(plain)
        blocks = get_blocks(encrypted, blk_sz)
        for j in range( len(blocks) - 2 ):
            if blocks[j] == blocks[j+1]:
                # Found a repeat after j blocks
                # Length of prefix <= j * blk_sz
                # Repeated blocks found after sending i repeated bytes
                #   the i bytes take up (i // blk_sz) blocks
                #   (i % blk_sz) gives number of "spill over" bytes
                return (j * blk_sz) - (i % blk_sz)

def get_blocks(s, blk_sz):
    return [s[i : i+blk_sz] for i in range(0, len(s), blk_sz)]

def byte_by_byte_w_padding(oracle, known, blk_sz, pre_sz):
    padding_bytes = blk_sz - (pre_sz % blk_sz)
    padding_blks = math.ceil(pre_sz / blk_sz)
    short_str = bytes( blk_sz - 1 - (len(known) % blk_sz) + padding_bytes)

    test = enc_oracle(short_str)

    begin = blk_sz*padding_blks
    end = begin + blk_sz

    for j in range(256):
        plaintext = short_str + known + bytes([j])
        ciphertext = enc_oracle(plaintext)
        ciphertext = ciphertext[begin:end]

        if test[begin:end] == ciphertext:
            return bytes([j])

    return None

def main():
    blk_sz = ch12.find_blk_sz(enc_oracle)

    pre_sz = find_prefix_size(enc_oracle, blk_sz)

    string = b''
    for i in range(10*blk_sz):
        ret = byte_by_byte_w_padding(enc_oracle, string, 10*blk_sz, pre_sz)
        if ret is None:
            break

        string += ret

    print(string)

if __name__ == "__main__":
    main()
