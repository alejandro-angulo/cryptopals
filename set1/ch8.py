import binascii
import itertools
from Crypto.Cipher import AES

def detect_ECB(s, key_sz):
    blocks = [ s[i:i + key_sz] for i in range(0, len(s), key_sz) ]
    pairs = itertools.combinations(blocks, 2)

    for p in pairs:
        if p[0] == p[1]:
            return True

    return False

def main():
    fname = '8.txt'
    fh = open(fname, 'r')
    key_sz = 16

    line_num = 1
    for line in fh:
        if line[-1] == '\n':
            line = line[:-1]

        contents = binascii.unhexlify( line )
        if detect_ECB(contents, key_sz) :
            print(line_num)

        line_num += 1
        

if __name__ == "__main__":
	main()
