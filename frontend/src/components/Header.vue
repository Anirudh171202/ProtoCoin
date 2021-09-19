<template>
  <div>
    <h1 class="text-5xl mb-4">ProtoCoin 🪙</h1>

    <h4 class="mb-2 text-lg" for="public-key">Genomes Sequenced</h4>
    <div class="w-full bg-gray-700 rounded-full relative">
      <div class="bg-green-500 rounded-full px-2 text-right" :style="{ width }">
        {{ numTransactions }}
      </div>
      <span class="absolute top-0 right-2">{{ totalCount }}</span>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';

export default Vue.extend({
  name: 'Header',
  computed: {
    numTransactions() {
      return this.$store.state.transactions.length;
    },
    totalCount() {
      let n = this.numTransactions;
      let next = 1;

      while (n >= 1) {
        n /= 10;
        next *= 10;
      }

      return next;
    },
    width() {
      const percent = this.numTransactions / this.totalCount;
      return `${100 * percent}%`;
    },
  },
});
</script>
