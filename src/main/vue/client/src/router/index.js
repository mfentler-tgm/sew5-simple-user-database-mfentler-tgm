import Vue from 'vue'
import Router from 'vue-router'
import User from '@/components/User'
import 'bootstrap/dist/css/bootstrap.css'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'User',
      component: User
    }
  ],
  mode: 'history'
})
