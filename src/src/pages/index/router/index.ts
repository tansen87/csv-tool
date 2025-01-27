import router, { addRoutes, } from '@/router'
import Layout from '../layout/index.vue'

addRoutes(router, [{
  path: '/login',
  component: () => import('@p-index/views/login/index.vue'),
}, {
  name: 'Layout',
  path: '/',
  component: Layout,
  children: [
    {
      path: '',
      component: () => import('@p-index/views/dashboard/index.vue'),
    },
    {
      path: 'icon',
      component: () => import('@p-index/views/icon/index.vue'),
    },
    {
      path: 'datetime',
      component: () => import('@p-index/views/datetime/index.vue'),
    },
    {
      path: 'table',
      component: () => import('@p-index/views/table/index.vue'),
    },
  ],
}])

export default router
