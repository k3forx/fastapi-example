<template>
  <div class="editor">
    <h1>New Memo</h1>
    <p>Title</p>
    <textarea name="memo" v-model="memo.title"></textarea>
    <p>Description</p>
    <textarea name="memo" v-model="memo.description"></textarea>
    <p></p>
    <button @click="save">Save</button>
  </div>
</template>

<style scoped>
textarea {
  width: 20%;
  height: 5em;
}
button {
  border: 1px solid #333;
  background-color: #333;
  color: #fff;
  padding: 10px 10px;
  margin-top: 5px;
}
</style>

<script>
import Axios from "axios";

export default {
  name: "new",
  data() {
    return {
      memo: {
        title: null,
        description: null,
      },
    };
  },
  methods: {
    save: function () {
      let title = this.memo.title;
      let description = this.memo.description;
      var axios = Axios.create({
        headers: {
          accept: "application/json",
          Authorization: "Bearer " + this.$store.state.userModule.access_token,
        },
        responseType: "json",
      });
      axios
        .post("http://127.0.0.1:8000/notes/", {
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
