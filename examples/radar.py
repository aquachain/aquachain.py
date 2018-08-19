#!/usr/bin/env python3.6
import time

WAIT_SECONDS=5

args = []


def handle_args():
    import sys
    return sys.argv

from aquachain.aquatool import AquaTool

def format_tx(t):
	s = ""
	s += "["+t['hash'] + "]" + '\n'
	s += "from   :"+t['from'] + '\n'
	s += "to     :"+t['to'] + '\n'
	if t['input'] != '0x':
		s += "data: "+t['input'] + '\n'
	s += "amount :"+str(int(t['value'],16)/1e18) + '\n'
	return s

def from_hex(i=0):
    return int(i, 16)

class System:
    def __init__(self, *kwargs):
        self.aqua = AquaTool(ipcpath='~/.aquachain/aquachain.ipc')
        #self.aqua = AquaTool(ipcpath='~/.aquachain/testnet/aquachain.ipc')
        # self.aqua = AquaTool(rpchost='https://c.onical.org')

    def run(self):
        txpool = self.aqua.w3.txpool
        print('pending', from_hex(txpool.status.pending))
        for tx in self.aqua.gethead()['transactions']:
          print(format_tx(tx))
        print('queued', from_hex(txpool.status.queued))
        new_block_filter = self.aqua.w3.eth.filter('latest')
        new_transaction_filter = self.aqua.w3.eth.filter('pending')
        while True:
            txs = new_transaction_filter.get_new_entries()
            if len(txs) > 0:
                print('\n')
                for tx in txs:
                    tx_hash = tx.hex()
                    t = self.aqua.gettransaction(f'{tx_hash}')
                    print("\nnew tx:", tx_hash,'\n\n', format_tx(t) ,'\n')

            newblock = new_block_filter.get_new_entries()
            if len(newblock) > 0:
                print('\n')
                print('newblock', newblock)
                for i in range(len(newblock)):
                    block = self.aqua.getblockbyhash(newblock[i].hex())
                    print(from_hex(block['number']), block)
            time.sleep(WAIT_SECONDS)
            print('.', end='', flush=True)

if __name__ == '__main__':
    System().run()
