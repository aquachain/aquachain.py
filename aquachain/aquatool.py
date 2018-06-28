#!/usr/bin/env python3

import os

from aquachain.bip44 import HDPrivateKey
from web3 import Web3
from mnemonic import Mnemonic
from eth_utils import to_checksum_address

import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

class AquaTool(object):
    '''
    AquaTool class requires one of rpchost or ipcpath to be set.
    '''
    def __init__(self, rpchost='', ipcpath=''):
        if ipcpath != '':
            log.debug("using ipc: %s", ipcpath)
            self.provider = Web3.IPCProvider(os.path.expanduser(ipcpath))
        elif rpchost != '':
            log.debug("using httprpc: %s", rpchost)
            self.provider = Web3.HTTPProvider(rpchost)
        else:
            raise Exception("need either ipc or http")
        self.w3 = Web3(self.provider)

    '''
    Result returns the RPC response of method and params it returns an exception
    '''
    def Result(self, method, params=[]):
        j = {}
        try: j = self.provider.make_request(method, params)
        except Exception as e:
            return e
        if 'error' in j:
            log.error("error: %s", j['error']['message'])
            return ValueError(j['error']['message'])
        if 'result' in j:
            return j['result']
        raise ValueError("unknown response")

    '''
    setrpc replaces current web3 instance provider with given RPC.
    use 'setipc' for IPC path.
    '''
    def setrpc(self, host):
        self.provider = Web3.IPCProvider(os.path.expanduser(ipcpath))
        self.w3 = Web3(self.provider)
        log.debug("new rpchost: %s", host)

    '''
    setipc replaces current web3 instance provider with given IPC.
    use 'setrpc' for RPC path.
    '''
    def setipc(self, host):
        self.provider = Web3.HTTPProvider(host)
        self.w3 = Web3(self.provider)
        log.debug("new ipcpath: %s", host)

    '''
    getprovider returns the web3 provider
    '''
    def getprovider(self):
        return self.provider

    '''
    to_wei turns float amount to WEI. by default from AQUA
    '''
    def to_wei(self, amount, denom='ether'):
        return self.w3.toWei(amount, denom)
    '''

    from_wei returns a float amount from WEI. by default to AQUA
    '''
    def from_wei(self, amount, denom='ether'):
        return self.w3.fromWei(amount, denom)


    '''
    to_hex is same as w3.toHex
    '''
    def to_hex(self, anything):
        return self.w3.toHex(anything)

    '''
    from_hex is same as w3.toAscii
    '''
    def from_hex(self, s):
        return self.w3.toAscii(s)

    '''
    to_decimal is same as w3.toDecimal
    '''
    def to_decimal(self, i):
        return self.w3.toDecimal(i)

    '''
    generate_key returns sha3(os.urandom(4096))
    '''
    def generate_key(self):
        return self.w3.sha3(os.urandom(4096))

    '''
    generate_seed returns a seed used for mnemonic (default 32)
    '''
    def generate_seed(self, size=32):
        return os.urandom(size)

    '''
    generate_phrase returns a random mnemonic phrase (default 32 byte)
    '''
    def generate_phrase(self, size=32):
        return self.seed_to_mnemonic(self.generate_seed(size=size))

    '''
    seed_to_mnemonic returns a phrase given a seed
    '''
    def seed_to_mnemonic(self, data):
        return Mnemonic('english').to_mnemonic(data)

    '''
    seed_from_mnemonic returns a seed given a phrase and a password
    '''
    def seed_from_mnemonic(self, words, password=''):
        return Mnemonic('english').to_seed(words, password)

    '''
    to_wei turns float amount to WEI. by default in AQUA
    '''
    def key_from_seed(self, seed):
        return HDPrivateKey.master_key_from_seed(seed)

    '''
    key_from_mnemonic returns a hdkey given a phrase and passphrase
    '''
    def key_from_mnemonic(self, words, passphrase=''):
        return HDPrivateKey.master_key_from_mnemonic(words, passphrase)

    '''
    sign_tx signs a transaction
    '''
    def sign_tx(self, private, tx):
        if 'nonce' not in tx:
            return ValueError('tx needs nonce')
        signed = self.w3.eth.account.signTransaction(tx, private)
        log.debug("signed tx: %s", signed)
        return signed.rawTransaction

    '''
    getnonce (number of sent transactions) for an account
    fromblock default from 'pending'
    '''
    def getnonce(self, acct, fromblock='pending'):
        nonce = self.Result("aqua_getTransactionCount",
                              [acct, fromblock])
        if nonce == '':
            return 0
        return int(nonce, 16)

    '''
    send_raw_tx
    '''
    def send_raw_tx(self, rawtx):
        log.debug("trying to send this tx: %s", rawtx)
        return self.Result("aqua_sendRawTransaction", [self.w3.toHex(rawtx)])

    '''
    gethead returns latest head block
    '''
    def gethead(self):
        log.debug("getting head block")
        return self.Result("aqua_getBlockByNumber",
                          ["latest", True])

    '''
    getpendingblock returns pending block
    '''
    def getpendingblock(self):
        log.debug("getting pending block")
        return self.Result("aqua_getBlockByNumber",
                          ["pending", True])

    '''
    gethead_header returns latest head header
    '''
    def gethead_header(self):
        log.debug("getting head header")
        return self.Result("aqua_getBlockByNumber",
                          ["latest", False])

    '''
    getblock returns block by number
    '''
    def getblock(self, number):
        if number == 'latest':
            return self.gethead()
        if number == 'pending':
            return self.getpendingblock()
        log.debug("getting block %s", number)
        return self.Result("aqua_getBlockByNumber",
                          [str(hex(number)), True])

    '''
    getblockbyhash
    '''
    def getblockbyhash(self, hash):
        log.debug("getting block %s", hash)
        return self.Result("aqua_getBlockByHash", [hash, True])

    '''
    getheader
    '''
    def getheader(self, number):
        log.debug("getting block %s", number)
        return self.Result("aqua_getBlockByNumber",
                          [str(hex(number)), False])

    '''
    getheaderbyhash
    '''
    def getheaderbyhash(self, hash):
        log.debug("getting block %s", hash)
        return self.Result("aqua_getBlockByHash", [hash, False])

    '''
    gettransaction returns transaction if known
    '''
    def gettransaction(self, hash):
        log.debug("getting tx %s", hash)
        return self.Result("aqua_getTransactionByHash", [hash])

    '''
    gettransactionreceipt returns transaction receipt if mined
    '''
    def gettransactionreceipt(self, hash):
        log.debug("getting tx receipt %s", hash)
        return self.Result("aqua_getTransactionReceipt", [hash])

    '''
    sendtx sends an unsigned transaction for the web3 provider to sign and send.
    '''
    def sendtx(self, tx):
        log.debug("sending tx %s", tx)
        return self.Result("aqua_sendTransaction", [tx])

    '''
    getbalance returns the balance for a given account (in AQUA)
    option fromblock can be 'pending' or a block number
    '''
    def getbalance(self, account, fromblock='latest'):
        log.debug("getting balance %s", account)
        result = self.Result("aqua_balance", [account, fromblock])
        if result is Exception:
            log.error("getbalance %s", result)
            return 0.00
        if result == '':
            return 0.00
        return float(result)

    '''
    getaccounts returns all rpc accounts
    '''
    def getaccounts(self):
        log.debug("getting accounts list")
        try :
            accounts = self.Result("aqua_accounts", [""])
            return accounts
        except Exception as e:
            log.error("error getting accounts: %s", e)
            return []

    '''
    checksum_encode an address
    '''
    def checksum_encode(self, address):
        return to_checksum_address(address)

'''
BlockFormatter formats a block into a basic string, barely useful for logs
'''
def BlockFormatter(block, ):
    if not 'number' in block:
        return ValueError('this function requires a block with number')
    num = int(block['number'], 16)
    diff = int(block['difficulty'], 16)
    miner = block['miner']
    blockhash = block['hash']
    return f'Block {num}: {blockhash}, with {len(block["transactions"])} tx, mined by {miner}, next difficulty {diff}'


# test
if __name__ == '__main__':
    aqua = AquaTool(rpchost='https://c.onical.org')
    block = aqua.getblock('latest')
    log.info("Current block: %s\nHave a nice day! https://aquachain.github.io", BlockFormatter(block))
