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

    if sys.argv[1] == "gen": ##rsa gen <keysize> <keyname>
        keyFileName = sys.argv[3]
        key = generateKeys(keyFileName, int(sys.argv[2]))
        printKey(key)
        try:
            saveKeyFile(key, keyFileName)
        except IOError:
            print("could not write file")
            exit(1)
        except Exception as ex:
            print(ex)
            exit(1)
    if len(sys.argv) == 5 or len(sys.argv) == 4:
        if sys.argv[1] == "encrypt": ##rsa encrypt <message> <key> <signer>
            msg = sys.argv[2]
            msg_list = msg.split()
            keyName = sys.argv[3]
            signing_key_name = sys.argv[4]
            key = readKeyFile(keyName)
            signing_key = readKeyFile(signing_key_name)
            key_public = (key[N], key[E])
            msg_encrypted = ""
            for word in msg_list:
                msg_encrypted = msg_encrypted + " " + str(encrypt(word, key_public))
            #msg_encrypted = encrypt(msg, key_public)
            print("Encrypted msg: \n", msg_encrypted)
            print("Signed: \n", sign(msg_encrypted, signing_key))
        if sys.argv[1] == "decrypt": ##rsa decrypt <cipher> <key>
            cipher = sys.argv[2]
            cipher_list = cipher.split()
            sig = verify(cipher_list)
            del cipher_list[-1]
            msg_decrypted = ""
            key = readKeyFile(sys.argv[3])
            for cipher_word in cipher_list:
                msg_decrypted = msg_decrypted + " " + str(decrypt(int(cipher_word),key[D],key[N]))
            #with open(fileName, "r") as cipherFile:
            #    cipher = int(cipherFile.readline()) ##one line may make problems later with padding
            print("Signed by: ", sig)
            print("Decrypted message: \n", msg_decrypted)
    if sys.argv[1] == "list":
        listKeys()



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
    d = pow(e,-1,phi)
    return (n, e, d, p, q, phi, id)

def encrypt(message, publicKey):
    msg_text = message
    n = publicKey[N]
    e = publicKey[E]
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

def sign(encrypted_msg, key):
    enc_msg = str(encrypted_msg)
    encrypted_msg_list = enc_msg.split()
    enc_sig = encrypt("sig:"+key[ID], (key[N], key[D]))
    encrypted_msg_list.append(enc_sig)
    signed_msg = ""
    for word in encrypted_msg_list:
        signed_msg = str(signed_msg) + " " + str(word)
    return signed_msg.strip()

def verify(cipher_list):
    sig = "Unknown"
    local_keys = os.listdir(keysFolder)
    cipher_list.reverse() #To get last word using index 0
    encrypted_sig = cipher_list[0]
    cipher_list.reverse()
    for key_name in local_keys:
        key = readKeyFile(key_name)
        print("Found key: ", key_name)
        sig = str(decrypt(int(encrypted_sig), key[E], key[N]))
        if "sig:" in sig:
            return sig.replace("sig:","")

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
            keyFile.write(hex(key[entry])+"\n")
        keyFile.write(key[ID]+"\n")

def printKey(key):
    n = key[N]
    e = key[E]
    d = key[D]
    print("----------------------------------------------"+
        "\nID: {}".format(key[ID]) +
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
    print(local_keys)
    if len(local_keys) == 0:
        return
    print("ID      PRIVATE")
    print("________________")
    for keyName in local_keys:
        key = readKeyFile(keyName)
        if key[D] == 0:
            check = u''
        else: check = u'\u2713'
        print("{}   {}\n".format(key[ID], check))


if __name__ == "__main__":
    main()