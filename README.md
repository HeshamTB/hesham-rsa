
# hesham-rsa
A simple program written in python to implement RSA public encryption. Used as Course EE-305 project KAU.
# Installation 
There is no packaging or installation. Works in current dir (portable) for now.

    git clone https://apollo-server.ddns.net/gitea/Hesham/hesham-rsa.git
    cd hesham-rsa

# Usage

    ./rsa.py [COMMAND] [ARGS]
   or 
   
    python rsa.py [COMMAND] [ARGS]

## generating keys
to generate a key pair with and ID 

    ./rsa.py gen [keysize] [keyID]
All generated keys are saved in {$working_dir}/saves/
## encrypting 

    ./rsa.py encrypt "[message]" [RecieverKeyID] [SenderSignetureKeyID]
## decrypting
Assuming the encrypted message is encrypted to myPrivateKey
    
    ./rsa.py decrypt "[cipher]" [myPrivateKeyID]
The signature is checked with all public keys stored in keys directory