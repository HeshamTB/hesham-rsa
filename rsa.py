#!/usr/bin/python3

#program to generate rsa key pair using methods in EE-305
# Hesham Banafa 

"""
Large Prime check: https://www.alpertron.com.ar/ECM.HTM
To crack a key, find p or q through n. (prime factorazation)
Another way to find p or q from the private key:
https://crypto.stackexchange.com/questions/13113/how-can-i-find-the-prime-numbers-used-in-rsa
"""

import math
import os
import sys
import MillerRabin as mr

VERSION="1.2.2"
keysFolder = "keys/"
byteOrder = "little"
N=0
E=1
D=2
P=3
Q=4
PHI=5
ID=6

def main():
    print("hesham-rsa version ", VERSION)
    if sys.argv[1] == "gen" and len(sys.argv) == 4: ##rsa gen <keysize> <keyname>
        keyFileName = sys.argv[3]
        if keyExist(keyFileName):
            choice = input("overwrite key %s (y/n)" % keyFileName)
            if choice == "y":
                key = generateKeys(keyFileName, int(sys.argv[2]))
            elif choice == "n":
                sys.exit(0)
            else:
                print("unrecognized choice!")
                sys.exit(1)
        else:
            key = generateKeys(keyFileName, int(sys.argv[2]))
        print("e: ", key[E])
        print("n: ", key[N])
        print("d: ", key[D])
        printKey(key)
        try:
            saveKeyFile(key, keyFileName)
        except IOError:
            print("could not write file")
            sys.exit(1)
        except Exception as ex:
            print(ex)
            sys.exit(1)
        sys.exit(0)
    if sys.argv[1] == "encrypt" and len(sys.argv) == 5: ##rsa encrypt <message> <key> <signer>
        msg = sys.argv[2]
        msg_list = msg.split()
        keyName = sys.argv[3]
        signing_key_name = sys.argv[4]
        key = readKeyFile(keyName)
        signing_key = readKeyFile(signing_key_name)
        key_public = (key[N], key[E])
        msg_encrypted = ""
        for word in msg_list:
            msg_encrypted = msg_encrypted + " " + hex(encrypt(word, key_public))
        #msg_encrypted = encrypt(msg, key_public)
        print("Encrypted msg: \n", msg_encrypted)
        print("Signed: \n", sign(msg_encrypted, signing_key)) ## Adds an encrypted sig at the end of message.
        sys.exit(0)
    elif sys.argv[1] == "encrypt":
        print("Not enough arguments")
        print("rsa encrypt <message> <key> <signer>")
        sys.exit(1)
    if sys.argv[1] == "decrypt" and len(sys.argv) == 4: ##rsa decrypt "<cipher>" <key>
        cipher = sys.argv[2]
        cipher_list = cipher.split()
        sig = verify(cipher_list)
        del cipher_list[-1]
        msg_decrypted = ""
        key = readKeyFile(sys.argv[3])
        for cipher_word in cipher_list:
            msg_decrypted = msg_decrypted + " " + str(decrypt(int(cipher_word, 16),key[D],key[N]))
        if sig == None:
            print("\033[91mUnknown signature! \u2717" + "\033[0m")
        else:
            print("Signed by: \033[92m " + sig + " \u2713\033[0m")
        print("Decrypted message: \n", msg_decrypted)
        sys.exit(0)
    elif sys.argv[1] == "decrypt":
        print("Not enough arguments")
        print("rsa decrypt \"<cipher>\" <keyid>")
        sys.exit(1)
    if sys.argv[1] == "list":
        listKeys()
        sys.exit(0)
    if sys.argv[1] == "export" and len(sys.argv) == 3: #rsa export <key>
        key_file_name = sys.argv[2]
        exportKey(key_file_name)
        sys.exit(0)
    elif sys.argv[1] == "export":
        printHelp()
        sys.exit(1)
    if sys.argv[1] == "crack" and len(sys.argv) == 3: #rsa crack <key>
        keyName = sys.argv[2]
        cracked_key = crackKey2(keyName)
        printKey(cracked_key)
        sys.exit(0)
    elif sys.argv[1] == "crack":
        printHelp()
        sys.exit(1)
    if sys.argv[1] == "print" and len(sys.argv) == 3: #rsa print <key>
        printKey(readKeyFile(sys.argv[2]))
        sys.exit(0)
    elif sys.argv[1] == "print":
        printHelp()
        sys.exit(1)
    if sys.argv[1] == "help":
        printHelp()
        sys.exit(0)

    #No command exit code
    printHelp()
    sys.exit(127)



def generateKeys(id, bits=64):
    from multiprocessing.pool import Pool
    #Primes of size 32 bit random
    #resulting in a 64-bit key mod
    pool = Pool()
    result1 = pool.apply_async(getPrime, [int(bits/2)])
    result2 = pool.apply_async(getPrime, [int(bits/2)])
    p = result1.get()
    q = result2.get()
    n = p*q
    #print("n: ", n)

    #lamda(n) = LCM(p-1, q-1)
    #Since LCM(a,b) = ab/GCD(a,b)
    #gcd = math.gcd(p-1, q-1)
    #print("GCD: ", gcd)
    #lcm = abs((p-1) * (q-1)) / gcd
    #print("LCM: ", lcm)
    phi = (p-1)*(q-1)
    #print("phi: ", phi)
    #e exponant should be 1 < e < lamda(n) and GCD(e, lamda(n)) = 1 (coprime)
    # recommended value is 65,537
    e = 65537
    d = pow(e,-1,phi) # d = e^-1 mod phi
    return (n, e, d, p, q, phi, id)

def encrypt(message, publicKey):
    msg_text = message
    n = publicKey[N]
    e = publicKey[E]
    #print("using n: {0}, e: {1}".format(n, e))

    msg_number_form = int.from_bytes(msg_text.encode(), byteOrder)
    #print("Word: %s or %d" % (msg_text, msg_number_form))

    msg_encrypted_number_form = pow(msg_number_form, e, n) # c = msg^e mod n
    return msg_encrypted_number_form

def decrypt(cipher, privateKey, n):
    msg_encrypted_number_form = cipher
    d = privateKey
    msg_decrypted_number_form = pow(msg_encrypted_number_form, d, n) # msg = c^d mod n
    msg_decrypted = int(msg_decrypted_number_form)
    try:
        msg_decrypted = str(msg_decrypted.to_bytes(msg_decrypted.bit_length(), byteOrder).decode()).strip()
    except UnicodeDecodeError:
        #print("decrypt: Cant decrypt properly")
        return ""
    return msg_decrypted

def getPrime(bits):
    while True:
        #Byte order "little" or "big" does not matter here since we want a random number from os.urandom()
        x = int.from_bytes(os.urandom(int(bits/8)), byteOrder)
        print(x, end="")
        if mr.is_prime(x):
            print("\nprime: ", x)
            return x
        backTrack(x)


def isPrime(number):
    if number == 2:
        return True

    #if 2 devides number then num is not prime. pg.21
    if number % 2 == 0 or number == 1:
        return False

    #largest integer less than or equal square root of number (K)
    rootOfNum = math.sqrt(number)
    K = math.floor(rootOfNum)

    #Take odd D such that 1 < D <= K
    #If D devides number then number is not prime. otherwise prime.
    for D in range(1, K, 2):
        if D % 2 == 0 or D == 1:
            pass
        else:
            if number % D == 0 or number % 5 == 0:
                return False
    return True

def sign(encrypted_msg, key):
    enc_msg = str(encrypted_msg)
    encrypted_msg_list = enc_msg.split()
    enc_sig = encrypt("sig:"+key[ID], (key[N], key[D]))
    encrypted_msg_list.append(hex(enc_sig))
    signed_msg = ""
    for word in encrypted_msg_list:
        signed_msg = str(signed_msg) + " " + str(word)
    return signed_msg.strip()

def verify(cipher_list):
    local_keys = os.listdir(keysFolder)
    cipher_list.reverse() #To get last word using index 0
    encrypted_sig = cipher_list[0]
    cipher_list.reverse()
    sig = None
    for key_name in local_keys:
        key = readKeyFile(key_name)
        print("Found key: ", key_name)
        sig = str(decrypt(int(encrypted_sig, 16), key[E], key[N]))
        if "sig:" in sig:
            return sig.replace("sig:","")
        else: continue
    else: return None

def readKeyFile(keyName):
    key = tuple()
    with open(keysFolder+keyName, "r") as keyFile:
        tempkey = keyFile.readlines()
        if len(tempkey) == 3: #means it only public part (n, e, id)
            key = (int(tempkey[N].strip(), 16), int(tempkey[E].strip(), 16), 0, 0, 0, 0, tempkey[2])
        else:                 #Make this a loop from 0 to 5
            key = (int(tempkey[N].strip(), 16),
            int(tempkey[E].strip(), 16),
            int(tempkey[D].strip(), 16),
            int(tempkey[P].strip(), 16),
            int(tempkey[Q].strip(), 16),
            int(tempkey[PHI].strip(), 16),
            str(tempkey[ID].strip()))
    return key


def saveKeyFile(key, fileName):
    if not os.path.isdir(keysFolder):
        os.makedirs(keysFolder)
    with open(keysFolder+fileName, "w") as keyFile:
        for entry in range(0, 6):
            if key[entry] != 0:
                keyFile.write(hex(key[entry])+"\n")
            else:
                pass
        keyFile.write(key[ID]+"\n")

def printKey(key):
    n = key[N]
    e = key[E]
    d = key[D]
    id = key[ID]
    print("----------------------------------------------"+
        "\nID: {}".format(id) +
        "\n{}-BIT KEY".format(n.bit_length())+
        "\nPUBLIC PART:"+
        "\n{0}/{1}".format(hex(n), hex(e))+
        "\nPTIVATE PART:"+
        "\n{0}".format(hex(d))+
        "\n----------------------------------------------",
    )

def listKeys():
    if not os.path.isdir(keysFolder):
        os.makedirs(keysFolder)
    local_keys = os.listdir(keysFolder)
    if len(local_keys) == 0:
        print("Cant find local keys.")
        return
    print("ID      PRIVATE      SIZE")
    print("-------------------------")
    for keyName in local_keys:
        key = readKeyFile(keyName)
        if key[D] == 0:
            check = "".strip()
        else: check = '\u2713'
        print("%7s%7s%7s-bit" % (key[ID].strip(), check, key[N].bit_length()))

def exportKey(keyFileName):
    key = readKeyFile(keyFileName)
    public_key = (key[N], key[E], 0, 0, 0, 0, key[ID])
    saveKeyFile(public_key, key[ID]+"-public")
    print("Saved public form of key {} in keys folder".format(key[ID]))

def crackKey(keyName):
    print("in crack")
    key = readKeyFile(keyName)
    n = key[N]
    for number in range(7, n - 1):
        if mr.is_prime(number):
            print("Trying prime: ", number, end="\r")
            # if number devides n then it p or q
            if n % number == 0:
                p = number
                q = int(n/p)
                phi = (p-1)*(q-1)
                e = 65537
                d = pow(e,-1,phi)
                key_cracked = (n, e, d, p, q, phi, str(keyName+"-cracked"))
                return key_cracked
            else: pass
        else: pass

def crackKey2(keyName):
    print("in crack")
    key = readKeyFile(keyName)
    n = key[N]
    print("n: ", n)
    bits = int(n.bit_length()/2)
    print("bits: ", bits)
    while True:
        number = int.from_bytes(os.urandom(int(bits/8)), byteOrder)
        if number == 0 or number == 1: continue
        print("Trying prime: ", number, end="\r")
        # if number devides n then it p or q
        if n % number == 0:
            print("\nFound a factor")
            p = number
            print("p: ", p)
            q = int(n/p)
            phi = (p-1)*(q-1)
            if phi == 0: continue
            e = 65537
            d = pow(e,-1,phi)
            key_cracked = (n, e, d, p, q, phi, str(keyName+"-cracked"))
            print(key_cracked)
            return key_cracked
        else: continue

def printHelp():
    print("commands:")
    print("rsa gen <keysize> <keyname>")
    print("rsa encrypt <message> <key> <signer>")
    print("rsa decrypt \"<cipher>\" <key>")
    print("rsa export <key>")
    print("rsa crack <key>")
    print("rsa print <key>")
    print("rsa list")

def backTrack(x):
    #Back track and clear terminal with length of x
    length = len(str(x))
    while length > 0:
        print("\b",end="")
        length -= 1

def keyExist(keyName):
    exist = os.path.exists(keysFolder+keyName)
    return exist
if __name__ == "__main__":
    main()
