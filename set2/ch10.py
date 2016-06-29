import binascii
from Crypto.Cipher import AES

class CBC:
    def __init__(self, ECB, IV):
        self._ECB = ECB
        self._IV = IV
        self._blocksize = 16

    def _partition_blocks(self, s):
        return [s[i : i+self._blocksize] for i in range (0, len(s), self._blocksize)]

    def encrypt(self, plaintext):
        plainblocks = self._partition_blocks(plaintext)
        prev = self._IV
        ciphertext = b''
      
        for plainblock in plainblocks:
            xortext = b''
            for i in range( len(prev) ):
                xortext += bytes([ plainblock[i] ^ prev[i] ])

            cipherblock = self._ECB.encrypt( xortext )
            ciphertext += cipherblock
            prev = cipherblock

        return ciphertext

    def decrypt(self, ciphertext):
        cipherblocks = self._partition_blocks(ciphertext)
        prev = self._IV
        plaintext = b''

        for cipherblock in cipherblocks:
            xortext = b''

            plainblock = self._ECB.decrypt(cipherblock)
            for i in range( len(prev) ):
                xortext += bytes([ plainblock[i] ^ prev[i] ])

            plaintext += xortext
            prev = cipherblock

        return plaintext

def main():
    fname = '10.txt'
    fh = open(fname)
    contents = binascii.a2b_base64( fh.read() )

    key = b'YELLOW SUBMARINE'    
    IV = bytes(16)

    test = CBC( AES.new(key, AES.MODE_ECB), IV )
    #encrypted = test.encrypt(contents)
    #decrypted = test.decrypt(encrypted)
    decrypted = test.decrypt(contents)
    print(decrypted)
    encrypted = test.encrypt(decrypted)

    if encrypted == contents:
        print('Yay')
    else:
        print('fuck')

if __name__ == "__main__":
    main()
