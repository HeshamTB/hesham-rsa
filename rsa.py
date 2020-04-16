#!/usr/bin/python3

#program to generate rsa key pair using methods in EE-305
# Hesham Banafa 

import math
import os
import decimal

def main():

    #Primes of size 32 bit random
    #resulting in a 64-bit key mod
    p = getPrime(32)
    print("p: ", p)
    q = getPrime(32)
    print("q: ", q)
    n = p*q
    print("n: ", n)
    print("%d bit key" % n.bit_length())

    #lamda(n) = LCM(p-1, q-1)
    #Since LCM(a,b) = ab/GCD(a,b)
    #gcd = math.gcd(p-1, q-1)
    #print("GCD: ", gcd)
    #lcm = abs((p-1) * (q-1)) / gcd
    #print("LCM: ", lcm)
    phi = (p-1)*(q-1)
    print("phi: ", phi)
    #e exponant should be 1 < e < lamda(n) and GCD(e, lamda(n)) = 1 (coprime)
    # recommended value is 65,537
    e = 65537
    d = pow(e,-1,phi)
    print("d: ", d)
    print("--------------")
    print("public key (%d, %d)" % (n,e) )

    msg_text = "Hello"
    msg_number_form = int.from_bytes(msg_text.encode(),"little")
    print("Message: %s or %d" % (msg_text, msg_number_form))

    msg_encrypted_number_form = pow(msg_number_form, e, n)
    print("Encrypted msg: ", msg_encrypted_number_form)
    msg_decrypted_number_form = pow(msg_encrypted_number_form, d, n)
    print("Decrypted msg: ", msg_decrypted_number_form)

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


if __name__ == "__main__":
    main()