import binascii
from Crypto.Cipher import AES

class CTR:
    def __init__(self, ECB, nonce):
        self._ECB = ECB
        self._nonce = nonce
        self._blk_sz = 16
        self._keybytes = b''
        self._num_blks = 0

    def encrypt(self, plaintext):
        

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)

def main():
    print('test')

if __name__ == "__main__":
    main()
