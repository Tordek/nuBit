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
        <p>Download the <a :href="entry.mp3Url">MP3</a></p>
        <p>Download the <a :href="entry.pdfUrl">PDF</a></p>
        
        <template v-if="entry.results === undefined">
            <p>Results are still coming in, be patient...</p>
        </template>

        <template v-else>
            <p>Your average score was {{ entry.results.overall.rating }}!</p>

            <p>On each of the categories, you got...</p>
            <ul>
                <li v-for="rating in entry.results.ratings" :key="rating.name">
                  <b>{{rating.description}}</b>: {{rating.rating}}
                </li>
            </ul>
        </template>
      </template>
      <template v-else-if="state === 'display'">
        <h1>You didn't submit anything last week...</h1>
        <p><router-link to="/mine">But you can try next week!</router-link></p>
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
      this.entry = await getUserEntry({ which: 'current' });
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