import binascii

def repeatingKeyXOR(key, s):
    keylength = len(key)
    strlength = len(s)

    cipher = [0] * strlength

    for i in range(keylength):
        for j in range(i, strlength, keylength):
            cipher[j] = s[j] ^ key[i]

    ciphertext = b''.join( bytes([i]) for i in cipher )
    return ciphertext

def main():
    key = "ICE"
    string = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"

    ciphertext = repeatingKeyXOR( bytes(key, "utf-8"), bytes(string, "utf-8"))
    print( binascii.hexlify(ciphertext) )
    

if __name__ == '__main__':
    main()
