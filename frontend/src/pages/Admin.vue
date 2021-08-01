<template>
  <div class="tabs">
    <ul>
      <li :class="{ 'is-active': state === 'weeks' }" @click="state = 'weeks'">
        <a>Week setup</a>
      </li>
      <li
        :class="{ 'is-active': state === 'current' }"
        @click="state = 'current'"
      >
        <a>Current Week</a>
      </li>
      <li :class="{ 'is-active': state === 'next' }" @click="state = 'next'">
        <a>Next Week</a>
      </li>
    </ul>

    <div v-if="state === 'weeks'">
      <Weeks>
    </div>
    <div v-if="state === 'current' || state === 'next'">
      <AdminWeekView :which="state">
    </div>
  </div>
</template>
<script lang="ts">
import AdminWeekView from "@/components/AdminWeekView.vue";
import { UserData } from "@/types";
import Vue, { PropType } from "vue";
export default Vue.extend({
  components: {    
    AdminWeekView
  },
  props: {
    user: Object as PropType<UserData>
  },
  data() {
    return {
      state: "weeks"
    };
  }
});
</script>