import requests
import time
import base64
from ecdsa import SigningKey, NIST384p
import json

def wallet():
    entry = None
    while input not in ['a','b','c','d']:
        entry = input(""" 
        a. Generate a new wallet
        b. Trasfer Coins
        c. View Coins
        d. Quit\n""")
    if entry == 'a':
        generate_ECDSA_keys()

    elif entry == 'b':
        sender_public = input("Please enter yours wallet's Public key: ")
        sender_private = input("Please enter your private key: ")
        rec_public = input("Please enter the destination public key: ")
        amount = input("Enter number of coins to be transferred: ")
        print("Please verify the detials below and choose [y,n] to proceed\n")
        print(F"From: {sender_public}\nPrivate Key: {sender_private}\nTo: {rec_public}\nAmount: {amount}\n")
        entry = input()
        if entry.lower() == 'y':
            send_transaction(sender_public, sender_private, rec_public, amount)
        elif entry.lower() == 'n':
            return wallet()

    elif entry == 'c':
        verify_transactions()

    else:
        quit()

def generate_ECDSA_keys():
    sk = SigningKey.generate(curve=NIST384p) #private key generation 
    private_key = sk.to_string().hex() #private key conversion to hex
    vk = sk.get_verifying_key() #public key
    public_key = vk.to_string().hex() #converting public key to hex
    public_key = base64.b64encode(bytes.fromhex(public_key)) #shortened public key

    #saving wallet credentials
    filename = input("Write the name of your new address: ") + ".txt"
    with open(filename, "w") as f:
        f.write(F"Private key: {private_key}\nWallet address / Public key: {public_key.decode()}")
    print(F"Your new address and private key are now in the file {filename}")

def send_transaction(addr_from, private_key, addr_to, amount):
    if len(private_key) == 64:
        signature, message = sign_ECDSA_msg(private_key)
        payload = {"from": addr_from,
                   "to": addr_to,
                   "amount": amount,
                   "signature": signature.decode(),
                   "message": message}
        headers = {"Content-Type": "application/json"}

        for (miner_address, miner_url)  in get_miners().items():
            res = requests.post(miner_url + '/txion', json=payload, headers=headers)
            print(miner_address + ':', res.text)
    else:
        print("Wrong address! Please try again.")

def get_miners():
    return json.loads(requests.get('http://localhost:5000/miners').content)


def verify_transactions():
    try:
        blockchain = []
        for miner_url in get_miners().values():
            res = json.loads(requests.get(miner_url + '/blocks').content)
            if len(res) > len(blockchain):
                blockchain = res

        print("--- LEDGER ---")
        for block in blockchain:
            print(block)
        print("--------------")
    except requests.ConnectionError:
        print('Ensure that miner.py is running on another terminal.')

def sign_ECDSA_msg(private_key):
    
    message = str(round(time.time()))
    bmessage = message.encode()
    sk = SigningKey.from_string(bytes.fromhex(private_key), curve=NIST384p)
    signature = base64.b64encode(sk.sign(bmessage))
    return signature, message

if __name__ == '__main__':
    print("""    =========================================\n
          Protocoin BLOCKCHAIN SYSTEM\n
       =========================================\n\n\n""")

    while True:
        wallet()

