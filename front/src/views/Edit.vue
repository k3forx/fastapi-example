<template>
  <div class="editor">
    <h1>Edit Memo</h1>
    <p>Title</p>
    <textarea name="memo" v-model="result.title"></textarea>

    <p>Description</p>
    <textarea name="memo-description" v-model="result.description"></textarea>
    <button v-on:click="Save">Save</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "edit",
  data() {
    return {
      result: {
        id: null,
        title: null,
        description: null,
      },
    };
  },
  created: function () {
    let id = this.$route.params["id"];
    axios.get("http://127.0.0.1:8000/notes/" + id).then((response) => {
      this.result = response.data;
    });
  },
  methods: {
    Save: function () {
      let id = this.result.id;
      let title = this.result.title;
      let description = this.result.description;
      axios
        .put("http://127.0.0.1:8000/notes/" + id, {
          title: title,
          description: description,
        })
        .then(() => {
          this.$router.push("/note");
        });
    },
  },
};
</script>
