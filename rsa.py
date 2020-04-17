#!/usr/bin/python3

#program to generate rsa key pair using methods in EE-305
# Hesham Banafa 

#Large Prime check: https://www.alpertron.com.ar/ECM.HTM

import math
import os
import sys

keysFolder = "keys/"
byteOrder = "little"

def main():

    if sys.argv[1] == "gen": ##rsa gen <keysize> <keyname>
        n ,e ,d = generateKeys(int(sys.argv[2]))
        key = (n, e, d)
        printKey(key)
        keyFileName = sys.argv[3]
        try:
            saveKeyFile(key, keyFileName)
        except IOError:
            print("could not write file")
            exit(1)
        except Exception as ex:
            print(ex)
            exit(1)
    if len(sys.argv) == 4:
        if sys.argv[1] == "encrypt": ##rsa encrypt <message> <key>
            msg = sys.argv[2]
            msg_list = msg.split()
            keyName = sys.argv[3]
            key = readKeyFile(keyName)
            key_public = (key[0], key[1])
            msg_encrypted = ""
            for word in msg_list:
                msg_encrypted = msg_encrypted + " " + str(encrypt(word, key_public))
            #msg_encrypted = encrypt(msg, key_public)
            print("Encrypted msg: \n", msg_encrypted)
        if sys.argv[1] == "decrypt": ##rsa decrypt <cipher> <key>
            cipher = sys.argv[2]
            cipher_list = cipher.split()
            msg_decrypted = ""
            key = readKeyFile(sys.argv[3])
            for cipher_word in cipher_list:
                msg_decrypted = msg_decrypted + " " + str(decrypt(int(cipher_word),key[2],key[0]))
            #with open(fileName, "r") as cipherFile:
            #    cipher = int(cipherFile.readline()) ##one line may make problems later with padding
            print("Decrypted message: \n", msg_decrypted)




def generateKeys(bits=64):
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
    d = pow(e,-1,phi)
    return n, e, d

def encrypt(message, publicKey):
    msg_text = message
    n = publicKey[0]
    e = publicKey[1]
    print("using n: {0}, e: {1}".format(n, e))

    msg_number_form = int.from_bytes(msg_text.encode(), byteOrder)
    print("Word: %s or %d" % (msg_text, msg_number_form))

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
        print("Cant decrypt properly")
    return msg_decrypted

def getPrime(bits):
    while True:
        #Byte order "little" or "big" does not matter here since we want a random number from os.urandom()
        x = int.from_bytes(os.urandom(int(bits/8)), byteOrder)
        print("trying: ", x, end="")
        if isPrime(x):
            print("\nprime: ", x)
            return x
        print("\r",end="")


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

def readKeyFile(keyName):
    key = tuple()
    with open(keysFolder+keyName, "r") as keyFile:
        tempkey = keyFile.readlines()
        key = (int(tempkey[0].strip(), 16), int(tempkey[1].strip(), 16), int(tempkey[2].strip(), 16))
    return key
    

def saveKeyFile(key, fileName):
    if not os.path.isdir(keysFolder):
        os.makedirs(keysFolder)
    with open(keysFolder+fileName, "w") as keyFile:
        keyFile.write("{0}\n{1}\n{2}\n".format(hex(key[0]), hex(key[1]), hex(key[2])))

def printKey(key):
    n = key[0]
    e = key[1]
    d = key[2]
    print("----------------------------------------------"+
        "\n{}-BIT KEY".format(n.bit_length())+
        "\nPUBLIC PART:"+
        "\n{0}/{1}".format(hex(n), hex(e))+
        "\nPTIVATE PART:"+
        "\n{0}".format(hex(d))+
        "\n----------------------------------------------",
    )

if __name__ == "__main__":
    main()