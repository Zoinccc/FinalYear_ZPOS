<template>
  <div class="layout">
    <nav class="sidebar">
      <h2>Z-POS</h2>
      <ul class="nav-links">
        <li><router-link to="/sales">Sales</router-link></li>
        <li><router-link to="/products">Products</router-link></li>
        <li><router-link to="/sales-history">Sales History</router-link></li>
        <li><a href="#" @click="logout">Logout</a></li>
      </ul>
      <div class="logged-in-user">
        Logged in as: <strong>{{ username }}</strong>
      </div>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'SidebarLayout',
  data() {
    return {
      username: ''
    }
  },
  mounted() {
    this.username = localStorage.getItem('username') || 'Unknown'
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      window.location.href = '/login'
    }
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #1a1f36;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.nav-links {
  list-style: none;
  padding: 0;
}

.nav-links li {
  margin: 20px 0;
}

.sidebar a {
  color: white;
  text-decoration: none;
}

.content {
  flex: 1;
  padding: 30px;
  background-color: #f4f6f8;
}

.logged-in-user {
  font-size: 13px;
  color: #bbb;
  padding-top: 10px;
}
</style>
