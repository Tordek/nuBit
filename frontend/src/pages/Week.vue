<template>
  <div>
    <div v-if="mode === 'loading'">Loading...</div>
    <VoteListDetailView
      v-else-if="mode === 'vote'"
      :week-data="weekData"
      @vote-submitted="mode = 'thanks'"
    />
    <div v-else-if="mode === 'thanks'" id="content">
      <div class="submit-babble">
        <h2>Thank you for voting!</h2>
        <p>Your vote has been recorded. I will guard it with my life. :)</p>
        <img src="/static/kirb_thanks.png" alt="Thanks!" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import getWeek from "@/services/getWeek";
import getVoteData from "@/services/getVoteData";
import { WeekData, VoteData, UserData } from "@/types";
import Vue, { PropType } from "vue";
import VoteListDetailView from "../components/VoteListDetailView.vue";

export default Vue.extend({
  props: {
    which: String,
    user: Object as PropType<UserData>
  },
  components: {
    VoteListDetailView
  },
  data() {
    return {
      mode: "loading",
      weekData: null as WeekData | null,
      voteData: null as VoteData | null
    };
  },
  async mounted() {
    try {
      this.weekData = await getWeek({which: this.which});

      if (this.user !== null) {
        this.voteData = await getVoteData();
      }

      this.mode = "vote";
    } catch (e) {
      alert("Something went wrong: " + e.toString());
    }
  }
});
</script>

<style scoped>
#thanks {
  width: 500px;
}
</style>