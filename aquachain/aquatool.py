#!/usr/bin/env python3

import os

from aquachain.bip44 import HDPrivateKey
from web3 import Web3
from mnemonic import Mnemonic

import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger('AQUA')

class AquaTool(object):
    def __init__(self, rpchost='', ipcpath=''):
        if ipcpath != '':
            log.info("using ipc: %s", ipcpath)
            self.provider = Web3.IPCProvider(os.path.expanduser(ipcpath))
        elif rpchost != '':
            log.info("using httprpc: %s", rpchost)
            self.provider = Web3.HTTPProvider(rpchost)
        else:
            raise Exception("need either ipc or http")

        self.w3 = Web3(self.provider)

    # Result returns the RPC response (or empty string), and logs any errors
    def Result(self, method, params):
        j = {}
        try: j = self.provider.make_request(method, params)
        except Exception:
            raise
        if 'error' in j:
            log.error("error: %s", j['error']['message'])
            return Exception(j['error']['message'])
        if 'result' in j:
            return j['result']
        raise Exception("unknown response")
    def setrpc(self, host):
        self.rpchost = host
        log.debug("new rpchost: %s", host)

    def getrpc(self):
        return self.rpchost

    def to_wei(self, amount, denom='ether'):
        return self.w3.toWei(amount, denom)

    def from_wei(self, amount, denom='ether'):
        return self.w3.fromWei(amount, denom)

    def to_hex(self, anything):
        return self.w3.toHex(anything)

    def from_hex(self, s):
        return self.w3.toAscii(s)

    def from_hex_i(self, i):
        return self.w3.toDecimal(i)
    #
    # key stuff

    def generate_key(self):
        return self.w3.sha3(os.urandom(4096))

    def generate_seed(self):
        return os.urandom(128 // 8)

    def generate_phrase(self):
        return self.seed_to_mnemonic(self.generate_seed())

    def seed_to_mnemonic(self, data):
        return Mnemonic('english').to_mnemonic(data)

    def seed_from_mnemonic(self, words, password=''):
        return Mnemonic('english').to_seed(words, password)

    def key_from_seed(self, seed):
        return HDPrivateKey.master_key_from_seed(seed)

    def key_from_mnemonic(self, words, password=''):
        return HDPrivateKey.master_key_from_mnemonic(words, password)

    def create_wallet(self, private_key, password=""):
        return self.w3.personal.importRawKey(self, private_key, password)

    def sign_tx(self, private, tx):
        signed = self.w3.eth.account.signTransaction(tx, private)
        log.debug("signed tx: %s", signed)
        return signed.rawTransaction

    def get_nonce(self, acct, fromblock='pending'):
        nonce = self.Result("aqua_getTransactionCount",
                              [acct, fromblock])
        if nonce == '':
            return 0
        return int(nonce, 16)

    def send_raw_tx(self, rawtx):
        log.info("tryingf to send this tx: %s", rawtx)
        return self.Result("aqua_sendRawTransaction", [self.w3.toHex(rawtx)])

    # block stuff
    def gethead(self):
        log.debug("getting head block")
        return self.Result("aqua_getBlockByNumber",
                          ["latest", True])

    def gethead_header(self):
        log.debug("getting head header")
        return self.Result("aqua_getBlockByNumber",
                          ["latest", False])

    def getblock(self, number):
        if number == 'latest':
            return self.gethead()
        log.debug("getting block %s", number)
        return self.Result("aqua_getBlockByNumber",
                          [str(hex(number)), True])

    def getblockbyhash(self, hash):
        log.debug("getting block %s", hash)
        return self.Result("aqua_getBlockByHash", [hash, True])

    def getheader(self, number):
        log.debug("getting block %s", number)
        return self.Result("aqua_getBlockByNumber",
                          [str(hex(number)), False])

    def getheaderbyhash(self, hash):
        log.debug("getting block %s", hash)
        return self.Result("aqua_getBlockByHash", [hash, False])

    # tx
    #
    def gettransaction(self, hash):
        log.debug("getting tx %s", hash)
        return self.Result("aqua_getTransactionByHash", [hash])

    def sendtx(self, tx):
        log.debug("sending tx %s", tx)
        return self.Result("aqua_sendTransaction", [tx])

    # account
    #
    def getbalance(self, account):
        log.debug("getting balance %s", account)
        result = self.Result("aqua_balance", [account, "latest"])
        if result is Exception:
            log.error("getbalance %s", result)
            return 0.00
        if result == '':
            return 0.00
        return float(result)

    def getaccounts(self):
        log.debug("getting accounts list")
        try :
            accounts = self.Result("aqua_accounts", [""])
            return accounts
        except Exception as e:
            log.error("error getting accounts: %s", e)
            return []

if __name__ == '__main__':
    block = AquaTool(rpchost='https://c.onical.org').getblock('latest')
    log.info("Current block: %s", block)
