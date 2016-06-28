def main():
	hex1 = '1c0111001f010100061a024b53535009181c'
	hex2 = '686974207468652062756c6c277320657965'

	print( hex(int(hex1, 16) ^ int(hex2, 16)) )

if __name__ == "__main__":
	main()
