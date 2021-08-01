<template>
  <div>
    <object :data="entry.pdfUrl" type="application/pdf">
      <div>
        <img src="@/assets/kirb_think.png" />
        <h2>
          <a :href="entry.pdfUrl">Link to PDF (embedded viewer failed)</a>
        </h2>
      </div>
    </object>

    <audio
      v-if="entry.mp3Format === 'mp3'"
      controls
      :src="entry.mp3Url"
      type="audio/mpeg"
    />
    <div v-else>
      <img src="@/assets/interface-play.png" />
      <a :href="entry.mp3Url" target="_blank">Listen Here!</a>
    </div>
    <div>
      <div v-for="voteParam in voteParams" :key="voteParam.name">
        <p class="vote-star-bottom-label">{{ voteParam.description }}</p>
        <VotingWidget
          :paramData="voteParam"
          v-model="entry[voteParam.name]"
          @input="$emit('voted')"
        />
      </div>
      <div>
        <p>{{ truncatedName }}</p>

        <p></p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Entry, VoteParam } from "@/types";
import Vue, { PropType } from "vue";
import VotingWidget from "../components/VotingWidget.vue";
export default Vue.extend({
  components: { VotingWidget },
  props: {
    entry: Object as PropType<Entry>,
    voteParams: Array as PropType<VoteParam[]>
  },
  computed: {
    truncatedName(): string {
      const s = `${this.entry.entrantName} - ${this.entry.entryName}`;
      if (s.length > 60) {
        return s.slice(0, 60) + "...";
      }
      return s;
    }
  }
});
</script>