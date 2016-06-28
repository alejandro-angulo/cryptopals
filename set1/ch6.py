import binascii
import ch3
import ch5

def hamming(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Strings must be of equal length when computing Hamming distance.")

    distance = 0
    for i in range( len(s1) ):
        distance += bin(s1[i] ^ s2[i]).count('1') 

    return distance

def crack_repeatingKeyXOR(s, key_sz):
    blocks = [ s[i:i + key_sz] for i in range(0, len(s), key_sz) ]
    transposed_blocks = []

    shortest_block = len( blocks[-1] )

    print( shortest_block )

    key = []
    for i in range( key_sz ):
        string = []
        for block in blocks:
            if block == blocks[-1] and i >= shortest_block:
                continue
            #print(i)
            string.append( block[i] )
        
        transposed_blocks.append(string)
        key.append( ch3.crack_singleByteXOR(string)[0] )

    print(key)
    return key

def guess_keysize(s):
    keysizes = {}
    start_sz = 2
    end_sz = 40

    for i in range(start_sz, end_sz + 1):
        blocks = [ s[j:j+i] for j in range(0, len(s), i) ][0:4]
        
        distances = []
        
        for j in range( len(blocks) ):
            for k in range( j, len(blocks) ):
                if j == k:
                    continue

                distances.append( hamming(blocks[j], blocks[k]) / i )

        
        average = sum(distances) / len(distances)
        keysizes[i] = average

    mini = 999999
    key_sz = -1
    for i in range( start_sz, end_sz + 1 ):
        if keysizes[i] < mini:
            mini = keysizes[i]
            key_sz = i

    return key_sz


def main():
#    print( hamming(b'this is a test', b'wokka wokka!!!') )

    fname = '6.txt'
    fh = open(fname, 'r')
    contents = binascii.a2b_base64( fh.read() )
    key_sz = guess_keysize(contents)
    print(key_sz)
    key = crack_repeatingKeyXOR(contents, key_sz)
    print( ''.join( chr(c) for c in key ) )
    print( ch5.repeatingKeyXOR(key, contents) )

if __name__ == '__main__':
    main()
