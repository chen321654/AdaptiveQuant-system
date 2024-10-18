<template>
    <div class="page-container">
        <header class="header">
            <div class="login-container">
                <template v-if="isLoggedIn">
                    <span class="username">{{ username }}</span>
                    <span class="separator">|</span>
                    <button class="logout-button" @click="handleLogout">退出</button>
                </template>
                <button v-else class="login-button" @click="showModal('login')">登录</button>
            </div>
        </header>
        <main class="main-content">
            <h1>欢迎来到我的网站</h1>
            <p>这里是网站的主要内容区域。</p>
        </main>

        <!-- Modal -->
        <div v-if="isModalVisible" class="modal-overlay" @click.self="closeModal">
            <UserLogin v-if="currentModal === 'login'" @showRegister="showModal('register')"
                @showFindPassword="showModal('FindPassword')" @loginSuccess="handleLoginSuccess" />
            <UserRegister v-if="currentModal === 'register'" @showLogin="showModal('login')"
                @registerSuccess="handleRegisterSuccess" />
            <FindPassword v-if="currentModal === 'FindPassword'" @showLogin="showModal('login')"
                @showRegister="showModal('register')" @findSuccess="handleFindSuccess" />
            <ResetPassword v-if="currentModal === 'ResetPassword'" @resetSuccess="handleResetSuccess" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import UserLogin from './account/UserLogin.vue'
import UserRegister from './account/UserRegister.vue'
import FindPassword from './account/FindPassword.vue'
import ResetPassword from './account/ResetPassword.vue'
import jsCookie from 'js-cookie';

const isModalVisible = ref(false)
const currentModal = ref('login')
const isLoggedIn = ref(false)
const username = ref('')

const showModal = (modalType) => {
    currentModal.value = modalType
    isModalVisible.value = true
}

const closeModal = () => {
    isModalVisible.value = false
}

const handleLoginSuccess = (userData) => {
    closeModal()
    isLoggedIn.value = true
    //username.value = UserLogin.value.userData.value
    username.value = "123456@qq.com"
}

const handleRegisterSuccess = () => {
    showModal('login')
}
const handleFindSuccess = () => {
    showModal('ResetPassword')
}
const handleResetSuccess = () => {
    showModal('Login')
}

const handleLogout = () => {
    isLoggedIn.value = false
    username.value = ''
    jsCookie.remove('username');
    location.reload();
}
</script>

<style scoped>
/* @import '@/assets/auth.css'; */

.page-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.header {
    padding: 1rem;
    background-color: #f0f2f5;
}

.login-container {
    display: flex;
    justify-content: flex-end;
}

.login-button {
    background-color: #4f46e5;
    color: white;
    font-weight: 500;
    padding: 0.625rem 1.25rem;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: background-color 0.15s ease-in-out;
}

.login-button:hover {
    background-color: #4338ca;
}

.main-content {
    flex-grow: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.username {
    font-weight: 500;
    margin-right: 0.5rem;
}

.separator {
    margin: 0 0.5rem;
    color: #6b7280;
}

.logout-button {
    background-color: transparent;
    color: #4f46e5;
    font-weight: 500;
    padding: 0.25rem 0.5rem;
    border: none;
    cursor: pointer;
    transition: color 0.15s ease-in-out;
}

.logout-button:hover {
    color: #4338ca;
}
</style>