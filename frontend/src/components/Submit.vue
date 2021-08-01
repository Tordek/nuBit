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
            <p>
            <input v-model="entry.mp3Link" type="text" id="mp3Link" class="input" />
            </p>
            <p><label for="mp3Link"
              >If you have an external link to your submission (e.g.
              SoundCloud), you can enter that here.</label
            ></p>
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

        <div v-if="!valid" class="message is-warning">
          <div class="message-header">Hold up!</div>
          <div class="message-body">
            <p v-for="error in Object.values(errors)" :key="error">
              {{ error }}
            </p>
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

export default Vue.extend({
  props: {
    user: Object as PropType<UserData>,
    initialEntry: Object as PropType<Entry>
  },
  data() {
    let entry;
    if (this.initialEntry === null) {
      entry = {
        entrantName: "",
        entryName: "",
        mp3Url: "",
        pdfUrl: "",
        uuid: "" as EntryId,
        isValid: true,
        mp3Format: "upload",
        mp3File: null,
        mp3Link: "",
        pdfFormat: "upload",
        pdfFile: null
      };
    } else {
      entry = {
        ...this.initialEntry,
        mp3Format: "keep",
        mp3File: null,
        mp3Link: "",
        pdfFormat: "keep",
        pdfFile: null
      };
    }

    return {
      state: "blank",
      entry: entry as Record<string, any>, // TODO: Fix.
      validHosts: [] as string[],
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
    errors() {
      const errors = {} as Record<string, string>;

      if (this.entry.entryName === "") {
        errors["entryName"] = "The entry name can't be blank";
      }

      if (this.entry.pdfFormat === "upload" && this.entry.pdfFile === null) {
        errors["pdf"] = "You haven't chosen a PDF file";
      }

      if (this.entry.mp3Format === "external") {
        if (this.entry.mp3Link === "") {
          errors["mp3"] = "The MP3 link can't be empty";
        } else if (
          !this.validHosts.some(host => this.entry.mp3Link.startsWith(host))
        ) {
          errors["mp3"] =
            "This audio hosting website is not in the approved list. " +
            `Please use one of these: ${this.validHosts.join(", ")}`;
        }
      }

      if (this.entry.mp3Format === "upload" && this.entry.mp3File === null) {
        errors["mp3"] = "You haven't chosen an MP3 file";
      }

      return errors;
    },
    valid() {
      return Object.keys(this.errors).length === 0;
    }
  }
});
</script>