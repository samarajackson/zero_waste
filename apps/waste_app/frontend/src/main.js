// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { store } from './store/store'
import VueCookies from 'vue-cookies'

// vue cookies settings
Vue.use(VueCookies)
Vue.$cookies.config('7d')
Vue.config.productionTip = false

// Axios Config settings
axios.defaults.baseURL = 'http://localhost:8000/'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

/* eslint-disable no-new */
// eslint-disable-next-line no-unused-vars
const app = new Vue({
  router,
  components: { App },
  template: '<App/>',
  store
}).$mount('#app')
