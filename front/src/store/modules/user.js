const state = {
  access_token: "",
  user_id: 0,
};

const mutations = {
  save_access_token(state, token) {
    state.access_token = token;
  },
};

export default {
  state,
  mutations,
};
