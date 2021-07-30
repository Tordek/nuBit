<template>
  <div>
    <progress v-if="error === null" class="progress is-large is-info" max="100"
      >Logging you in...</progress
    >
    <p v-else>
      There's been an error logging in. <router-link to="/">Go back home</router-link>.
    </p>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import loginOauth from "@/services/loginOauth";

const APP_URL = process.env["VUE_APP_APP_URL"];

export default Vue.extend({
  data() {
    return {
      error: null as null | string
    }
  },
  async mounted() {
    const query = this.$route.query;

    if (query["code"] === null || Array.isArray(query["code"])) {
      // If there's no code (or we somehow got 2 codes), we're in the wrong place. Bail.
      this.$router.push("/");
    }

    // Hide the token from the URL bar
    // this.$router.replace({ name: "OauthDiscord" })

    try {
      await loginOauth({
        code: query["code"] as string,
        state: query["state"] as string,
        redirectUri: `${APP_URL}/oauth/discord`
      });

      this.$router.replace("/");
    } catch (e) {
      this.error = e.toString();
      console.log(e);
    }
  }
});
</script>