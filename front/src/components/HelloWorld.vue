<template>
  <div class="hello">
    <h1>Send a request</h1>
    <input type="text" v-model="get_key" />
    <input @click="get_data" type="button" value="GET" />
    <br />
    <p>{{ result }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HelloWorld",
  data() {
    return {
      get_key: "",
      post_key: "",
      post_val: "",
      result: "",
    };
  },
  methods: {
    get_data() {
      axios
        .get("http://127.0.0.1:8000/notes/", {
          params: {
            id: this.get_key,
          },
        })
        .then(
          function (response) {
            this.result = response.data;
            console.log(response);
          }.bind(this)
        )
        .catch(
          function (error) {
            this.result = "GETエラー";
            console.log(error);
          }.bind(this)
        );
    },
  },
};
</script>
