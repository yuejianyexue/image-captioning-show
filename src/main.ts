
import { createApp } from 'vue'
import App from './App.vue'
import '@/assets/css/iconfont.css'

import '@/assets/css/main.css'
// 引入路由器
import router from './router'

// 创建一个应用
const app= createApp(App)

// 使用路由器
app.use(router)

// 挂载整个应用到APP容器中
app.mount('#app')

// 配置axios为全局对象
import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:8000'
// axios.defaults.baseURL = 'http://localhost:3000'
app.config.globalProperties.$axios = axios