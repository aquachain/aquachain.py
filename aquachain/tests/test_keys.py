#!/usr/bin/env python3

import unittest

from aquachain.aquakeys import Keystore, HDPrivateKey
from aquachain.aquatool import AquaTool
import logging
import os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

dummymnemseed = b'G\x01\x16\\\xa4\x9f\xb1\x99\xc0E\x80U\x96<\xf8l\x9e\x06"F=\x94\x9f\xd9{\x1c\x81d\x14o\x8b\x19#\x9e-T\xa6W\xb1\xf0_\xff\xdd\xf2\x16g\xc8\xcd\xb2\x7f\x86d\x94\xdc\x92\x87\xec\x03\x91\x15cw&\x91'
# hello world
testcase1 = 'sea oval armed kid foil tuition journey initial salad' + \
            ' convince fortune filter pulse drastic evidence argue piano' + \
            ' skirt wealth dragon call blast wide hard'

testcase2b = '0x5a6772e31ea5AE3D41D21dAc90968e910523853C'
testcase2 = 'wisdom write work exercise critic ' + \
            'chair legal call truck final ' + \
            'umbrella cat foil neither tomorrow ' + \
            'human worry blossom north snack ' + \
            'infant swear reunion student'

dummykey = b'\xc1\xf3\xb4/=%\xa7\xd4^\x1b\x9f\xbeE\xf1n+:\xd8\x84\x93' + \
           b'p\\\xa4\x19W\xe0\xa1\x02\x06.\xfe\xab'

aqua = AquaTool(rpchost='https://c.onical.org')

class Test_Account(unittest.TestCase):
    # def test_fileloader(self):
    #     log.info("fileloader")
    #     private_key = aqua.file_to_private(my_key, '')
    #     self.assertNotEqual('', private_key)
    #     acct = aqua.private_to_account(private_key)
    #     self.assertNotEqual('', acct.address)
    #     log.info("got real account: %s", acct.address)
    #     signed = aqua.sign(private_key, 'hello world')
    #     log.info("Signed Helloworld: %s",
    #              signed)

    def test_nonce(self):
        n = aqua.getnonce('0x545ac449bfc7891ef1a8d2065aa2a54ba7570c45', fromblock='latest')
        log.info("found account nonce: %s", n)

    def test_mnemonic_keys(self):
        phrase = 'into curious truck notable tree forest squirrel' + \
                  ' armed shallow resist nation vessel elevator' + \
                  ' jacket beauty blanket walk zoo brush chat' + \
                  ' fence lumber put nasty'
        password = ''
        seed = aqua.seed_from_mnemonic(phrase, password)
        log.info("SEED FROM MNEMONIC: %s", seed)

    def test_mnemonic(self):
        phrase = aqua.seed_to_mnemonic(dummykey)
        log.info("NEW MNEMONIC %s", phrase)
        self.assertEqual(phrase, testcase1)

    def test_createmasterwallet(self):
        for i in range(1):
            mnem = aqua.seed_to_mnemonic(aqua.generate_seed())
            key = aqua.key_from_mnemonic(mnem)
            key1 = aqua.key_from_mnemonic(mnem, 'password')
            pub = key.public_key.address()
            pub1 = key1.public_key.address()
            private_key = key._key.to_hex()
            private_key1 = key1._key.to_hex()
            log.info('MNEMONIC: %s', mnem)
            log.info('PUBLIC KEY: %s', pub)
            log.info('PRIVATE KEY: %s', private_key)
            log.info('PUBLIC KEY1: %s', pub1)
            log.info('PRIVATE KEY1: %s', private_key1)
            self.assertNotEqual(pub, pub1)
            self.assertNotEqual(private_key, private_key1)


    def test_retrieve_master(self):
        mnem1 = 'crunch clog neck wet dress auction ball gate you enter zebra glory'
        pub1 = '0x0de55d1767dc6d5f753bb7393a35770f557b87da'
        priv1 = '739edf3d230317cbdfb6853e5dffe2255d38b80bd6068d1fa6569e51a00d9805'
        pubpass1 = '0xae4b90836a6f5727292183a6091ca2196f1c4d14'
        privpass1 = 'f8c9f7466c7538909cace97e78e71b3cd9641c63fc08a0d4f038bc88e93b6133'
        test1 = (mnem1, pub1, priv1, pubpass1, privpass1)

        mnem2 = 'rebuild absurd they lamp uncover rhythm school host ecology act debris blanket'
        pub2 = '0x0ffb9d5b1ab7f2b5089d9e9e83aaa28d138e571b'
        priv2 = '158e66b24010f4dbefd66e35d2f7d774b63fd63220c86b64894cad3ba94b7b25'
        pubpass2 = '0x448531d1466413413f6303eff3e459096ea844bf'
        privpass2 = '95796931b9bb6f412a783a8d3ea263de325f6c306fd016ea1b10248d5fc594df'
        test2 = (mnem2, pub2, priv2, pubpass2, privpass2)

        mnem3 = 'usage advice fuel increase patient chronic dinner patch boy dash annual museum'
        pub3 = '0xd969c2d24bfef77bd8e212a00cd4cd53bbc90860'
        priv3 = '99b484abfb4665b88e9ce510bdc36c3e0e214ed624084890eac2637cdc713009'
        pubpass3 = '0x48d84520a0743f99ebc194cd6e8f4d258282f455'
        privpass3 = 'f5320a130d0863e95119d392c02bd34b5e077d3897180664ed2ae263cb8f7af2'
        test3 = (mnem3, pub3, priv3, pubpass3, privpass3)

        for (phrase, pub, priv, pubpass, privpass) in {test1, test2, test3}:
            log.info("phrase: %s checking for pub %s priv %s\n pubpass %s privpass %s", phrase, pub, priv, pubpass, privpass)
            seed1 = aqua.seed_from_mnemonic(phrase, '')
            seed2 = aqua.seed_from_mnemonic(phrase, 'password')
            self.assertNotEqual(seed1, seed2)

            key1 = aqua.key_from_seed(seed1)
            key2 = aqua.key_from_seed(seed2)

            priv1 = key1._key.to_hex()
            priv2 = key2._key.to_hex()
            self.assertNotEqual(priv1, priv2)

            pub1 = key1.public_key.address()
            pub2 = key2.public_key.address()
            self.assertNotEqual(pub1, pub2)

            self.assertEqual(priv, priv1)
            self.assertEqual(pub, pub1)
            self.assertEqual(privpass, priv2)
            self.assertEqual(pubpass, pub2)

            log.info("%s == %s", pub, pub1)
            log.info("%s == %s", pubpass, pub2)

    # def test_sign(self):
    #     key = aqua.generate_key()
    #     signed = aqua.sign(key, aqua.to_hex("hello world"))
    #     log.info("signed data: %s", signed)

    def test_signtx(self):
        key = aqua.generate_key()
        transaction = {
            'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
            'value': 1000000000,
            'gas': 2000000,
            'gasPrice': 234567897654321,
            'nonce': 0,
            'chainId': 61717561,
        }
        log.info("signing tx: %s", transaction)
        signed = aqua.sign_tx(key, transaction)
        log.info("signed tx: %s", signed)



class Test_Keystore(unittest.TestCase):
    keystore = Keystore(directory='testdata')

    def test_asavekeys(self):
        for i in range(1):
            phrase = aqua.generate_phrase()
            filename = self.keystore.save_phrase(phrase)
            log.info("saved key %s", filename)

    def test_privkey(self):
        key = aqua.key_from_seed(dummymnemseed)
        pub = key.public_key.address()
        log.info('NEW PUBLIC KEY: %s', pub)
        self.assertEqual(pub, '0xdb966b140b23322f890e5ea80f5ea7284bfefb03')
        log.info('NEW PRIVATE KEY: %s', key._key.to_hex())

    def test_listphrases(self):
        log.info("listphrase test")
        keys = self.keystore.listphrases()
        self.assertFalse(len(keys) == 0)
        for key in keys:
            log.info("found phrase: %s", key)

    def test_loadkey(self):
        keys = self.keystore.listphrases()
        self.assertFalse(len(keys) == 0)
        for phrase in keys:
            log.info("[loader] %s", phrase)
            key = aqua.key_from_mnemonic(phrase, 'password')
            log.info("[loaded] %s %s",
                     key.public_key.address(), key._key.to_hex())


    def test_loadphrase(self):
        phrase = 'drum legend crowd awesome ethics cat topic grid clerk equip display cross'
        mkey = self.keystore.load_phrase(phrase, "password")
        for i in range(10):
            key = HDPrivateKey.from_parent(mkey, i)
            log.info("HD%s: %s", i, key.public_key.address())

    def test_loadphrases(self):
        phrases = Keystore(directory='.').listphrases()
        keys = self.keystore.load_phrases(phrases, "password")
        self.assertFalse(len(keys) == 0)
        for key in keys:
            log.info("loadphrases: %s", key.public_key.address())

    def test_loadfile(self):
        key_filename = os.path.join('testdata',
                                    'aqua1527314056152731405672612.wallet')
        password = 'password'
        phrase = self.keystore.readfile(key_filename)
        hdkey = self.keystore.load_phrase(phrase['poem'], password)
        pub = hdkey.public_key.address()
        log.info('Found master key: %s', pub)

        # 44/0/0
        # self.assertEqual('0x99e4c027d183aa37684a558b5804cce730456a63', pub)

        # 44/0/0/0
        self.assertEqual('0x7e362eef9425dae8b84374543c78d539869b6e3a', pub)


    def test_zd_wallets(self):
        phrases = self.keystore.listphrases()
        keys = self.keystore.load_phrases([phrases[0]], "password")
        self.assertFalse(len(keys) == 0)
        key = keys[0]
        log.info("hdwallet: %s", phrases[0])
        oldkey = ''
        for i in range(100):
            pub = key.public_key.address()
            log.info("test_hd_wallets: %s (%s)", pub, key._key.to_hex())
            key = self.keystore.from_parent_key(key, i)
            self.assertNotEqual(oldkey, key)
            oldkey = key

    def test_keystoredir(self):
        keys = self.keystore.listphrases()
        self.assertTrue(len(keys) != 0)
        ks1 = Keystore(directory='testdata2')
        keys1 = ks1.listphrases()
        self.assertTrue(len(keys1) == 0)



if __name__ == '__main__':
    unittest.main()
