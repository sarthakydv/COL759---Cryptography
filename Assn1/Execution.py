from Functions import *

# Execution
# Part 0 - Read Cipher Text
n = input("Number of Test Cases: ")
for i in range(int(n)):
    path = "tests/test" + str(i + 1)
    prt = "Running Test Case " + str(i + 1)
    print(prt.center(100, "*"))
    f = open(path, "r")
    Str = f.read()

    #   Part 1 - Kasiski Method
    #   Executing Kasiski Method
    frequencies = countOcc(Str)
    possibleKeyLengths = [i[0] for i in frequencies if i[0] != 2]
    print("Kasiski Method:")
    print("Most probable key lengths are:")
    print(possibleKeyLengths[0:20])
    print()

    # Part 2 - Index of Coincidence

    #   Finding Key Length after verification by IoC
    keyLength = findKeyLength(Str, possibleKeyLengths)
    #   print(keyLength)
    #   Checking for a shorter key
    keyLength = findOptimalKeyLength(Str, keyLength)
    print("Index of Coincidence:")
    print("Key Length is " + str(keyLength))
    print()

    # Part 3 - Mutual Index of Coincidence

    #   Finding the key using MiC with the actual distribution in the English Languare
    print("Mutual Index of Coincidence:\n")
    key = findKey(Str, keyLength)
    print("The most probable key is:" + key + "\n")
    print("Deciphered text is:")
    print(decipher(Str, key))
    solved = input("Did we get the right key? (Y/N)\n").upper()
    if solved != "Y":
        change = input("Do you want to change the key length? (Y/N)").upper()
        if change == "Y":
            keyLength = int(input("Enter expected key length: "))
        nKeys = int(input("How many best choice chars for given key length?"))
        topKEach(Str, keyLength, nKeys)
    while solved != "Y":
        keyCustom = (input("Enter custom key: ")).upper()
        print("Deciphered text is:")
        print(decipher(Str, keyCustom))
        solved = input("Did we get the right key? (Y/N)\n").upper()