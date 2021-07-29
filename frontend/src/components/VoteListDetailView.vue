<template>
  <div>
    <div v-show="working">
      PUT A SPINNER HERE OR SOMETHING I'M LAZY
    </div>
    <transition name="entry-list-toggle">
      <div v-show="showEntryList">
        <h2>{{ weekData.theme }}</h2>
        <h3>{{ weekData.date }} - {{ entries.length }} entries</h3>

        <table cellpadding="0">
          <thead>
            <tr>
              <th>Entrant</th>
              <th>Composition Title</th>
              <th>View &amp; Listen</th>
              <th>Download</th>
              <th
                v-for="voteParam in weekData.voteParams"
                :key="voteParam.name"
              >
                {{ voteParam.description }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entry, entryIndex) in entries" :key="entryIndex">
              <td>{{ entry.entrantName }}</td>
              <td>{{ entry.entryName }}</td>
              <td
                :class="{
                  'entry-cell-selected': viewedEntryIndex == entryIndex
                }"
              >
                <button class="icon-button" @click="viewEntry(entryIndex)">
                  <img src="/static/interface-video-play.png" alt="Play" />
                </button>
              </td>
              <td>
                <a :href="entry.mp3Url" target="_blank">MP3</a>
                <a :href="entry.pdfUrl" target="_blank">PDF</a>
              </td>
              <td
                v-for="voteParam in weekData.voteParams"
                :key="voteParam.name"
              >
                <VotingWidget
                  :paramData="voteParam"
                  v-model="entry[voteParam.name]"
                  @input="updateNumEntriesRated"
                />
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="weekData.votingOpen">
          <p>
            You've rated {{ numEntriesRated }}/{{ entries.length }} entries.
          </p>
          <button @click="submitVote">
            Submit Vote
          </button>
        </div>
        <div v-else>
          <p>Voting for this week is now closed.</p>
        </div>
      </div>
    </transition>

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

      <EntryDetail v-else :entry="weekData.entries[viewedEntryIndex]" :voteParams="weekData.voteParams"/>
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
import { WeekData } from "../types";
import postUserVotes, { PostUserVotesParams } from "@/services/postUserVotes";
import EntryDetail from "../components/EntryDetail.vue";
import VotingWidget from "./VotingWidget.vue";

export default Vue.extend({
  components: { EntryDetail, VotingWidget },
  props: {
    weekData: Object as PropType<WeekData>,
    userVoteKey: String
  },
  data() {
    return {
      showEntryList: true,
      pdfColorInvert: false,
      viewedEntryIndex: null as number | null,
      working: false,
      entries: this.weekData.entries
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
      if (this.viewedEntryIndex === null) return;

      let index = this.viewedEntryIndex + offset;

      if (index < 0) {
        index = 0;
      } else if (index >= this.entries.length) {
        index = this.entries.length - 1;
      }

      this.viewedEntryIndex = index;
      this.showEntryList = false;
    },
    async submitVote() {
      this.working = true;

      if (this.userVoteKey === "") {
        alert(
          'Please enter a vote key! (To obtain a vote key, DM the command "vote!vote" to @8Bot on the 8BMT discord server.'
        );
        return;
      }

      let voteData: PostUserVotesParams = {
        votes: [],
        voteKey: this.userVoteKey
      };

      for (let entry of this.entries) {
        for (let param of this.weekData.voteParams) {
          if (entry[param.name] != null) {
            voteData.votes.push({
              entryUUID: entry.uuid,
              voteForName: entry.entrantName,
              voteParam: param.name,
              rating: entry[param.name]
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
      var total = 0;

      for (let entry of this.entries) {
        for (let param of this.weekData.voteParams) {
          if (entry[param.name] !== null && entry[param.name] != 0) {
            total++;
            break;
          }
        }
      }

      return total;
    },
  }
});
</script>