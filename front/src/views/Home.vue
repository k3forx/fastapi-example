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
import axios from "axios";

export default {
  name: "Home",
  data() {
    return {
      notes: null,
    };
  },
  created: function () {
    axios.get("http://127.0.0.1:8000/notes").then((response) => {
      this.notes = response.data.notes.reverse();
      console.log(response);
    });
  },
};
</script>
