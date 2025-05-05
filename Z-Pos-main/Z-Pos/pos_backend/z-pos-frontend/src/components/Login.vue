<template>
  <div class="login-container">
    <img src="@/assets/logo.png" alt="Z-POS Logo" class="logo" />
    <div class="login-card">
      <form @submit.prevent="login">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/token/', {
          username: this.username,
          password: this.password
        });

        const { token, role } = response.data;

        localStorage.setItem('token', token);
        localStorage.setItem('role', role);
        localStorage.setItem('username', this.username);

        alert(`Login successful as ${role}!`);
        this.$router.push('/sales');

      } catch (err) {
        this.error = 'Invalid credentials!';
      }
    }
  }
}
</script>

<style scoped>
html, body {
  overflow: hidden;
  margin: 0;
  padding: 0;
}

.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 70vh;
  background-color: #f4f6f8;
}

.logo {
  width: 180px;
  margin-bottom: 20px;
}

.login-card {
  background-color: #1a1f36;
  padding: 50px 40px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 280px;
  text-align: center;
}

input {
  width: 100%;
  padding: 10px;
  margin: 15px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #ffffff;
  color: #1a1f36;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

button:hover {
  background-color: #d9d9d9;
}

.error {
  color: #ff4d4d;
  margin-top: 15px;
}
</style>

<style>
html, body {
  overflow: hidden;
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #f4f6f8;
}
#app {
  height: 100%;
}
</style>
