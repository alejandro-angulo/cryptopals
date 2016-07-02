from Crypto.Cipher import AES
import binascii
import ch9
import ch11

postfix = b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'
postfix += b'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
postfix += b'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg'
postfix += b'YnkK'

key = None

def enc_oracle(plaintext):
    global key
    if key is None:
        key = ch11.rand_bytes(16)

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext += binascii.a2b_base64(postfix)
    #plaintext = ch11.rand_padding(plaintext)
    plaintext = ch9.pad_PCKS7(plaintext, 16)

    return cipher.encrypt(plaintext)

def find_blk_sz(oracle):
    zero_len = len( oracle(b'') )
    blk_sz = 1

    while True:
        plaintext = bytes(blk_sz)
        encrypted = oracle(plaintext)
        
        if len(encrypted) != zero_len:
            return len(encrypted) - zero_len

        blk_sz += 1

def is_ECB(oracle, blk_sz):
    s = bytes(blk_sz * 2)
    encrypted = oracle(s)

    if encrypted[0 : blk_sz] == encrypted[blk_sz : 2*blk_sz]:
        return True

    return False

def byte_by_byte(oracle, known, blk_sz):
    short_str = bytes(blk_sz - 1 - (len(known) % blk_sz))

    test = enc_oracle( short_str )

    for j in range(256):
        plaintext = short_str + known + bytes([j])
        ciphertext = enc_oracle(plaintext)[:blk_sz]

        if test[:len(short_str) + 1 + len(known)] == ciphertext:
            return bytes([j])

    return None

def main():
    blk_sz = find_blk_sz(enc_oracle) 
    if not is_ECB(enc_oracle, blk_sz):
        raise Exception('Not ECB')

    string = b''
    while True:
        ret = byte_by_byte(enc_oracle, string, 10*blk_sz)
        if ret is None:
            break

        string += ret

    print(string)

if __name__ == "__main__":
    main()
