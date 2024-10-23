<template>
    <div class="auth-container">
        <div class="form-container">
            <h2 class="title">重置密码</h2>
            <form class="form" @submit.prevent="handleSubmit">
                <div class="form-group">
                    <label for="newPassword" class="label">新密码</label>
                    <input id="newPassword" name="newPassword" type="password" autocomplete="new-password" required
                        v-model="newPassword" class="input" />
                </div>

                <div class="form-group">
                    <label for="confirmNewPassword" class="label">确认新密码</label>
                    <input id="confirmNewPassword" name="confirmNewPassword" type="password" autocomplete="new-password"
                        required v-model="confirmNewPassword" class="input" />
                </div>

                <div class="form-group">
                    <label for="captcha" class="label">验证码</label>
                    <div class="captcha-input-container">
                        <input id="captcha" name="captcha" type="text" required v-model="captcha"
                            class="input captcha-input" placeholder="输入验证码" />
                        <Captcha ref="captchaRef" />
                    </div>
                </div>

                <button type="submit" class="submit-button" :disabled="isSubmitting">
                    {{ isSubmitting ? '提交中...' : '重置密码' }}
                </button>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import Captcha from './Captcha.vue';
import jsCookie from 'js-cookie';

const emit = defineEmits(['resetSuccess'])

const newPassword = ref('')
const confirmNewPassword = ref('')
const captcha = ref('')
const isSubmitting = ref(false)

const handleSubmit = async () => {
    if (newPassword.value !== confirmNewPassword.value) {
        alert('新密码和确认新密码不匹配')
        return
    }

    isSubmitting.value = true

    try {
        const token = getToken()
        const response = await fetch('/User/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': jsCookie.get()
            },
            body: JSON.stringify({
                newPassword: newPassword.value,
                captcha: captcha.value
            })
        })

        if (response.ok) {
            alert('密码重置成功')
            emit('resetSuccess')
        } else {
            const errorData = await response.json()
            alert(errorData.message || '密码重置失败，请重试')
        }
    } catch (error) {
        console.error('密码重置错误:', error)
        alert('密码重置过程中发生错误，请重试')
    } finally {
        isSubmitting.value = false
    }
}
</script>

<style scoped>
@import '../../assets/auth.css';
</style>