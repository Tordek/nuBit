<template>
  <div>
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="https://bulma.io">
          8Bit logo
        </a>
      </div>
      <div class="navbar-start">        
        <div class="navbar-item">
          <router-link to="/weeks/current">Current week entries</router-link>
        </div>        
        <div class="navbar-item">
          <router-link to="/weeks/previous">Previous week entries</router-link>
        </div>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="navbar-item">
            <router-link to="/submit" class="button is-primary">Submit your entry</router-link>
          </div>
          <UserInformation :user="user" @update:user="setUser" />
        </div>
      </div>
    </nav>
    <section class="section">
      <RouterView />
    </section>
  </div>
</template>

<script lang="ts">
import UserInformation from "@/components/UserInformation.vue";
import Vue from "vue";
import { UserDataResponse } from '@/services/getUserData';

export default Vue.extend({
  components: { UserInformation },
  data() {
    return {
      user: null as UserDataResponse | null
    };
  },
  methods: {
    setUser(user: UserDataResponse) {
      this.user = user;
    }
  }
});
</script>