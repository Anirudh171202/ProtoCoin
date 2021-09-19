<template>
  <div id="app" class="app text-white p-16 h-full min-h-screen bg-gray-900">

    <div class="m-auto w-max min-h-full limit-max">
      <div class="max-w-full p-6 bg-gray-800 rounded-lg">
        <Header />
      </div>

      <div class="h-6 min-h-6"></div>

      <div class="flex flex-col md:flex-row justify-center">
        <div>
          <div class="max-w-full p-6 bg-gray-800 rounded-lg">
            <add-details v-if="!hasCredentials" />
            <make-transaction v-else />
          </div>
          <div
            v-if="hasCredentials"
            class="max-w-full p-6 bg-gray-800 rounded-lg mt-6">
            <button
              @click="logout"
              class="transition rounded-sm hover:bg-gray-600
                border-2 border-gray-600 px-2 py-1 w-full">
              Logout
            </button>
          </div>
        </div>

        <div class="w-6 min-w-6"></div>

        <div class="max-w-full p-6 bg-gray-800 rounded-lg">
          <transactions />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters, mapMutations } from 'vuex';

import Header from './components/Header.vue';
import AddDetails from './components/AddDetails.vue';
import MakeTransaction from './components/MakeTransaction.vue';
import Transactions from './components/Transactions.vue';

export default Vue.extend({
  name: 'App',
  computed: mapGetters(['hasCredentials']),
  methods: mapMutations(['logout']),
  components: {
    Header,
    AddDetails,
    MakeTransaction,
    Transactions,
  },
});
</script>

<style scoped>
.max-400 {
  max-width: 400px;
}

.min-w-6 {
  min-width: 1.5rem;
}

.app .limit-max {
  max-width: calc(100vw - 9rem);
}
</style>
