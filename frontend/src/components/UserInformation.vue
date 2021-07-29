<template>
  <div>
    <div v-if="user === null" class="buttons">
      <a class="button is-primary" :href="oauth_url">
        Log in with Discord
      </a>
    </div>
    <div v-else>
      <img
        :src="`https://cdn.discordapp.com/avatars/${user.user_id}/${user.avatar}.png`"
        alt="User Avatar" />
    </div>
  </div>
</template>
<script lang="ts">
import Vue from "vue";
import getUserData, { UserDataResponse } from "@/services/getUserData";
import { PropType } from "vue/types/options";

const oauth_url = process.env.VUE_APP_OAUTH_URL;

export default Vue.extend({
  props: {    
      user: Object as PropType<UserDataResponse>
  },
  data() {
    return {
      oauth_url
    }
  },
  async mounted() {
    try {
      const userData = await getUserData();
      this.$emit('update:user', userData)
    } catch (e) {
      // We don't care about login errors
    }
  }
});
</script>