import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from '@/components/Login.vue'
import SidebarLayout from '@/components/SidebarLayout.vue'
import SalesScreen from '@/components/SalesScreen.vue'
import ProductManagement from '@/components/ProductManagement.vue'
import SalesHistory from '@/components/SalesHistory.vue'

let cartIsNotEmpty = false;

export function setCartState(hasItems) {
  cartIsNotEmpty = hasItems;
}

const routes = [
  {
    path: '/login',
    component: LoginForm
  },
  {
    path: '/',
    component: SidebarLayout,
    children: [
      { path: 'sales', component: SalesScreen },
      { path: 'products', component: ProductManagement },
      { path: 'sales-history', component: SalesHistory }
    ]
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  if (to.path !== '/login' && !token) {
    return next('/login')
  }

  if (to.path === '/sales-history' && role !== 'admin') {
    alert('Access denied: Only admins can view sales history.')
    return next('/sales')
  }

  if (from.path === '/sales' && cartIsNotEmpty) {
    const confirmLeave = confirm('Cart is not empty. Are you sure you want to leave the Sales screen?')
    if (!confirmLeave) return next(false)
  }

  next()
})

export default router
