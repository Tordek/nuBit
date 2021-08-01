<template>
  <div>    
      <template v-if="state === 'loading'">
        <h1 class="title">
          Hold up, we're looking for your submission...
        </h1>
        <progress class="progress is-large is-info">Loading</progress>
      </template>
      <template v-else-if="state === 'display' && entry !== null">
        <h1 class="title">{{ entry.entryName }}</h1>
        <p><a @click="state = 'submit'" class="button is-primary">Change it!</a></p>
      </template>
      <template v-else-if="state === 'display'">
        <h1>You haven't submitted anything yet...</h1>
        <p><a @click="state = 'submit'" class="button is-primary">Submit something!</a></p>
      </template>
      <template v-else-if="state === 'submit'">
        <Submit :initialEntry="entry" @update:entry="updateEntry" />
      </template>
  </div>
</template>

<script lang="ts">
import { Entry, UserData } from "@/types";
import Vue, { PropType } from "vue";
import Submit from "@/components/Submit.vue";
import getUserEntry from "@/services/getUserEntry";

export default Vue.extend({
  components: {
    Submit
  },
  props: {
    user: Object as PropType<UserData>
  },
  data() {
    return {
      entry: null as null | Entry,
      state: "blank"
    };
  },
  async mounted() {
    this.state = "loading";

    try {
      this.entry = await getUserEntry();
    } catch {
      // No entry, no problem.
    }

    this.state = "display";
  },
  methods: {
    updateEntry(entry: Entry) {
      this.entry = entry;
      this.state = "display";
    }
  }
});
</script>