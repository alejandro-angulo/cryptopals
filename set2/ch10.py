import binascii
import itertools

class CBC:
    def __init__(self, ECB, IV):
        self._ECB = ECB
        self._IV = IV
        self._blocksize = 16

def main():
    key = b'YELLOW SUBMARINE'    
    IV = bytes(16)
    print(IV)

if __name__ == "__main__":
    main()
