import Vue from 'vue';
import Vuex from 'vuex';
import { Transaction, makeTransaction } from './wallet';

Vue.use(Vuex);

interface Credentials {
  publicKey: string;
  privateKey: string;
}

const writeCreds = (creds: Credentials) => {
  localStorage.setItem('creds', JSON.stringify(creds));
};

const getCreds = (): Credentials | null => {
  const creds = localStorage.getItem('creds');

  if (creds === null) {
    return null;
  }

  return JSON.parse(creds);
};

export default new Vuex.Store({
  state: {
    credentials: getCreds(),
    transactions: [] as Transaction[],
  },
  mutations: {
    logout(state) {
      localStorage.removeItem('creds');
      state.credentials = null;
    },
    setCredentials(state, credentials: Credentials) {
      writeCreds(credentials);
      state.credentials = credentials;
    },
    setTransactions(state, transactions: Transaction[]) {
      state.transactions = transactions;
    },
  },
  actions: {
    async makeTransaction({ state: { credentials } }, { receiver, amount }) {
      if (credentials === null) {
        return;
      }

      await makeTransaction({
        receiver,
        amount,
        sender: credentials.publicKey,
      }, credentials.privateKey);
    },
    addTransaction({ state: { transactions } }, transaction: Transaction) {
      transactions.push(transaction);
    },
  },
  getters: {
    hasCredentials({ credentials }) {
      return credentials !== null;
    },
  },
  modules: {},
});
