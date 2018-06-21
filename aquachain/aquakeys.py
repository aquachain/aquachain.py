#!/usr/bin/env python3

import json
import datetime
import os
import errno

from aquachain.bip44 import HDPrivateKey, HDKey

import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def mkdir_if_not_exist(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def default_keystore_dir():
    # TODO: windows
    return os.path.expanduser('~/.aquachain/keystore/')

# Keystore has a directory and a HD path, creates and manages keys.
class Keystore(object):
    def __init__(self, directory='', hdpath="m/44'/60'/0'/0"):
        if directory == '':
            log.info("no directory found, looking in default place: %s",
                     default_keystore_dir())
            directory = default_keystore_dir()

        self.hdpath = hdpath
        self.directory = directory
        log.info("keystore dir: %s", self.directory)

    # listphrases returns available phrases in keystore directory
    def listphrases(self):
        log.debug("were gonna list phrases stored in %s", self.directory)
        keys = []
        if not os.path.isdir(os.path.expanduser(self.directory)):
            log.error("no keystore found")
            return keys

        for (root, dirs, files) in os.walk(self.directory):
            for file in files:
                if file.startswith('aqua') and file.endswith('.wallet'):
                    file_abs = os.path.join(root, file)
                    log.info("Found aqua key: %s", file)
                    try:
                        contents = self.readfile(file_abs)
                        if 'poem' not in contents:
                            log.error("skipping becausae no poem")
                            continue
                        log.debug("read phrase %s", contents['poem'])
                    except Exception as e:
                        log.error("skipping becausae \"%s\"", e)
                        continue
                    else:
                        log.info("WAS GOOD KEY: %s", file)
                        keys.append(contents['poem'])
        return keys

    # from_parent_key returns a key derived from the parent key, at i
    def from_parent_key(self, key, i):
        return HDPrivateKey.from_parent(key, i)

    # save_phrase writes a new phrase file to the keystore directory
    def save_phrase(self, phrase):
        mkdir_if_not_exist(self.directory)
        now = datetime.datetime.now()
        nowstr = now.strftime("%s") + str(now.microsecond)
        filename = f'aqua{nowstr}.wallet'
        abs = os.path.join(self.directory, filename)

        dat = {
            "poem": phrase,
            "version": 1,
            }

        data = json.dumps(dat)
        log.debug("saving key in %s", abs)
        with open(abs, 'w+') as file:
            file.write(data)
        return abs

    # load_phrase returns a list of keys, from the given phrases and password.
    def load_phrases(self, phrases, password):
        keyset = []
        for phrase in phrases:
            keyset.append(self.load_phrase(phrase, password))
        return keyset

    # load_phrase returns a HDKey from the phrase with given password
    def load_phrase(self, phrase, password):
        return HDKey.from_path(HDPrivateKey.master_key_from_mnemonic(phrase, password), self.hdpath)[-1]

    # readfile reads aquachain phrase files containing 'poem' field
    def readfile(self, filename):
        with open(filename) as data:
            d = json.load(data)
            data.close()
            log.debug("keyfile found: %s %s", filename, d)
            log.debug("file contained: %s", d)
            if 'poem' in d:
                return d
        raise Exception("ERROR: could not read file")
