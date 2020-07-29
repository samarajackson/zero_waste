import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    userid: '',
    user: {}
  },
  mutations: {
    changeid (state, userid) {
      state.userid = userid
    },
    updateuser (state, user) {
      state.user = user
    }
  },
  getters: {
    userid: state => { return (state.userid) },
    user: state => state.user
  }
})
