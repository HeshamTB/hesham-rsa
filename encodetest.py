#!/usr/bin/python3

s = 'test message hello awdawd'
print(s)
s_number = int.from_bytes(s.encode('utf-8'),'little')
print(s_number)

ss = str(s_number.to_bytes(s_number.bit_length(),'little').decode('utf-8')).strip()
print(ss)

msg_list = list()

for word in s.split():
    msg_list.append(word)
print(msg_list)

import rsa as en

key = en.generateKeys("temp")
enc_list = list()
pub_key = (key[0],key[1])
for word in msg_list:
    enc_list.append(en.encrypt(word,pub_key))
print(enc_list)

unenc_list = list()

for enc_word in enc_list:
    unenc_list.append(str(en.decrypt(enc_word,key[2],key[0])).strip(('\x00')))
print(unenc_list)

sig = "hesham"
n = key[en.N]
e = key[en.D] #encrypt with private key
d = key[en.E]
sig_enc = en.encrypt(sig,(n,e))
print(sig_enc)
sig_un = en.decrypt(sig_enc,d,n)
print(sig_un)
print(key)

import OAEP

key = en.generateKeys("encode-test", 2048)
x = int(en.encrypt("test message int to octet string and int to octet string.", (key[en.N], key[en.E])))
print(x)
encoded_msg = OAEP.i2osp(x, key[en.N].bit_length())
print(encoded_msg)
char_encoded_message = str()
for num in encoded_msg:
    char_encoded_message += chr(num)
print(char_encoded_message)
decoded = list()
for char in char_encoded_message:
    decoded.append(int(ord(char)))
#print(decoded)
os2i = OAEP.os2ip(decoded)
#print(os2i)
print(en.decrypt(os2i, key[en.D], key[en.N]))


#decoded = OAEP.os2ip(encoded_msg)
#print(decoded)
