<template>
    <div class="auth-container">
        <div class="form-container">
            <h2 class="title">登录您的账户</h2>
            <form class="form" @submit.prevent="handleSubmit">
                <div class="form-group">
                    <label for="username" class="label">用户名</label>
                    <input id="username" name="username" type="text" autocomplete="nickname" required v-model="Text"
                        class="input" />
                </div>

                <div class="form-group">
                    <label for="password" class="label">密码</label>
                    <input id="password" name="password" type="password" autocomplete="current-password" required
                        v-model="password" class="input" />
                </div>

                <div class="form-group">
                    <label for="captcha" class="label">验证码</label>
                    <div class="captcha-input-container">
                        <input id="captcha" name="captcha" type="text" required v-model="captcha"
                            class="input captcha-input" placeholder="输入验证码" />
                        <Captcha ref="captchaRef" />
                    </div>
                </div>

                <button type="submit" class="submit-button" :disabled="isLoading">
                    {{ isLoading ? '登录中...' : '登录' }}
                </button>
            </form>

            <div class="divider">
                <span class="divider-text">或者</span>
            </div>

            <div class="links-container">
                <button @click="$emit('showRegister')" class="link-button">注册</button>
                <button @click="$emit('showFindPassword')" class="link-button">找回密码</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import Captcha from './Captcha.vue';
import jsCookie from 'js-cookie';


const emit = defineEmits(['showRegister', 'showFindPassword', 'loginSuccess'])
const username = ref('')
const password = ref('')
const captcha = ref('')
const captchaRef = ref(null)
const isLoading = ref(false)
var userData = ref('')
const handleSubmit = async () => {
    isLoading.value = true

    try {
        const response = await fetch('http://127.0.0.1:8000/User/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
                captcha: captcha.value,
                hashkey: captchaRef.value.captchaId.value,
            }),
        })

        const data = await response.json()

        if (data.code == '200') {
            console.log('Login successful', data)
            userData = response.headers.get('username')
            jsCookie.set(response.headers.get('username'), response.headers.get('sessionid'))

            emit('loginSuccess')
        } else {
            alert(data.msg)
            captchaRef.value.refreshCaptcha()
            captcha.value = ''
        }

    } catch (error) {
        console.error('Login error:', error)
        alert('登录过程中发生错误，请重试')
    } finally {
        isLoading.value = false
    }

}
</script>

<style scoped>
@import '../../assets/auth.css';
</style>