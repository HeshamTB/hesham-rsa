#!/usr/bin/python3

#program to generate rsa key pair using methods in EE-305
# Hesham Banafa 

import math
import os
import sys

def main():
    
    if sys.argv[1] == "gen" and len(sys.argv) == 3:
        n ,e ,d = generateKeys()
        key = (n, e, d)
        keyFileName = sys.argv[2]
        try:
            saveKeyFile(key, keyFileName)
        except IOError:
            print("could not write file")
            exit(1)
        except Exception as ex:
            print(ex)
            exit(1)
    if sys.argv[1] == "encrypt" and len(sys.argv) == 4:
        msg = sys.argv[2]
        keyName = sys.argv[3]
        key = readKeyFile(keyName)
        key_public = (key[0], key[1])
        msg_encrypted = encrypt(msg, key_public)

def generateKeys(bits=64):
    #Primes of size 32 bit random
    #resulting in a 64-bit key mod
    p = getPrime(int(bits/2))
    q = getPrime(int(bits/2))
    n = p*q
    #print("n: ", n)
    print("%d bit key" % n.bit_length())

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
    #print("d: ", d)
    print("---------------------------------")
    print("public key (%d, %d)" % (n,e))
    return n, e, d

def encrypt(message, publicKey):
    return None

def decrypt(cipher, privateKey, n):
    pass

def getPrime(bits):
    while True:
        #Byte order "little" or "big" does not matter here since we want a random number from os.urandom()
        x = int.from_bytes(os.urandom(int(bits/8)),"little")
        if isPrime(x):
            return x


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
    for D in range(2, K):
        if D % 2 == 0:
            pass
        else:
            if number % D == 0 or number % 5 == 0:
                return False
    return True

def readKeyFile(keyName):
    key = tuple()
    with open(keyName, "r") as keyFile:
        tempkey = keyFile.readlines()
        key = (int(tempkey[0].strip()), int(tempkey[1].strip()), int(tempkey[2].strip()))
    return key
    

def saveKeyFile(key, fileName):
    with open(fileName, "w") as keyFile:
        keyFile.write("{0}\n{1}\n{2}\n".format(key[0], key[1], key[2]))

if __name__ == "__main__":
    main()