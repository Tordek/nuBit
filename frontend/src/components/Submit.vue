<template>
  <div>
    <div class="block">
      <h1 class="title">Get ready!</h1>
      <h2 class="subtitle">
        Thanks for participating this week, and congratulations for exercising
        your musical skills!
      </h2>
    </div>

    <div class="column is-half is-offset-one-quarter">
      <template v-if="state === 'loading'">
        <h1 class="title">
          Hold on..
        </h1>
        <progress class="progress is-large is-info">Loading</progress>
      </template>

      <form v-else-if="state === 'editing'" class="box" @submit="submit">
        <div class="field">
          <label for="entryName" class="label">Entry Name</label>
          <input
            v-model="entry.entryName"
            id="entryName"
            type="text"
            class="input"
          />
        </div>

        <div class="field">
          <label class="label">Audio format</label>
          <div class="control">
            <label class="radio">
              <input v-model="entry.mp3Format" type="radio" value="upload" />
              Upload MP3</label
            >
            <label class="radio"
              ><input v-model="entry.mp3Format" type="radio" value="external" />
              Link MP3</label
            >
            <label v-show="entry.mp3Url" class="radio"
              ><input v-model="entry.mp3Format" type="radio" value="keep" />
              Keep current MP3 file</label
            >
          </div>
        </div>

        <div class="field">
          <template v-if="entry.mp3Format === 'upload'">
            <div class="file has-name">
              <label class="file-label">
                <input
                  @change="setFile('mp3', $event)"
                  accept=".mp3"
                  class="file-input"
                  type="file"
                />
                <span class="file-cta">
                  <span class="file-icon">
                    <i class="fas fa-upload"></i>
                  </span>
                  <span class="file-label">
                    Upload MP3 File
                  </span>
                </span>
                <span v-if="entry.mp3File" class="file-name">
                  {{ entry.mp3File.name }}
                </span>
              </label>
            </div>
          </template>

          <template v-else-if="entry.mp3Format === 'external'">
            <label for="mp3Link"
              >If you have an external link to your submission (e.g.
              SoundCloud), you can enter that here.</label
            >
            <input type="text" v-model="entry.mp3Link" />

            <div v-if="mp3LinkError" class="error-message">
              {{ mp3LinkError }}
            </div>
          </template>

          <a v-else-if="entry.mp3Format === 'keep'" :href="entry.mp3Url"
            >Link to MP3</a
          >
        </div>

        <div class="field">
          <label class="label">Score format</label>
          <label class="radio"
            ><input v-model="entry.pdfFormat" type="radio" value="upload" />
            Upload PDF</label
          >
          <label v-show="entry.pdfUrl" class="radio"
            ><input v-model="entry.pdfFormat" type="radio" value="keep" /> Keep
            current PDF file</label
          >
        </div>

        <div class="field">
          <a v-if="entry.pdfFormat === 'keep'" :href="entry.pdfUrl"
            >Link to PDF</a
          >

          <div v-else-if="entry.pdfFormat === 'upload'" class="file has-name">
            <label class="file-label">
              <input
                @change="setFile('pdf', $event)"
                accept=".pdf"
                class="file-input"
                type="file"
              />
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-upload"></i>
                </span>
                <span class="file-label">
                  Upload PDF File
                </span>
              </span>
              <span v-if="entry.pdfFile" class="file-name">
                {{ entry.pdfFile.name }}
              </span>
            </label>
          </div>
        </div>

        <input
          class="button is-primary"
          type="submit"
          value="Submit Entry"
          :disabled="!valid"
        />
      </form>

      <template v-else-if="state === 'submitting'">
        <progress class="progress is-large" />
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Entry, EntryId, UserData } from "@/types";
import getValidHosts from "@/services/getValidHosts";
import postUserEntry, { SubmitRequest } from "@/services/postUserEntry";

function makeEmptyEntry(): Entry {
  return {
    entrantName: "",
    entryName: "",
    mp3Format: "",
    mp3Url: "",
    pdfUrl: "",
    uuid: "" as EntryId,
    pdfFormat: "",
    isValid: true
  };
}

export default Vue.extend({
  props: {
    user: Object as PropType<UserData>,
    initialEntry: Object as PropType<Entry>
  },
  data() {
    let entry = this.initialEntry || makeEmptyEntry();
    return {
      state: "blank",
      entry: {
        ...entry,
        mp3Format: "upload",
        mp3File: null,
        mp3Link: "",
        pdfFormat: "upload",
        pdfFile: null,
        isValid: true
      } as Record<string, any>, // TODO: Fix.
      validHosts: [] as Array<string>,
      error: null as null | string
    };
  },
  async mounted() {
    this.state = "loading";

    try {
      this.validHosts = await getValidHosts();
    } catch {
      this.error = "There was an issue, try reloading or notify an admin.";
    }

    this.state = "editing";
  },
  methods: {
    async submit(e: Event) {
      e.preventDefault();

      try {
        this.state = "submitting";

        const entry: SubmitRequest = {
          name: this.entry.entryName
        };

        if (this.entry.pdfFormat === "upload") {
          entry.pdfFile = this.entry.pdfFile;
        }

        if (this.entry.mp3Format === "upload") {
          entry.mp3File = this.entry.mp3File;
        } else if (this.entry.mp3Format === "external") {
          entry.mp3Link = this.entry.mp3Link;
        }

        const result = await postUserEntry(entry);

        this.$emit("update:entry", result);
      } catch (e) {
        alert(e.toString());
        this.state = "editing";
      }
    },
    setFile(type: string, event: InputEvent) {
      const element = event.target as HTMLInputElement;

      if (element === null) return;

      const files = element.files;

      if (files === null) return;

      let file = files[0];

      this.entry[type + "File"] = file;
    }
  },
  computed: {
    valid() {
      if (this.entry.entryName === "") {
        return false;
      }

      if (this.entry.pdfFormat === "upload" && this.entry.pdfFile === null) {
        return false;
      }

      if (this.entry.mp3Format === "external" && this.entry.mp3Link === "") {
        return false;
      }

      if (this.entry.mp3Format === "upload" && this.entry.mp3File === null) {
        return false;
      }

      return true;
    },
    mp3LinkError() {
      if (this.entry.mp3Link === "") {
        return "Link can't be empty.";
      }

      if (this.validHosts.some(host => this.entry.mp3Link.startsWith(host))) {
        return false;
      }

      return (
        "This audio hosting website is not in the approved list. " +
        `Please use one of these: ${this.validHosts.join(", ")}`
      );
    }
  }
});
</script>