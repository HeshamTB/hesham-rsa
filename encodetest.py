

s = 'test message hello awdawdaefe'
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

key = en.readKeyFile('key')
enc_list = list()
pub_key = (key[0],key[1])
for word in msg_list:
    enc_list.append(en.encrypt(word,pub_key))
print(enc_list)

unenc_list = list()

for enc_word in enc_list:
    unenc_list.append(en.decrypt(enc_word,key[2],key[0]).strip(('\x00')))
print(unenc_list)