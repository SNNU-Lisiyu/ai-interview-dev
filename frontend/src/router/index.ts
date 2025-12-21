import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layout/MainLayout.vue'
import HRLayout from '../layout/HRLayout.vue'
import Home from '../views/Home.vue'
import Welcome from '../views/Welcome.vue'

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: Welcome
  },
  {
    path: '/candidate',
    component: MainLayout,
    redirect: '/candidate/interview',
    children: [
      {
        path: 'home',
        name: 'Home',
        component: Home
      },
      {
        path: 'interview',
        name: 'Interview',
        component: () => import('../views/Interview.vue')
      },
      {
        path: 'report',
        name: 'Report',
        component: () => import('../views/Report.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/Profile.vue')
      }
    ]
  },
  {
    path: '/hr',
    component: HRLayout,
    redirect: '/hr/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'HRDashboard',
        component: () => import('../views/hr/Dashboard.vue')
      },
      {
        path: 'candidates',
        name: 'HRCandidates',
        component: () => import('../views/hr/CandidateList.vue')
      },
      {
        path: 'candidates/:id',
        name: 'HRCandidateDetail',
        component: () => import('../views/hr/CandidateDetail.vue')
      },
      {
        path: 'jobs',
        name: 'HRJobs',
        component: () => import('../views/hr/JobList.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory('/ai-interview/'),
  routes
})

export default router
