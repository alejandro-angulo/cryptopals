import binascii
import sys

def pad_PCKS7(s, length):
    pad_length = length - len(s)
    for i in range(pad_length):
        s += bytes( [pad_length] )

    return s

def main():
    string = b'YELLOW SUBMARINE'
    padded_string = pad_PCKS7(string, 20)
    print(padded_string)

if __name__ == "__main__":
	main()
