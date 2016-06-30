from Crypto.Cipher import AES
import ch11
import ch9

def key_val_parse(s):
    pairs = s.split(b'&')
    ret = []
    
    for i in range( len(pairs) ):
        ret.append( pairs[i].split(b'=') )

    return ret        

def profile_for(email):
    email = sanitize(email)

    profile = [
        ['email', email],
        ['uid', 10],
        ['role', 'user']
    ]

    return profile_encode(profile)

def sanitize(email):
    return email.replace('=', '').replace('&', '')

def profile_encode(profile):
    profile_str = ''

    for i in range( len(profile) ):
        profile_str += profile[i][0] + '=' + str(profile[i][1]) + '&'
    # Remove trailing ampersand ('&')
    profile_str = profile_str[:-1]

    return profile_str

def profile_encrypt(profile_str, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt( ch9.pad_PCKS7(profile_str.encode(), 16) )

def profile_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = unpad_PCKS7( cipher.decrypt(ciphertext) )

    return decrypted

def unpad_PCKS7(s):
    pad_length = s[-1]
    return s[0:-pad_length]

def main():
    key = ch11.rand_bytes(16)
    
    email1 = 'test@davs.com' # Want this to be 13 characters
    email2 = 'adminadminadmindf' + ('\x0b' * 11) # Want admin string to start after 10 characters
    profile1 = profile_for(email1)
    profile2 = profile_for(email2)

    enc1 = profile_encrypt(profile1, key)
    enc2 = profile_encrypt(profile2, key)

    dec1 = profile_decrypt(enc1, key)
    dec2 = profile_decrypt(enc2, key)

    print( dec1[0:32] + dec2[16:32] )
    print( profile_decrypt(enc1[0:32] + enc2[16:32], key) )

if __name__ == "__main__":
    main()
