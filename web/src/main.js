import { createApp } from 'vue'
//element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

//import store from './stores'
//创建实例
const app = createApp(App)
//全局应用配置
app.config.globalProperties.$axios = axios
app.use(ElementPlus).use(router).mount('#app')