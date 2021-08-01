import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Layout from '../components/Layout.vue'
import Home from '../pages/Home.vue'
import Week from '../pages/Week.vue'
import ErrorPage from '../pages/ErrorPage.vue'
import MySubmission from '../pages/MySubmission.vue'
import MyResults from '../pages/MyResults.vue'
import OauthDiscord from '../pages/DiscordOauth.vue'
import Admin from '../pages/Admin.vue'

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
        component: Week,
        props: true
      },
      {
        path: 'mine',
        component: MySubmission,
      },
      {
        path: 'results',
        component: MyResults,
      },
      {
        path: 'admin',
        component: Admin
      }
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
