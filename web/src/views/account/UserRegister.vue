<template>
    <div class="auth-container">
        <div class="form-container">
            <h2 class="title">创建新账户</h2>
            <form class="form" @submit.prevent="handleSubmit">
                <div class="form-group">
                    <label for="username" class="label">用户名</label>
                    <input id="username" name="username" type="text" autocomplete="nickname" required v-model="username"
                        class="input" />
                </div>
                <div class="form-group">
                    <label for="email" class="label">电子邮箱</label>
                    <input id="email" name="email" type="email" autocomplete="email" required v-model="email"
                        class="input" />
                </div>

                <div class="form-group">
                    <label for="captcha" class="label">验证码</label>
                    <div class="captcha-input-container">
                        <input id="captcha" name="captcha" type="text" required v-model="captcha"
                            class="input captcha-input" placeholder="输入验证码" />
                        <button type="button" class="send-captcha-button" @click="sendCaptcha"
                            :disabled="isSendingCaptcha || countdown > 0">
                            {{ buttonText }}
                        </button>
                    </div>
                </div>

                <div class="form-group">
                    <label for="password" class="label">密码</label>
                    <input id="password" name="password" type="password" autocomplete="new-password" required
                        v-model="password" class="input" />
                </div>

                <div class="form-group">
                    <label for="confirmPassword" class="label">确认密码</label>
                    <input id="confirmPassword" name="confirmPassword" type="password" autocomplete="new-password"
                        required v-model="confirmPassword" class="input" />
                </div>

                <button type="submit" class="submit-button" :disabled="isLoading">
                    {{ isLoading ? '注册中...' : '注册' }}
                </button>
            </form>

            <div class="divider">
                <span class="divider-text">已有账户？</span>
            </div>

            <div class="links-container">
                <button @click="$emit('showLogin')" class="link-button full-width-link">登录</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const emit = defineEmits(['showLogin', 'registerSuccess'])
const isSendingCaptcha = ref(false)
const countdown = ref(0)

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const captcha = ref('')
const isLoading = ref(false)

const buttonText = computed(() => {
    if (isSendingCaptcha.value) {
        return '发送中...'
    } else if (countdown.value > 0) {
        return `${countdown.value}秒后重新发送`
    } else {
        return '发送验证码'
    }
})

const startCountdown = () => {
    countdown.value = 60
    const timer = setInterval(() => {
        countdown.value--
        if (countdown.value === 0) {
            clearInterval(timer)
        }
    }, 1000)
}

const sendCaptcha = async () => {
    if (!email.value) {
        alert('请输入邮箱地址')
        return
    }

    isSendingCaptcha.value = true
    try {
        const response = await axios.get('/User/retrieve/', {
            params: { email: email.value }
        })

        if (response.status === 200) {
            alert('验证码已发送，请查看您的邮箱')
            startCountdown()
        } else {
            alert(response.data.message || '发送验证码失败，请重试')
        }
    } catch (error) {
        console.error('发送验证码错误:', error)
        alert('发送验证码时出现错误，请重试')
    } finally {
        isSendingCaptcha.value = false
    }
}

const handleSubmit = async () => {
    if (password.value !== confirmPassword.value) {
        alert('密码和确认密码不匹配')
        return
    }

    isLoading.value = true
    try {
        const response = await axios.post('/User/register/', {
            username: username.value,
            email: email.value,
            passwd: password.value,
            passwd_v: confirmPassword.value,
            email_code: captcha.value
        })

        if (response.data.code === '200') {
            console.log('Registration successful', response.data)
            emit('registerSuccess')
        } else {
            alert(response.data.msg)
            captcha.value = ''
        }
    } catch (error) {
        console.error('Registration error:', error)
        alert('注册过程中发生错误，请重试')
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
@import '../../assets/auth.css';

.captcha-input-container {
    display: flex;
    gap: 0.5rem;
}

.captcha-input {
    flex: 1;
}

.send-captcha-button {
    background-color: #4338ca;
    color: white;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: background-color 0.15s ease-in-out;
    white-space: nowrap;
    min-width: 120px;
}

.send-captcha-button:hover:not(:disabled) {
    background-color: #3730a3;
}

.send-captcha-button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
}
</style>