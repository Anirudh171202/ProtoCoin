<template>
    <div class="rounded-md border-gray-700">
      <h1 class="text-3xl mb-3">Enter your credentials</h1>

      <label class="mb-1" for="public-key">Public Key</label>
      <input
        id="public-key"
        class="rounded-sm bg-gray-600 px-2 py-1 w-full mt-1 mb-3 text-sm"
        type="text"
        placeholder="Enter public key here"
        v-model="publicKey" />

      <label class="mb-1" for="private-key">Private Key</label>
      <input
        id="private-key"
        class="rounded-sm bg-gray-600 px-2 py-1 w-full mt-1 mb-3 text-sm"
        type="text"
        placeholder="Enter private key here"
        v-model="privateKey" />

      <button
        @click="setCredentials({ publicKey, privateKey })"
        class="transition rounded-sm hover:bg-gray-600 border-2 border-gray-600 px-2 py-1">
        Submit
      </button>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';

import { mapMutations } from 'vuex';

export default Vue.extend({
  data() {
    return {
      publicKey: '',
      privateKey: '',
    };
  },
  methods: mapMutations(['setCredentials']),
  name: 'add-details',
});
</script>
