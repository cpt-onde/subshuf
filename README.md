# subshuf

**sub**stitution cipher through **shuf**fling of a word list, for computerless encryption of seed words from one piece of paper to another.

## No guarantees

There may be gaping security holes. Not written by a cryptographer. Use your own judgement. 

## Purpose

To help encrypt a cleartext word seed you have on paper to another piece of paper without inputting the seed into a computer. Uses a lookup table for this.
There is also a reverse lookup table to get back to cleartext.

The shuffled word order in the lookup tables is deterministically defined by a password or passphrase that you set.

## What it does

Shuffles a word list based on a keystretched password/passphrase to create a lookup table substitution cipher kind of. Uses either python or node.js.

It uses Argon2i for keystretching, which seeds a a crude SHA256 pseudo random number generator (PRNG) and then Fisher-Yates for the shuffling, based on the input from the PRNG.

## How it does it

Takes a word list file called english.json, outputs in json and csv formats forward and reverse lookup tables as word pairs.

## How to use it

* Install dependencies for python and/or node.js respectively. They are independent, you only need either python or node.js.

* Place a file called english.json with all possible words in the directory.

* Set a password or passphrase as an environment variable called subshufpw.

* Run the python or node.js script

* You now have a lookup table and a reverse lookup table

* The csv can be pasted into LibreOffice and ask it to make a table of it "Table>Convert>Text to Table…"

* Use the table to encrypt your seed from paper to paper, by manually looking up each word in the table called "forward" something

* Use the "reverse" something table to verify that you can get back to cleartext

* Remember the password/passphrase to at a later time get back to cleartext, by inputting it into the program and create the reverse lookup table anew

The keystretching takes about 1GB of RAM
