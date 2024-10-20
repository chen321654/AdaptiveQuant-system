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
                            :disabled="isSendingCaptcha">
                            {{ isSendingCaptcha ? '发送中...' : '发送验证码' }}
                        </button>
                    </div>
                </div>

                <button type="submit" class="submit-button" :disabled="isSubmitting" @click="ResetPassword">
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
import { ref } from 'vue'
import ResetPassword from './ResetPassword.vue';

const emit = defineEmits(['showLogin', 'showRegister', 'resetSuccess'])

const email = ref('')
const captcha = ref('')
const isSendingCaptcha = ref(false)
const isSubmitting = ref(false)

const sendCaptcha = async () => {
    if (!email.value) {
        alert('请输入邮箱地址')
        return
    }

    isSendingCaptcha.value = true
    try {
        const response = await fetch('http://127.0.0.1:8000/User/retrieve/', {
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email.value }),
        })

        if (response.ok) {
            alert('验证码已发送，请查看您的邮箱')
        } else {
            const errorData = await response.json()
            alert(errorData.message || '发送验证码失败，请重试')
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
        const response = await fetch('http://127.0.0.1:8000/User/retrieve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email.value,
                captcha: captcha.value,
            }),
        })

        if (response.ok) {

            emit('findSuccess')
        } else {
            const errorData = await response.json()
            alert(errorData.message || '重置密码失败，请重试')
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
}

.send-captcha-button:hover:not(:disabled) {
    background-color: #4338ca;
}

.send-captcha-button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
}
</style>