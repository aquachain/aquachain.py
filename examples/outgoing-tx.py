from aquachain.aquatool import AquaTool
import sys
aqua = AquaTool(ipcpath='/home/user/.aquachain/aquachain.ipc')

block = aqua.gethead()

total_tx = 0

acct_tx_incoming = []
acct_tx_outgoing = []

ACCOUNT = '0x0000001bb3ee5e82f08c884428797c65c102683e'

if len(sys.argv) == 2:
    ACCOUNT = sys.argv[1]
    print(f'scanning blockchain for transactions related to account: {ACCOUNT}')

try:
    nonce = aqua.getnonce(ACCOUNT)
    balance = aqua.getbalance(ACCOUNT)
    if nonce == 0 and balance == 0:
        print('this account is not active')
        quit()
    print('Account:', ACCOUNT)
    print('Current Balance:', balance)
    print('Current Nonce:', nonce)
except TypeError:
    print('this account is invalid')
    quit()
limit = int(block['number'], 16)
print(f"Scanning {limit} blocks for transactions.", end='', flush=True)
for i in range(limit):
    if i % 100 == 0:
        print('.', end='', flush=True)
    #    print('scanning', int(block['number'], 16))
    l = len(block['transactions'])
    if l > 0:
        total_tx += l
        num = int(block['number'], 16)
        txs = block['transactions']
        for tx in txs:
            if tx['from'] == ACCOUNT:
                acct_tx_outgoing.append(tx['hash'])
            if tx['to'] == ACCOUNT:
                acct_tx_incoming.append(tx['hash'])
    if block['parentHash'] == '0x0000000000000000000000000000000000000000000000000000000000000000':
        break
    block = aqua.getblockbyhash(block['parentHash'], body=True)

print(f'\nfound total of {total_tx} tx on the aquachain')
print(f'{len(acct_tx_outgoing)} of which are from the account: {ACCOUNT},')
print(f'{len(acct_tx_incoming)} of which are from the account: {ACCOUNT},')
print(f'relevant outgoing tx: {acct_tx_outgoing}')
print(f'relevant incoming tx: {acct_tx_incoming}')
