<template>
  <div>
    <h1 class="text-3xl mb-3">Transactions</h1>

    <div class="grid table-cols rounded-md border-gray-700 border-2">

      <h2 class="p-4 bg-gray-700 border-gray-700 border-2 text-center">From</h2>
      <h2 class="p-4 bg-gray-700 border-gray-700 border-2 text-center">To</h2>
      <h2 class="p-4 bg-gray-700 border-gray-700 border-2 text-center">Amount</h2>

      <template v-for="(transaction, index) in reversedTransactions">
        <p
          class="p-4 border-gray-700 border-2 text-center
            overflow-ellipsis overflow-hidden whitespace-nowrap"
          :title="transaction.sender"
          :key="`sender-${index}`">
          {{ transaction.sender }}
        </p>
        <p
          class="p-4 border-gray-700 border-2 text-center
            overflow-ellipsis overflow-hidden whitespace-nowrap"
          :title="transaction.receiver"
          :key="`receiver-${index}`">
          {{ transaction.receiver }}
        </p>
        <p
          class="p-4 border-gray-700 border-2 text-center
            overflow-ellipsis overflow-hidden whitespace-nowrap"
          :title="transaction.amount"
          :key="`amount-${index}`">
          {{ transaction.amount }}
        </p>
      </template>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import { mapState } from 'vuex';

import { getBlockchain } from '../wallet';

export default Vue.extend({
  computed: {
    ...mapState(['transactions']),
    reversedTransactions() {
      return [...this.transactions].reverse();
    },
  },
  mounted() {
    setInterval(async () => {
      const transactions = [];
      (await getBlockchain()).forEach(block => {
        transactions.push(...block.transactions);
      });
      this.$store.commit('setTransactions', transactions);
    }, 2000);
  },
  name: 'transactions',
});
</script>

<style>
.table-cols {
  grid-template-columns: 5fr 5fr 1fr;
}
</style>
