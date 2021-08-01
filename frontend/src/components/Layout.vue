<template>
  <div>
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          8Bit logo
        </a>
      </div>
      <div class="navbar-start">        
        <div class="navbar-item">
          <router-link to="/weeks/current">Current week entries</router-link>
        </div>        
        <div class="navbar-item">
          <router-link to="/weeks/next">Next week entries</router-link>
        </div>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="navbar-item">
            <router-link to="/results" class="button is-primary">My results</router-link>
          </div>
          <UserInformation :user="user" @update:user="setUser" />
        </div>
      </div>
    </nav>
    <section class="section">
      <RouterView :user="user" :key="$route.fullPath" />
    </section>
  </div>
</template>

<script lang="ts">
import UserInformation from "@/components/UserInformation.vue";
import { UserData } from "@/types";
import Vue from "vue";

export default Vue.extend({
  components: { UserInformation },
  data() {
    return {
      user: null as UserData | null
    };
  },
  methods: {
    setUser(user: UserData) {
      this.user = user;
    }
  }
});
</script>