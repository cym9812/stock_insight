<script setup lang="ts">
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <div class="app-container">
    <nav class="sidebar glass-card">
      <div class="logo">
        <span class="logo-icon">💠</span>
        <h1>Antigravity <span class="sub">Insight</span></h1>
      </div>
      <ul class="nav-links">
        <li>
          <router-link to="/dashboard" :class="{ active: route.path === '/dashboard' }">
            <span class="icon">📊</span> Market Overview
          </router-link>
        </li>
        <li>
          <router-link to="/strategy" :class="{ active: route.path === '/strategy' }">
            <span class="icon">🎯</span> Strategy Center
          </router-link>
        </li>
        <li>
          <router-link to="/stock" :class="{ active: route.path.startsWith('/stock') }">
            <span class="icon">📈</span> Stock Analysis
          </router-link>
        </li>
        <li>
          <router-link to="/portfolio" :class="{ active: route.path === '/portfolio' }">
            <span class="icon">💼</span> Portfolio
          </router-link>
        </li>
      </ul>
      
      <div class="sidebar-footer">
        <div class="user-profile">
          <div class="avatar">UX</div>
          <div class="info">
            <span class="name">Premium User</span>
            <span class="status">AI Active</span>
          </div>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--bg-dark);
}

.sidebar {
  width: 280px;
  margin: 20px;
  display: flex;
  flex-direction: column;
  padding: 32px 24px;
  border-radius: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 60px;
}

.logo-icon {
  font-size: 1.8rem;
  filter: drop-shadow(0 0 8px var(--accent));
}

.logo h1 {
  font-size: 1.4rem;
  margin: 0;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.logo h1 .sub {
  color: var(--text-muted);
  font-weight: 400;
  font-size: 1.1rem;
}

.nav-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.nav-links a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  color: var(--text-muted);
  text-decoration: none;
  border-radius: 14px;
  transition: var(--transition);
  font-weight: 600;
  font-size: 0.95rem;
}

.nav-links a .icon {
  font-size: 1.2rem;
  opacity: 0.7;
}

.nav-links a:hover {
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-main);
  transform: translateX(6px);
}

.nav-links a.active {
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
  color: var(--accent);
  box-shadow: inset 0 0 0 1px rgba(56, 189, 248, 0.2);
}

.nav-links a.active .icon {
  opacity: 1;
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: white;
  font-size: 0.8rem;
}

.info {
  display: flex;
  flex-direction: column;
}

.name {
  font-weight: 700;
  font-size: 0.9rem;
}

.status {
  font-size: 0.7rem;
  color: var(--up-color);
  font-weight: 600;
}

.main-content {
  flex: 1;
  padding: 20px 20px 20px 0;
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
