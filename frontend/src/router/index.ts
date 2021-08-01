import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Layout from '../components/Layout.vue'
import Home from '../pages/Home.vue'
import Week from '../pages/Week.vue'
import ErrorPage from '../pages/ErrorPage.vue'
import MySubmission from '../pages/MySubmission.vue'
import OauthDiscord from '../pages/DiscordOauth.vue'

Vue.use(VueRouter)

const routes: RouteConfig[] = [
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
        path: 'weeks/:which',
        component: Week
      },
      {
        path: 'mine',
        component: MySubmission,
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
