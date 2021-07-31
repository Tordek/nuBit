<template>
  <section class="section">
    <div class="container">
      <template v-if="error === null">
        <h1 class="title">Logging you in, hold on...</h1>
        <progress class="progress is-large is-info" max="100"
          >Logging you in...</progress
        >
      </template>
      <template v-else>
        <h1 class="title">Oh no!</h1>
        <h2 class="subtitle">
          There's been an error during login.
        </h2>
        <p><router-link to="/">Go back home</router-link>.</p>
      </template>
    </div>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import loginOauth from "@/services/loginOauth";

const APP_URL = process.env["VUE_APP_APP_URL"];

export default Vue.extend({
  data() {
    return {
      error: null as null | string
    };
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