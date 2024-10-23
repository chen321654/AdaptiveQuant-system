<template>
    <div class="auth-container">
        <div class="form-container">
            <h2 class="title">找回密码</h2>
            <form class="form" @submit.prevent="handleSubmit">
                <div class="form-group">
                    <label for="email" class="label">邮箱</label>
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

                <button type="submit" class="submit-button" :disabled="isSubmitting">
                    {{ isSubmitting ? '提交中...' : '重置密码' }}
                </button>
            </form>

            <div class="divider">
                <span class="divider-text">或者</span>
            </div>

            <div class="links-container">
                <button @click="$emit('showLogin')" class="link-button">返回登录</button>
                <button @click="$emit('showRegister')" class="link-button">创建账户</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const emit = defineEmits(['showLogin', 'showRegister', 'resetSuccess'])

const email = ref('')
const captcha = ref('')
const isSendingCaptcha = ref(false)
const isSubmitting = ref(false)
const countdown = ref(0)

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
    if (!email.value || !captcha.value) {
        alert('请填写所有必填字段')
        return
    }

    isSubmitting.value = true
    try {
        const response = await axios.post('/User/retrieve/', {
            email: email.value,
            captcha: captcha.value,
        })

        if (response.status === 200) {
            emit('resetSuccess')
        } else {
            alert(response.data.message || '重置密码失败，请重试')
        }
    } catch (error) {
        console.error('重置密码错误:', error)
        alert('重置密码时出现错误，请重试')
    } finally {
        isSubmitting.value = false
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
    background-color: #4f46e5;
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
    background-color: #4338ca;
}

.send-captcha-button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
}
</style>