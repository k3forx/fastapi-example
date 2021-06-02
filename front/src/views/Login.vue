<template>
  <div class="login">
    <h1>Welcome</h1>

    <input type="text" placeholder="Username" v-model="user.username" />
    <br />
    <input type="password" placeholder="Password" v-model="user.password" />
    <br />
    <button v-on:click="Login">Login</button>
    <br />
    <button v-on:click="Register">Register</button>
  </div>
</template>

<script>
import axios from "axios";
import oauth from "axios-oauth-client";

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
    Login: function () {
      let username = this.user.username;
      let password = this.user.password;

      const getAuthorizationCode = oauth.client(axios.create(), {
        url: "http://127.0.0.1:8000/token",
        username: username,
        password: password,
      });

      getAuthorizationCode().then((response) => {
        this.$store.state.userModule.access_token = response.access_token;
        // sessionStorage.setItem("token", response.access_token)
        this.$store.commit("save_access_token", response.access_token);
        console.log("saved token");
        this.$router.push({ path: "/note" });
      });
    },
    Register: function () {
      this.$router.push({ path: "/register" });
    },
  },
};
</script>
