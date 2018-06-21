#!/usr/bin/env python3
'''
Aquachain Test Suite
'''

from aquachain.aquatool import AquaTool

import os
import unittest
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

aqua = AquaTool(rpchost='https://c.onical.org')



class Test_AAA(unittest.TestCase):
    def test_web3(self):
        log.info("1.3 aqua is %s wei", aqua.to_wei(1.3))


class Test_Blocks(unittest.TestCase):

    def test_getblock(self):
        for i in range(1):
            log.info("fetching block %s", i)
            block = aqua.getblock(i)
            self.assertTrue('number' in block)
            self.assertTrue(block['number'] == hex(i))
            log.info("got expected hash: %s", (block['hash']))

    def test_getblockbyhash(self):
        log.info("running blockbyhash")
        block10 = aqua.getblock(10)
        block = block10
        for i in range(1):
            self.assertTrue('parentHash' in block)
            log.info("fetching block %s (%s)", 10-(i+1), block['parentHash'])
            block = aqua.getblockbyhash(block['parentHash'])
            self.assertTrue(block['number'] == hex(10-(i+1)))

    def test_gethead(self):
        print("head block")
        print(aqua.gethead())

    def test_checksum_encode(self):
        self.assertTrue('0x545ac449bfc7891ef1a8d2065aa2a54ba7570c45' != aqua.checksum_encode('0x545ac449bfc7891ef1a8d2065aa2a54ba7570c45'))


class Test_Transactions(unittest.TestCase):
    def test_gettransaction(self):
        head = aqua.gethead()
        block = head
        self.assertTrue('number' in head)
        log.info("head block: %s", int(head['number'], 16))
        self.assertNotEqual('', block)
        for i in range(5):
            block = aqua.getblockbyhash(block['parentHash'])
            self.assertNotEqual(block, '')
            log.debug("fetched block %s (%s)",
                      int(block['number'], 16), block['hash'])
            if len(block['transactions']) > 0:
                tx = aqua.gettransaction(block['transactions'][0]['hash'])
                log.debug("found tx: %s", tx)


if __name__ == '__main__':
    unittest.main()
