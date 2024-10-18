import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView
    },

    {
      path: '/Login',
      name: 'Login',
      component: () => import('../views/account/UserLogin.vue')
    },
    {
      path: '/Register',
      name: 'Register',
      component: () => import('../views/account/UserRegister.vue')
    },
    {
      path: '/ResetPassword',
      name: 'ResetPassword',
      component: () => import('../views/account/ResetPassword.vue')
    },
    {
      path: '/FindPassword',
      name: 'FindPassword',
      component: () => import('../views/account/FindPassword.vue')
    },
    {
      path: '/PersonalCenter',
      name: 'PersonalCenter',
      component: () => import('../views/personalcenter/PersonalCenter.vue')
    }
  ]
})

export default router
