<template>
  <div>
    <progress class="progress is-large is-info" max="100"
      >Logging you in...</progress
    >
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import loginOauth from "@/services/loginOauth";
export default Vue.extend({
  async mounted() {
    const query = this.$route.query;

    if (query["code"] === null || Array.isArray(query["code"])) {
      // If there's no code (or we somehow got 2 codes), we're in the wrong place. Bail.
      this.$router.push("/");
    }

    // Hide the token from the URL bar
    // this.$router.replace({ name: "OauthDiscord" })

    try {
      await loginOauth({ authorization_response: query["code"] as string });

      this.$router.replace("/");
    } catch (e) {
      console.log(e);
    }
  }
});
</script>