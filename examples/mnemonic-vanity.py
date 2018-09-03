from aquachain.aquatool import AquaTool
from aquachain.aquakeys import Keystore
passphrase = ''
vanity = '0xaa'

keystore = Keystore(directory='myaquakeys')
aqua = AquaTool(ipcpath="~/.aquachain/aquachain.ipc")

print("Looking for", vanity, "saving to", keystore.directory)

#keys = keystore.listphrases()
#for keyphrase in keys:
#    key = aqua.key_from_mnemonic(keyphrase, passphrase)
#    address = key._key.public_key.address()
#    print(address, keyphrase)
count = 0
while True:
    if count % 1000 == 0:
        print('.')
        count = 0
    count = count + 1
    phrase = aqua.generate_phrase()
    key = aqua.key_from_mnemonic(phrase, passphrase)
    address = key._key.public_key.address()
    if vanity in address:
        print(key._key.public_key.address(), phrase)
        keystore.save_phrase(phrase)
        break
