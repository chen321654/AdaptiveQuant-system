<template>
    <el-container class="layout-container">
        <el-header height="auto" class="header">
            <el-menu :default-active="activeIndex" mode="horizontal" :ellipsis="false" @select="handleSelect"
                background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
                <el-menu-item index="0">
                    <img style="width: 50px" src="/stock.png" alt="行情中心" />
                </el-menu-item>

                <el-sub-menu index="1">
                    <template #title>A股市场</template>
                    <el-menu-item index="1-1">A股市场</el-menu-item>
                    <el-menu-item index="1-2">A股指数</el-menu-item>
                    <el-menu-item index="1-3">A股警示</el-menu-item>
                </el-sub-menu>

                <el-sub-menu index="2">
                    <template #title>板块</template>
                    <el-menu-item index="2-1">概念板块</el-menu-item>
                    <el-menu-item index="2-2">地狱板块</el-menu-item>
                    <el-menu-item index="2-3">同花顺行业</el-menu-item>
                    <el-menu-item index="2-4">见证会行业</el-menu-item>
                </el-sub-menu>

                <el-sub-menu index="3">
                    <template #title>数据中心</template>
                    <el-menu-item index="3-1">龙虎榜</el-menu-item>
                    <el-menu-item index="3-2">大宗交易</el-menu-item>
                    <el-menu-item index="3-3">新股申购</el-menu-item>
                </el-sub-menu>

                <el-menu-item index="4" style="margin-left: auto;">
                    <template v-if="isLoggedIn">
                        <span class="username">{{ username }}</span>
                        <el-button type="text" @click="handleLogout" style="color: #fff;">退出</el-button>
                    </template>
                    <el-button v-else type="text" @click="showModal('login')" style="color: #fff;">登录</el-button>
                </el-menu-item>
            </el-menu>
        </el-header>

        <el-container class="main-container">
            <el-main class="main-content">
                <el-aside width="200px">
                    <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
                        background-color="#f0f0f0" text-color="#000000" active-text-color="#ffd04b">
                        <el-menu-item index="1">
                            <el-icon><icon-menu /></el-icon>
                            <span>涨跌分布</span>
                        </el-menu-item>
                        <el-menu-item index="2">
                            <el-icon><icon-menu /></el-icon>
                            <span>涨跌停</span>
                        </el-menu-item>
                        <el-menu-item index="3">
                            <el-icon>
                                <setting />
                            </el-icon>
                            <span>昨日涨停今日收益</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <Stockindex ref="" />
            </el-main>
        </el-container>

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
    </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { Menu as IconMenu, Setting } from '@element-plus/icons-vue'
import Stockindex from './component/stockindex.vue'
import UserLogin from './account/UserLogin.vue'
import UserRegister from './account/UserRegister.vue'
import FindPassword from './account/FindPassword.vue'
import ResetPassword from './account/ResetPassword.vue'
import jsCookie from 'js-cookie'


const isModalVisible = ref(false)
const currentModal = ref('login')
const isLoggedIn = ref(false)
const username = ref('')
const activeIndex = ref('1')

const showModal = (modalType) => {
    currentModal.value = modalType
    isModalVisible.value = true
}

const closeModal = () => {
    isModalVisible.value = false
}

const handleLoginSuccess = () => {
    closeModal()
    isLoggedIn.value = true
    username.value = UserLogin.value.userData.value
}

const handleRegisterSuccess = () => {
    showModal('login')
}

const handleFindSuccess = () => {
    showModal('ResetPassword')
}

const handleResetSuccess = () => {
    showModal('login')
}

const handleLogout = () => {
    isLoggedIn.value = false
    username.value = ''
    jsCookie.remove('username')
    location.reload()
}

const handleSelect = (key, keyPath) => {
    console.log(key, keyPath)
}

const handleOpen = (key, keyPath) => {
    console.log(key, keyPath)
}

const handleClose = (key, keyPath) => {
    console.log(key, keyPath)
}
</script>

<style scoped>
.layout-container {
    min-height: 100vh;
}

.header {
    padding: 0;
}

/* .main-container {
    height: calc(100vh - 60px);
} */

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

.main-content {
    padding: 20px;
}

.username {
    font-weight: 500;
    margin-right: 0.5rem;
}

:deep(.el-menu) {
    border-right: none;
}

:deep(.el-menu--horizontal) {
    border-bottom: none;
}

:deep(.el-menu-item) {
    font-size: 14px;
}

.index-card {
    height: 100%;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* .el-row {
    margin-bottom: 20px;
}

.el-row:last-child {
    margin-bottom: 0;
}

.el-col {
    margin-bottom: 20px;
} */
</style>