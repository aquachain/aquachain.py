# python3.6
from aquachain.aquatool import AquaTool

aqua = AquaTool(ipcpath='~/.aquachain/aquachain.ipc')
head = aqua.gethead_header()
headnumber = int(head['number'], 16)

def fmtrange(x, y):
    s = str(x)
    if x == y + 1 or x == y - 1:
        return f'{x}, {y}'
    for i in range(x+1, y):
       s += ',' + str(i) 
    return s


blocks_mined = []
msg = ""
prev_num   = 0
prev_miner = ''
for i in range(headnumber):
    block = aqua.getblock(headnumber-i)
    if block['miner'] == prev_miner:
        cur = int(block['number'], 16)
        blocks_mined.append(cur)
        msg = f"Block {blocks_mined} mined by {block['miner']}"
    elif msg != '':
        if len(blocks_mined) > 10:
            msg = 'super effective! '+msg
        if len(blocks_mined) > 3:
            print(msg)
        msg = ''
        blocks_mined = []
    else:
        blocks_mined = []
        msg = ''
    prev_miner = block['miner']

