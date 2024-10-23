<template>
    <div class="captcha-container">
        <img v-if="captchaUrl" :src="captchaUrl" alt="验证码" @click="refreshCaptcha" class="captcha-image" />
        <div v-else class="captcha-placeholder">加载中...</div>
        <button type="button" class="refresh-button" @click="refreshCaptcha" aria-label="刷新验证码">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.3" />
            </svg>
        </button>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';

const captchaUrl = ref('');
const captchaId = ref('');
const fetchCaptcha = async () => {
    try {
        const response = await axios.get('/User/login');
        // captchaUrl.value = 'https://pic.616pic.com/ys_bnew_img/00/29/79/9UMK4fzdwr.jpg  '
        captchaUrl.value = 'http://127.0.0.1:8000' + response.data.data.image_url;
        captchaId.value = response.data.data.hashkey;

    } catch (error) {
        console.error('Failed to fetch captcha:', error);
    }
};

const refreshCaptcha = () => {
    fetchCaptcha();
};

onMounted(() => {
    fetchCaptcha();
});

defineExpose({ refreshCaptcha, captchaId });
</script>

<style scoped>
.captcha-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.captcha-image {
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    width: 120px;
    height: 40px;
    object-fit: cover;
    cursor: pointer;
}

.captcha-placeholder {
    width: 120px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    color: #6b7280;
}

.refresh-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    padding: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4f46e5;
}

.refresh-button:hover {
    color: #4338ca;
}
</style>