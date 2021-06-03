import Vuex from "vuex";
import userModule from "./modules/user";
import createPersistedState from "vuex-persistedstate";

export default new Vuex.Store({
  modules: {
    userModule,
  },
  plugins: [
    createPersistedState({
      key: "token",
      paths: ["userModule.access_token"],
      storage: window.sessionStorage,
    }),
  ],
});
