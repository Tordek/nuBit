<template>
  <div class="vote-star-widget">
    <div
      v-for="starNum in [1, 2, 3, 4, 5]"
      class="vote-star-cell"
      :key="starNum"
    >
      <button
        @click="vote(starNum)"
        class="vote-star"
        v-tooltip="paramData.helpTipDefs[starNum]"
        :title="`Vote ${starNum} out of 5 in this category.`"
      >
        <img
          v-if="value >= starNum"
          class="vote-star-img"
          src="../assets/interface-star-yes.svg"
          :alt="`Vote ${starNum} out of 5 in this category.`"
        />
        <img
          v-else
          class="vote-star-img"
          src="../assets/interface-star-no.svg"
          :alt="`Vote ${starNum} out of 5 in this category.`"
        />
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { VoteParam } from "@/types";
import Vue, { PropType } from "vue";
export default Vue.extend({
  name: "VotingWidget",
  props: {
    value: Number,
    paramData: Object as PropType<VoteParam>
  },
  methods: {
    vote(newValue: number): void {
      if (this.value === newValue) {
        this.$emit("input", 0);
      } else {
        this.$emit("input", newValue);
      }
    }
  }
});
</script>

<style scoped>
.vote-star-widget {
  display: flex;
  border-collapse: collapse;
  margin: 0px;
  padding: 0px;
}

.vote-star-cell {
  margin: 0px;
  padding: 0px;
}

.vote-star {
  background: none;
  border: none;
  font-size: 1.2em;
  padding: 0px;
  margin-right: 1px;
  width: 1.2em;
  height: 1.2em;
  overflow: hidden;
  top: 2px;
}

.vote-star-img {
  width: 1.2em;
  margin: 0px;
  padding: 0px;
}
</style>
