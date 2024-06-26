const crypto = require('crypto');
const argon2 = require('argon2');
const fs = require('fs');
const csvWriter = require('csv-writer').createArrayCsvWriter;

async function generateSeed(password, salt) {
    try {
        const hash = await argon2.hash(password, {
            type: argon2.argon2i,
            timeCost: 8,
            raw: true,
            salt: Buffer.from(salt, 'ascii'),
            memoryCost: 1024 * 1024,
            hashLength: 32,
            parallelism: 1,
        });
        const hashHex = Buffer.from(hash).toString('hex');
        const seed = Buffer.from(hashHex, 'hex')
        console.log(hashHex)
        return seed;
    } catch (err) {
        console.error(err);
    }
}

class SHA256PRNG {
    constructor(seed) {
      // Ensure the seed is a buffer
      if (typeof seed === 'string') {
        seed = Buffer.from(seed, 'utf8');
      }
      this.state = seed;
    }
  
    _hash() {
      this.state = crypto.createHash('sha256').update(this.state).digest();
      return this.state;
    }
  
    random() {
      // Generate 8 bytes and convert to a float in the range [0, 1)
      const randomBytes = this._hash().slice(0, 8);
      const randomInt = randomBytes.readBigUInt64BE();
      return Number(randomInt) / Number(BigInt(2) ** BigInt(64));
    }
  }

function fisherYatesShuffle(array, generator) {
    let currentIndex = array.length;
    while (currentIndex > 1) {
        let randomIndex = Math.floor(generator.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
    return array;
}

function writeJsonFile(filename, data) {
    fs.writeFileSync(filename, JSON.stringify(data, null, 2));
}

async function main() {
    // const password = 'masonit';
    const password = process.env.subshufpw;
    const salt = '0123456789ABCDEF';
    const seed = await generateSeed(password, salt);
    const generator = new SHA256PRNG(seed);

    const words = JSON.parse(fs.readFileSync('english.json', 'utf8'));
    const shuffledWords = fisherYatesShuffle([...words], generator);
    const forwards = words.map((word, index) => [word, shuffledWords[index]]);
    const reverses = shuffledWords.map((word, index) => [word, words[index]]).sort((a, b) => a[0].localeCompare(b[0]));

    writeJsonFile('pairwise-forward-js.json', forwards);
    writeJsonFile('pairwise-reverse-js.json', reverses);

    const forwardCsvWriter = csvWriter({ path: 'pairwise-forward-js.csv' });
    const reverseCsvWriter = csvWriter({ path: 'pairwise-reverse-js.csv' });

    await forwardCsvWriter.writeRecords(forwards);
    await reverseCsvWriter.writeRecords(reverses);
}

main().catch(console.error);
