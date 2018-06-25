from aquachain.aquatool import AquaTool
from aquachain.aquakeys import Keystore
from web3.contract import ConciseContract
from aquamotd import MOTD_ABI, MOTD_ADDRESS
import os, time, random, datetime
import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def userenv(foo):
        os.os.path.expanduser(foo)

aqua = AquaTool(ipcpath=os.path.expanduser('~/.aquachain/aquachain.ipc'))
keystore = Keystore(directory=os.path.expanduser('~/.aquachain/aquakeys'))

args = []

def _handle_args():
    import sys
    return sys.argv

args = _handle_args()

def from_hex(i=0):
    return int(i, 16)

WAIT_SECONDS=5.0


class System:
    def __init__(self, *kwargs):
        self.aqua = AquaTool(ipcpath='/home/user/.aquachain/aquachain.ipc')
        #self.aqua = AquaTool(rpchost='https://c.onical.org')
        self.block = self.aqua.gethead()
        self.headnumber = int(self.block['number'], 16)
        self.motd_contract = self.aqua.w3.eth.contract(address=MOTD_ADDRESS, abi=MOTD_ABI,ContractFactoryClass=ConciseContract)
        self.latest = self.motd_contract.get()
        self.count = self.motd_contract.changedCount()
        print('got: ',self.motd_contract.get())

    def run(self):
        log.info('main thread started')
        while True:
            log.info('all systems go, latest: (%d) %s [%d]', self.headnumber, self.latest, self.count)
            time.sleep(WAIT_SECONDS)

    def handle_event(self, event):
        log.info('%s: new event: %x', datetime.datetime.utcnow(), event)
        self.count = self.motd_contract.changedCount()
        self.block = self.aqua.gethead()
        self.latest = self.motd_contract.get()
        self.headnumber = int(self.block['number'], 16)



    def log_loop(self, event_filter, poll_interval):
        log.info('filter log thread started')
        while True:
            # for event in block_filter.get_new_entries():
            #     self.handle_event(event)
            for tx in event_filter.get_new_entries():
                print('\n', len(tx))
                tx_hash = tx.hex()
                t = self.aqua.gettransaction(f'{tx_hash}')
                if t == None:
                    t = self.aqua.getblockbyhash(tx_hash)
                print("\nnew event:", tx_hash,'\n\n', t,'\n')
            time.sleep(poll_interval)


if __name__ == '__main__':
    from threading import Thread
    system = System()
    block_filter = system.aqua.w3.eth.filter('latest')
    Thread(target=system.log_loop, args=(block_filter, 1), daemon=True).start()
    tx_filter = system.aqua.w3.eth.filter('pending')
    Thread(target=system.log_loop, args=(tx_filter, 1), daemon=True).start()
    # event_filter = motd_contract.events.filter({'filter': {}})
    # Thread(target=system.log_loop, args=(event_filter, 1), daemon=True).start()
    system.run()
