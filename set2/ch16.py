from Crypto.Cipher import AES
import ch9
import ch10
import ch11
    
key = ch11.rand_bytes(16)
IV  = ch11.rand_bytes(16)

def enc_userdata(s):
    global key
    global IV

    prefix = "comment1=cooking%20MCs;userdata="
    suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

    cipher = ch10.CBC(AES.new(key, AES.MODE_ECB), IV)

    s = s.replace(';', '%3B').replace('=', '%3D')
    s = (prefix + s + suffix).encode('utf-8')
    s = ch9.pad_PCKS7(s, 16)
    
    return cipher.encrypt(s)

def dec_userdata(ciphertext):
    cipher = ch10.CBC(AES.new(key, AES.MODE_ECB), IV)
    plaintext = cipher.decrypt(ciphertext)

    return plaintext

def is_admin(userdata):
    if userdata.find(b';admin=true;') != -1:
        return True

    return False

def main():
    key = ch11.rand_bytes(16)
    plaintext = ('x' * 16) + '!admin.true!'
    enc = bytearray(enc_userdata(plaintext))
    enc[32] ^= 26 # '!' ^ 26 = ';'
    enc[38] ^= 19 # '.' ^ 19 = '='
    enc[43] ^= 26 # '!' ^ 26 = ';'
    dec = dec_userdata(bytes(enc))
    print(dec)
    print( is_admin(dec) )

if __name__ == "__main__":
    main()
