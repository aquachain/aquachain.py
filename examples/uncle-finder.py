from aquachain.aquatool import AquaTool

aqua = AquaTool(ipcpath='/home/user/.aquachain/aquachain.ipc')

block = aqua.gethead()

total_uncles = 0
uncle_blocks = []
for i in range(1000000):
    #if i % 1000 == 0:
    #    print('scanning', int(block['number'], 16))
    l = len(block['uncles'])
    if l > 0:
        total_uncles += l
        num = int(block['number'], 16)
        print('uncles in', num, l)
        uncle_blocks.append(num)
    if block['parentHash'] == '0x0000000000000000000000000000000000000000000000000000000000000000':
        break
    block = aqua.getblockbyhash(block['parentHash'])

print(f'found total of {total_uncles} uncles')
print(f'located in blocks: {uncle_blocks}')
