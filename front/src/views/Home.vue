<template>
  <div class="home">
    <ul v-for="note in notes" :key="note.id">
      <li>
        <router-link :to="{ name: 'List', params: { id: note.id } }">{{
          note.title
        }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import Axios from "axios";

export default {
  name: "Home",
  data() {
    return {
      notes: null,
    };
  },
  created: function () {
    var axios = Axios.create({
      headers: {
        accept: "application/json",
        Authorization: "Bearer " + this.$store.state.userModule.access_token,
      },
      responseType: "json",
    });
    axios.get("http://127.0.0.1:8000/notes").then((response) => {
      this.notes = response.data.notes.reverse();
    });
  },
};
</script>
