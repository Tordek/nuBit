import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Layout from '../components/Layout.vue'
import Home from '../pages/Home.vue'
import Week from '../pages/Week.vue'
import ErrorPage from '../pages/ErrorPage.vue'
import Submit from '../pages/Submit.vue'
import OauthDiscord from '../pages/DiscordOauth.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/oauth/discord',
    name: "OauthDiscord",
    component: OauthDiscord,
  },
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        component: Home
      },
      {
        path: 'week/:which',
        component: Week
      },
      {
        path: 'submit',
        component: Submit
      },
    ]
  },
  {
    path: '*',
    component: ErrorPage
  }
]

const router = new VueRouter({
  routes,
  mode: 'history',
})

export default router
