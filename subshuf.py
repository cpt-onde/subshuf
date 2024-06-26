import os
import math
from nacl import pwhash
import copy
import json
import csv
import hashlib

pwd = os.environ.get('subshufpw')
password = pwd.encode("utf-8")
kdf = pwhash.argon2i.kdf
salt = b'0123456789ABCDEF'
memlimit = 1048576 *1024 # 2**20 kibibytes
Alices_key = kdf(32, password, salt,
                 opslimit=8, memlimit=memlimit )
hexseed = Alices_key.hex()
print(hexseed)
seed = bytes.fromhex(hexseed)
print (seed)


class SHA256PRNG:
    def __init__(self, seed):
        # Ensure the seed is a byte string
        if isinstance(seed, str):
            seed = seed.encode()
        self.state = seed

    def _hash(self):
        self.state = hashlib.sha256(self.state).digest()
        return self.state

    def random(self):
        # Generate 8 bytes and convert to a float in the range [0, 1)
        random_bytes = self._hash()[:8]
        random_int = int.from_bytes(random_bytes, byteorder='big')
        return random_int / (2**64)

prng = SHA256PRNG(seed)

def fisher_yates_shuffle_improved(words):
    """mainly snagged from https://gist.github.com/JenkinsDev/1e4bff898c72ec55df6f"""

    the_list = copy.deepcopy(words)
    amnt_to_shuffle = len(the_list)
    # We stop at 1 because anything * 0 is 0 and 0 is the first index in the list
    # so the final loop through would just cause the shuffle to place the first
    # element in... the first position, again.  This causes this shuffling
    # algorithm to run O(n-1) instead of O(n).
    while amnt_to_shuffle > 1:
        # Indice must be an integer not a float and math.floor returns a float
        i = int(math.floor(prng.random() * amnt_to_shuffle))
        # We are using the back of the list to store the already-shuffled-indice,
        # so we will subtract by one to make sure we don't overwrite/move
        # an already shuffled element.
        amnt_to_shuffle -= 1
        # Move item from i to the front-of-the-back-of-the-list. (Catching on?)
        the_list[i], the_list[amnt_to_shuffle] = the_list[amnt_to_shuffle], the_list[i]
    return the_list

fi = open('english.json')
words = json.load(fi)

shuffled_words = fisher_yates_shuffle_improved(words)

forwards = []
reverses = []
for elem1, elem2 in zip(words, shuffled_words):
    forwards.append([elem1,elem2])
    reverses.append([elem2,elem1])

reverses.sort(key=lambda x: x[0])
fo = open('pairwise-forward.json', 'w')
fo2 = open('pairwise-reverse.json', 'w')
json.dump(forwards,fo)
json.dump(reverses,fo2)

fo3 = open('pairwise-forward.csv', 'w')
fo4 = open('pairwise-reverse.csv', 'w')
writer1 = csv.writer(fo3)
writer2 = csv.writer(fo4)
writer1.writerows(forwards)
writer2.writerows(reverses)
