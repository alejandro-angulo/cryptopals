from operator import itemgetter
import binascii
import ch3

def main():
	fname = '4.txt'
	fh = open(fname, 'r')
	results = []

	for line in fh:
		if line[-1] == '\n':
			line = line[:-1]

		decoded = binascii.unhexlify(line)
		results.append( ch3.crack_singleByteXOR(decoded) )

	print( max(results, key=itemgetter(1)) )

if __name__ == "__main__":
	main()