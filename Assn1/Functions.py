# Functions
# Part 1 - Kasiski Method
def divisors(n):  # Finds all divisors, except 1
    divs = []
    for i in range(2, n + 1):
        if n % i == 0:
            divs.append(i)
    return divs


# Finds all repeating substrings, poplulates a list of all divisors of distances
# and returns sorted list of number of occurences in decreasing order
def countOcc(str):
    divs = []
    i = 0
    while i < len(str) - 3:
        length = 3
        found = False
        # subStr = s[i:i + length]
        # if (len(subStr) < 3):
        #     break
        j = i + 3
        while j < len(str):
            if str[i : i + length] == str[j : j + length]:
                while str[i : i + length + 1] == str[j : j + length + 1]:
                    length = length + 1
                # subStr = s[i:i + length]
                distance = j - i
                found = True
                divs.extend(divisors(distance))
                # print("%s\ti:%s\tj:%s\tdiff:%s\t\tDivisors:%s" %
                #       (subStr, i, j, diff, divisors(diff)))
            #     j = j + length
            # else:
            j = j + 1
            if found:
                break
        i = i + 1
        if found:
            i = i + length - 1
        # print(i)
    # print(count)
    d = {}
    for i in divs:
        if i in d:
            d[i] = d[i] + 1
        else:
            d[i] = 1
    final = sorted(d.items(), key=lambda x: x[1], reverse=True)
    # print(final)
    return final


# Part 2 - Index of Coincidence
# Choosing Threshold for IoC
THRESHOLD = 0.058


# Seperates ciphertext into n Caesar ciphers
def makeCaesarCipher(str, keySize):
    l = []
    for i in range(keySize):
        tmp = str[i::keySize]
        l.append(tmp)
    # print(l)
    return l


# Calculates IoC for given Caesar cipher
def IoCCalc(cipher):
    if len(cipher) < 2:
        return 0
    dict = {}
    for c in cipher:
        if c in dict:
            dict[c] += 1
        else:
            dict[c] = 1
    val = 0
    for c in dict.values():
        val = val + c * (c - 1)
    val = val / (len(cipher) * (len(cipher) - 1))
    return val


# Finds the first key length from Kasiski Method that satisfies IoC criteria
def findKeyLength(Str, possibleKeyLengths):
    for keyLength in possibleKeyLengths:
        l = makeCaesarCipher(Str, keyLength)
        IoC = 0
        for j in l:
            IoC = IoC + IoCCalc(j)
        IoC = IoC / len(l)
        # print(check)
        if IoC > THRESHOLD:
            return keyLength
            # print('here')


# def findKeyLength():
#     d = {}
#     for i in res1:
#         l = makeStrings(s, i)
#         check = 0
#         for j in l:
#             check = check + IoCCalc(j)
#         check = check / len(l)
#         d[i] = check
#     result = sorted(d.items(), key=lambda x: x[1], reverse=True)
#     print(result)


# It is possible that a multiple of keyLength is found during greedy search in
# findKeyLength(), we find the smallest possible length by taking divisors here
def findOptimalKeyLength(Str, keyLength):
    divs = divisors(keyLength)
    divs = divs[:-1]  # removing the original keyLength
    for newKeyLength in divs:
        l = makeCaesarCipher(Str, newKeyLength)
        check = 0
        for j in l:
            check = check + IoCCalc(j)
        check = check / len(l)
        # print(check)
        if check > THRESHOLD:
            return newKeyLength
    return keyLength


# Part 3 - Mutual Index of Coincidence

# Distribution of frequencies of the English alphabet
english_frequences = [
    0.08167,
    0.01492,
    0.02782,
    0.04253,
    0.12702,
    0.02228,
    0.02015,
    0.06094,
    0.06966,
    0.00153,
    0.00772,
    0.04025,
    0.02406,
    0.06749,
    0.07507,
    0.01929,
    0.00095,
    0.05987,
    0.06327,
    0.09056,
    0.02758,
    0.00978,
    0.02360,
    0.00150,
    0.01974,
    0.00074,
]
# tmp = sum(english_frequences)
# english_frequences = [i * 10000 / tmp for i in english_frequences]
# del tmp
# print(sum(english_frequences))
# print((english_frequences))


def shiftCipher(shift):
    newFreq = []
    for i in range(26):
        newFreq.append(english_frequences[(i - shift + 26) % 26])
    return newFreq


def MiCCalc(freq, shift, n):
    val = 0
    newFreq = shiftCipher(shift)
    for i in range(26):
        val += freq[i] * newFreq[i]
    val /= n
    # val = abs(val - 0.065)
    # print(val * 100)
    # print(val)
    return val


def findNext(cipher):
    dict = {}
    for c in cipher:
        if c in dict:
            dict[c] += 1
        else:
            dict[c] = 1
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for c in ALPHABET:
        if c not in dict:
            dict[c] = 0
    freq = sorted(dict.items(), key=lambda x: x[0])
    # print("this")
    # print(freq)
    freq = [i[1] for i in freq]
    # print(freq)
    shift = 0
    val = 0
    d1 = {}
    while shift < 26:
        val = MiCCalc(freq, shift, len(cipher))
        d1[shift] = val
        shift = shift + 1
    # print(len(d1))
    d1 = sorted(d1.items(), key=lambda x: x[1], reverse=True)
    # print(d1)
    return chr(ord("A") + d1[0][0])


def findKey(Str, keyLength):
    key = ""
    for cipher in makeCaesarCipher(Str, keyLength):
        key += findNext(cipher)
        # print()
    return key


def findNextK(cipher, K):
    dict = {}
    for c in cipher:
        if c in dict:
            dict[c] += 1
        else:
            dict[c] = 1
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for c in ALPHABET:
        if c not in dict:
            dict[c] = 0
    freq = sorted(dict.items(), key=lambda x: x[0])
    # print("this")
    # print(freq)
    freq = [i[1] for i in freq]
    # print(freq)
    shift = 0
    val = 0
    d1 = {}
    while shift < 26:
        val = MiCCalc(freq, shift, len(cipher))
        d1[shift] = val
        shift = shift + 1
    # print(len(d1))
    d1 = sorted(d1.items(), key=lambda x: x[1], reverse=True)
    out = []
    for i in range(K):
        out.append(chr(ord("A") + d1[i][0]))
    return out


def topKEach(Str, keyLength, K):
    key = ""
    for cipher in makeCaesarCipher(Str, keyLength):
        print(findNextK(cipher, K))
    return key


def decipher(Str, key):
    shift = []
    for i in key:
        shift.append(ord(i) - ord("A"))
    lower = ord("A")
    # print(lower)
    # print(shift)
    text = ""
    for i in range(0, len(Str), len(key)):
        for j in range(len(key)):
            if i + j < len(Str):
                ch = ord(Str[i + j]) - shift[j]
                if ch < lower:
                    ch = ch + 26
                text = text + chr(ch)
    return text