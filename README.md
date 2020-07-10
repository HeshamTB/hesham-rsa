
# hesham-rsa (hrsa)
A simple program written in python to implement RSA public encryption. Used as Course EE-305 project.
# Installation 
There is no packaging or installation. Works in current dir (portable) for now.
# Usage

    ./hrsa
   or 
   
    python hrsa

## generating keys
to generate a key pair with and ID 

    ./hrsa [keysize] [keyID]
All generated keys are {working dir}/saves/ in keys folder
## encrypting 

    ./hrsa encrypt "[message]" [RecieverKeyID] [SenderSignetureKeyID]

