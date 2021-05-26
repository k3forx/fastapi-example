<template>
  <div class="editor">
    <h2>Title: {{ result.title }}</h2>
    <h3>Description: {{ result.description }}</h3>
    <button>
      <router-link :to="{ name: 'Edit', params: { id: result.id } }"
        >Edit</router-link
      >
    </button>
    <p></p>
    <button v-on:click="Delete">Delete</button>
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
    console.log(this.$notes);
    axios.get("http://127.0.0.1:8000/notes/" + id).then((response) => {
      this.result = response.data;
      console.log(response);
    });
  },
  methods: {
    Delete: function () {
      let id = this.result.id;
      console.log("delete" + id);
      axios.delete("http://127.0.0.1:8000/notes/" + id).then(() => {
        this.$router.push("/note");
      });
    },
  },
};
</script>
