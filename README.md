
# hesham-rsa
A simple program written in python to implement RSA public encryption. Used as Course EE-305 project KAU.
# Installation 
There is no packaging or installation. Works in current dir (portable) for now.

    git clone https://apollo-server.ddns.net/gitea/Hesham/hesham-rsa.git

# Usage

    ./rsa.py [COMMAND] [ARGS]
   or 
   
    python rsa.py

## generating keys
to generate a key pair with and ID 

    ./rsa.py gen [keysize] [keyID]
All generated keys are {working dir}/saves/ in keys folder
## encrypting 

    ./rsa.py encrypt "[message]" [RecieverKeyID] [SenderSignetureKeyID]
