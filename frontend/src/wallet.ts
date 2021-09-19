/* eslint-disable indent */
import { ec as Ecdsa } from 'elliptic';

const ec = new Ecdsa('secp256k1');

export interface Transaction {
  sender: string;
  receiver: string;
  amount: number;
}

const getMiners = async (): Promise<string[]> => {
  const body = await fetch('http://localhost:5000/miners');
  return body.json();
};

export const makeTransaction = async (transaction: Transaction, privateKey: string) => {
  const key = ec.keyFromPrivate(privateKey);

  const message = (new Date()).toString();

  const body = {
    ...transaction,
    message,
    signature: key.sign(message).toString(),
  };

  const miners = await getMiners();

  miners.forEach(minerUrl => {
    fetch(`${minerUrl}/txion`, {
      method: 'POST',
      body: JSON.stringify(body),
      headers: { 'Content-Type': 'application/json' },
    })
      .then(res => res.text())
      .then(console.log);
  });
};

export const getBlockchain = async () => {
  let longestBlockchain = [];

  const miners = await getMiners();

  const blockchains = miners
    .map(minerUrl => fetch(`${minerUrl}/blocks`)
    .then(res => res.json()));

  // eslint-disable-next-line no-restricted-syntax
  for (const blockchainPromise of blockchains) {
    // eslint-disable-next-line no-await-in-loop
    const blockchain = await blockchainPromise;
    if (blockchain.length > longestBlockchain.length) {
      longestBlockchain = blockchain;
    }
  }

  return longestBlockchain;
};
