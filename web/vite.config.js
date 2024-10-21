import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    // 是否开启 https
    https: false,
    // 设置反向代理，跨域
    proxy: {
      '/User': {
        // 后台地址
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
        bypass(req, res, options) {
          const proxyURL = options.target + options.rewrite(req.url)
          res.setHeader('x-req-proxyURL', proxyURL) // 将真实请求地址设置到响应头中
        },
        rewrite: (path) => path.replace(/^\/User/, 'User')
      },
      '/data': {
        // 后台地址
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true
        // rewrite: (path) => path.replace(/^\/data/, '')
      }
    }
  }
})
