import binascii
import sys

def pad_PCKS7(s, blk_sz):
    pad_length = blk_sz - (len(s) % blk_sz)
    for i in range(pad_length):
        s += bytes( [pad_length] )

    return s

def main():
    string = b'YELLOW SUBMARINE'
    string = b'\x895\xbe\xec\r\x85\xca\x96\xa2`test\x8aW\xbf[\x0c'
    padded_string = pad_PCKS7(string, 20)
    print(padded_string)

if __name__ == "__main__":
	main()
