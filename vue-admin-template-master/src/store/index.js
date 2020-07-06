// import Vue from 'vue'
// import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
import usermg from './management/usermg'
import datamg from './management/datamg'
// Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    usermg,
    datamg,
  },
  getters
})

export default store
