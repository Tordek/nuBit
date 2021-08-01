<template>
  <div>
    <div v-if="user !== null">
      <img
        :src="user.avatar"
        alt="User Avatar"
      />
      {{ user.username }}
      <button class="button is-danger" @click="logout">
        <i class="fas fa-power-off"></i>
      </button>
    </div>
    <div v-else-if="oauthUrl !== null" class="buttons">
      <a class="button is-primary" :href="oauthUrl">
        Log in with Discord
      </a>
    </div>
    <progress v-else class="progress" style="width: 100px" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import getUserData from "@/services/getUserData";
import getAuthUrl from "@/services/getAuthUrl";
import logout from "@/services/logout";
import { PropType } from "vue/types/options";
import { UserData } from "@/types";

const APP_URL = process.env["VUE_APP_APP_URL"];

export default Vue.extend({
  props: {
    user: Object as PropType<UserData>
  },
  data() {
    return {
      oauthUrl: null as string | null
    };
  },
  async mounted() {
    try {
      const userData = await getUserData();
      this.$emit("update:user", userData);
      return;
    } catch {
      // No problem if the user isn't logged in.
    }

    this.getLoginLink();
  },
  methods: {
    async logout() {
      try {
        await logout();
      } finally {
        this.$emit("update:user", null);
        this.getLoginLink();
        if (this.$route.path !== '/')
          this.$router.push("/");
      }
    },
    async getLoginLink() {
      // If there was no login, fetch the login URL
      try {
        this.oauthUrl = (
          await getAuthUrl({ redirectUri: `${APP_URL}/oauth/discord` })
        ).authUrl;
      } catch {
        // TODO: Actually display the error
        // because we can't login now
      }
    }
  }
});
</script>