<template>
  <div>
    <h1 class="title">{{ weekData.theme }}</h1>

    <h2 class="subtitle">
      {{ weekData.date }} - {{ weekData.entryCount }} entries<template
        v-if="weekData.entries === null"
      >
        so far</template
      >
    </h2>

    <template v-if="weekData.entries !== null">
      <table class="table is-hoverable">
        <thead>
          <tr>
            <th>Entrant</th>
            <th>Composition Title</th>
            <th>View &amp; Listen</th>
            <th>Download</th>
            <th v-for="voteParam in weekData.voteParams" :key="voteParam.name">
              {{ voteParam.description }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(entry, entryIndex) in weekData.entries"
            :key="entryIndex"
            :class="{ 'is-selected': viewedEntryIndex == entryIndex }"
          >
            <td>{{ entry.entrantName }}</td>
            <td>{{ entry.entryName }}</td>
            <td>
              <button class="icon-button" @click="viewEntry(entryIndex)">
                <img src="/static/interface-video-play.png" alt="Play" />
              </button>
            </td>
            <td>
              <a :href="entry.mp3Url" target="_blank">MP3</a>
              <a :href="entry.pdfUrl" target="_blank">PDF</a>
            </td>
            <td v-for="voteParam in weekData.voteParams" :key="voteParam.name">
              <VotingWidget
                v-if="user"
                :paramData="voteParam"
                :disabled="!weekData.votingOpen"
                v-model="voteData[entry.uuid][voteParam.name]"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="weekData.entries !== null && weekData.votingOpen">
        <p>
          You've rated {{ numEntriesRated }}/{{ weekData.entries.length }}
          entries.
        </p>
        <button @click="submitVote">Submit Vote</button>
      </div>
    </template>

    <div v-else>
      <p>
        Submissions are still coming in! You can't see them yet, but you'll be
        able to soon.
      </p>
    </div>

    <div
      class="pdf-container"
      :class="{
        'pdf-container-full': !showEntryList,
        'pdf-container-small': showEntryList
      }"
    >
      <div v-if="viewedEntryIndex === null">
        <div id="pdf-alt" class="pdf-alt">
          <img src="/static/kirb_phones.png" />
          <h2>
            Welcome!<br />Select one of the entries on the left to view its
            score.
          </h2>
        </div>
      </div>

      <EntryDetail
        v-else
        :entry="weekData.entries[viewedEntryIndex]"
        :voteParams="weekData.voteParams"
      />
    </div>

    <div>
      <div width="48px" class="viewer-control">
        <button class="icon-button" @click="toggleEntryContainer()">
          <img src="/static/interface-category-grid.png" />
        </button>
      </div>
      <div width="48px" class="viewer-control">
        <button class="icon-button" @click="selectAdjacentEntry(-1)">
          <img src="/static/interface-up-arrow.png" />
        </button>
      </div>
      <div width="48px" class="viewer-control">
        <button class="icon-button" @click="selectAdjacentEntry(1)">
          <img src="/static/interface-down-arrow.png" />
        </button>
      </div>
      <div width="48px" class="viewer-control">
        <button class="icon-button" @click="toggleNightMode()">
          <img src="/static/interface-bulb.png" />
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { UserData, VoteData, WeekData } from "../types";
import postUserVotes, { PostUserVotesParams } from "@/services/postUserVotes";
import EntryDetail from "../components/EntryDetail.vue";
import VotingWidget from "./VotingWidget.vue";

export default Vue.extend({
  components: { EntryDetail, VotingWidget },
  props: {
    user: Object as PropType<UserData>,
    weekData: Object as PropType<WeekData>
  },
  data() {
    return {
      showEntryList: true,
      pdfColorInvert: false,
      viewedEntryIndex: null as number | null,
      voteData: null as VoteData | null,
      working: false
    };
  },
  methods: {
    viewEntry(entryIndex: number) {
      this.viewedEntryIndex = entryIndex;
      this.showEntryList = false;
    },
    toggleEntryContainer() {
      this.showEntryList = !this.showEntryList;
    },
    toggleNightMode() {
      this.pdfColorInvert = !this.pdfColorInvert;
    },
    selectAdjacentEntry(offset: number) {
      if (this.weekData.entries === null) return;
      if (this.viewedEntryIndex === null) return;

      let index = this.viewedEntryIndex + offset;

      if (index < 0) {
        index = 0;
      } else if (index >= this.weekData.entries.length) {
        index = this.weekData.entries.length - 1;
      }

      this.viewedEntryIndex = index;
      this.showEntryList = false;
    },
    async submitVote() {
      if (this.weekData.entries === null) return;
      if (this.voteData === null) return;

      this.working = true;

      let voteData: PostUserVotesParams = {
        votes: [],
      };

      for (let entry of this.weekData.entries) {
        for (let param of this.weekData.voteParams) {
          if (this.voteData[entry.uuid][param.name] != null) {
            voteData.votes.push({
              entryUUID: entry.uuid,
              voteForName: entry.entrantName,
              voteParam: param.name,
              rating: this.voteData[entry.uuid][param.name]
            });
          }
        }
      }

      try {
        postUserVotes(voteData);
        this.$emit("votes-submitted");
      } catch (e) {
        alert(
          "Something went wrong :/\nMake sure you entered a valid vote key"
        );
      }

      this.working = false;
    }
  },
  computed: {
    numEntriesRated() {
      if (this.weekData.entries === null) return 0;
      if (this.voteData === null) return 0;
      var total = 0;

      for (const entry of this.weekData.entries) {
        for (const param of this.weekData.voteParams) {
          if (
            this.voteData[entry.uuid][param.name] !== null &&
            this.voteData[entry.uuid][param.name] !== 0
          ) {
            total++;
            break;
          }
        }
      }

      return total;
    }
  }
});
</script>