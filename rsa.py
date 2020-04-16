#!/usr/bin/python3

#program to generate rsa key pair using methods in EE-305
# Hesham Banafa 

import math

def main():

    #test isPrime method
    for i in range(2,999999):
        if isPrime(i):
            print(i, 'is prime')

def getPrime(bits):
    pass

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