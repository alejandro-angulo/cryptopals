import binascii
from Crypto.Cipher import AES

def main():
    key = b'YELLOW SUBMARINE'

    fname = '7.txt'
    fh = open(fname)
    contents = binascii.a2b_base64( fh.read() )

    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(contents)

    print(decrypted)

if __name__ == "__main__":
	main()
