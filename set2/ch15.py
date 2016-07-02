def isValid_PKCS7(s):
    pad_len = s[-1]

    for i in range(1,pad_len):
        if s[-1-i] != pad_len:
            return False

    return True

def main():
    tests = [
        b"ICE ICE BABY\x04\x04\x04\x04",
        b"ICE ICE BABY\x05\x05\x05\x05",
        b"ICE ICE BABY\x01\x02\x03\x04"
    ]

    for idx, test in enumerate(tests):
        print("testing case %d:" % (idx))
        if isValid_PKCS7(test):
            print("    Valid padding.")
        else:
            # Already tested all cases indivdually.
            raise ValueError("Invalid Padding.")

if __name__ == "__main__":
    main()
