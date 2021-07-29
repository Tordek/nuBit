<template>
  <div>
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="https://bulma.io">
          8Bit logo
        </a>
        <div class="navbar-end">
          <div class="navbar-item">
            <UserInformation :user="user" @update:user="setUser" />
          </div>
        </div>
      </div>
    </nav>
    <section class="section">
      <RouterView @update:user="setUser" />
    </section>
  </div>
</template>

<script lang="ts">
import UserInformation from "@/components/UserInformation.vue";
import Vue from "vue";
import { UserDataResponse } from './services/getUserData';

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