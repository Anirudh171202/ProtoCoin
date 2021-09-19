<template>
  <div class="rounded-md border-gray-700">
      <h1 class="text-3xl mb-3">Make Transaction</h1>

      <label class="mb-1" for="to-public-key">Receiver's Public Key</label>
      <input
        id="to-public-key"
        class="rounded-sm bg-gray-600 px-2 py-1 w-full mt-1 mb-3 text-sm"
        type="text"
        placeholder="Enter public key of receiver"
        v-model="toPublicKey" />

      <label class="mb-1" for="amount">Amount</label>
      <input
        id="amount"
        class="rounded-sm bg-gray-600 px-2 py-1 mt-1 mb-3 block text-sm"
        type="number"
        placeholder="Enter amount of coins to send"
        v-model.number="amount" />

      <button
        @click="sendCoins"
        class="transition rounded-sm hover:bg-gray-600 border-2 border-gray-600 px-2 py-1">
        Send
      </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

import { mapActions } from 'vuex';

export default Vue.extend({
  data() {
    return {
      amount: 0,
      toPublicKey: '',
    };
  },
  methods: {
    sendCoins() {
      const { amount, toPublicKey: receiver } = this;

      if (typeof amount !== 'number'
        || Number.isNaN(amount)
        || !Number.isFinite(amount)
        || amount <= 0) {
        // eslint-disable-next-line no-alert
        alert('Please enter a valid amount');
      }

      // eslint-disable-next-line no-alert
      if (window.confirm(`Are you sure you want to send ${amount} coins to '${receiver}'`)) {
        this.makeTransaction({ amount, receiver });
      }
    },
    ...mapActions(['makeTransaction']),
  },
});
</script>
