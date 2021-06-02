<template>
  <div class="login">
    <h1>Register</h1>
    <input type="text" placeholder="Username" v-model="user.username" />
    <br />
    <input type="password" placeholder="Password" v-model="user.password" />
    <br />
    <button v-on:click="Register">Register</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "login",
  data() {
    return {
      user: {
        username: null,
        password: null,
      },
    };
  },
  methods: {
    Register: function () {
      let username = this.user.username;
      let password = this.user.password;
      axios
        .post("http://127.0.0.1:8000/register", {
          username: username,
          raw_password: password,
        })
        .then(() => {
          this.$router.push("/");
        });
    },
  },
};
</script>
