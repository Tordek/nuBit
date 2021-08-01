import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Tooltip from "v-tooltip"

Vue.config.productionTip = false
Vue.use(Tooltip)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
