<template>
  <div class="app">
    <!-- 顶部导航区 -->
    <div class='title'>
      <!-- <RouterLink replace :to="{ path: '/home' }" active-class="active"><span>首页</span></RouterLink> -->
      <div class="name">Image<p>Captioning</p>
      </div>
      <div class="button">
        <li class="icon">
          <a href="#">
            <div class="iconfont icon-shujutansuo"></div>
            <span>探索</span>
          </a>
          <div class="dropdown">
            <a href="#" @click="random(0)">其他用户</a>
            <a href="#" @click="random(1)">数据库</a>
          </div>
        </li>
        <li v-if="userStore.userID" class="icon">
          <a href="#">
            <div class="iconfont icon-denglu"> </div>
            <span>个人中心</span>
          </a>
          <div class="dropdown">
            <a href="#" :to="{ path: '/personage' }" >我的信息</a>
            <a href="#" >足迹</a>
          </div>
        </li>
        <li v-else class="icon">
          <a href="#">
            <div class="iconfont icon-denglu2"> </div>
            <span>登录</span>
          </a>
          <div class="dropdown">
            <a href="#" @click="showlogin">登录</a>
            <a href="#" @click="showregister">注册</a>
          </div>
        </li>
        <RouterLink :to="userStore.userID ? '/personage' : '#'"  class="username">{{ userStore.userID ? userStore.username : '用户尚未登录' }}</RouterLink>

      </div>
    </div>
    <!--正文层-->
    <!-- 导航区 -->
    <div class="navigate">
      <RouterLink replace :to="{ path: '/home' }" active-class="active"><span>首页</span></RouterLink>
      <RouterLink replace :to="{ path: '/upcaption' }" active-class="active">描述图像</RouterLink>
      <RouterLink replace :to="{ path: '/lookdata' }" active-class="active">数据库</RouterLink>
      <RouterLink replace :to="{ path: '/about' }" active-class="active">关于</RouterLink>
    </div>
    <!-- 展示区 -->
    <div class="bock">
      <div class="main-content">
        <RouterView></RouterView>
      </div>
    </div>
    <!-- 登录组件 -->
    <div v-if="loginShow" class="login-modal">
      <div class="login-form">
        <h2>用户登录</h2>
        
        <input type="text" v-model="loginUsername" placeholder="用户名" class="input-field">
        
        <input type="password" v-model="loginPassword" placeholder="密码" class="input-field">
        <div class="loginBox">
          <button @click="login" class="login-button">登录</button>
          还没有账号？
          <button @click="showregister" class="register-button">立即注册</button>
        </div>
      </div>
    </div>
    <!-- 注册组件 -->
    <div v-if="registerShow" class="login-modal">
      <div class="login-form">
        <h2>用户注册</h2>
        <el-form :model="form" ref="formRef" :rules="rules" label-width="auto" style="max-width: 600px">
        <el-form-item label="用户名" prop="regusername">
          <el-input v-model="form.regusername" />
        </el-form-item>
        <el-form-item label="密码" prop="regpassword">
          <el-input show-password v-model="form.regpassword" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input show-password v-model="form.confirmPassword" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="register">注册</el-button>
        </el-form-item>
      </el-form>
        <p v-if="passwordsMatch">密码匹配</p>
        <p v-else>密码不匹配</p>
        <div class="loginBox">
        </div>
      </div>
    </div>
    <div v-if='imageSrc' class="showImage">
    <img  :src="imageSrc" alt="image">
      <div class="caption">
        <div>{{ captions.caption1.value }}</div>
        <div>{{ captions.caption2.value }}</div>
        <div>{{ captions.caption3.value }}</div>
        <div>{{ captions.caption4.value }}</div>
        <div>{{ captions.caption5.value }}</div>
      </div>
    </div>

    <div v-if="loginShow || registerShow||imageSrc" class="overlay" @click="closeLogin"></div>
  </div>
</template>

<script lang='ts' setup name="image captioning">
import axios from 'axios';
import { ref, computed, reactive } from 'vue';
import { RouterView, RouterLink } from 'vue-router'

import {useUserStore} from '@/assets/store/user'
const userStore = useUserStore()
import type { FormRules } from 'element-plus'
import {ElMessage} from 'element-plus'


const formRef = ref()
const form = reactive({
  regusername: '',
  regpassword: '',
  confirmPassword: '',
  loginUsername: '',
  loginPassword: '',
})

const loginShow = ref(false)
const registerShow = ref(false)
const regusername = ref('')
const regpassword = ref('')
const confirmPassword = ref('')
const loginUsername = ref('')
const loginPassword = ref('')
const captions = {
    caption1: ref(''),
    caption2: ref(''),
    caption3: ref(''),
    caption4: ref(''),
    caption5: ref('')
};
const imageSrc = ref('')
const Filename = ref()

const rules = reactive<FormRules>({
  regusername: [
    { required: true, message: "用户名不能为空" ,trigger:'blur'},
    { pattern: /^[a-zA-Z0-9_]+$/, message: "用户名只能包含字母、数字和下划线", trigger: 'blur' }
  ],
  regpassword:[
    {required:true,message:'密码不能为空',trigger:'blur'},
    {min:6,message:"密码不能小于6位",trigger:'blur'}
  ],
  confirmPassword:[
    {required:true,message:'密码不能为空',trigger:'blur'},
    {min:6,message:"密码不能小于6位",trigger:'blur'}
  ],
  
})
// 判断密码是否相同
const passwordsMatch = computed(() => form.regpassword === form.confirmPassword);

function showlogin() {
  loginShow.value = true
}


function showregister() {
  registerShow.value = true
}
function closeLogin() {
  loginShow.value = false
  registerShow.value = false
  imageSrc.value=''
}
// 登录
function login() {
  const formData = new window.FormData()
  formData.append('userName', loginUsername.value)
  formData.append('userPassword', loginPassword.value)
  axios.post('/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
    .then((res) => {
      if (res.data == 0) {
        alert('密码错误或者用户名不存在，请重新输入')
        loginPassword.value = ''
        return
      }
      else{
        userStore.userID=res.data
        userStore.username=loginUsername.value
        alert(`登录成功(id:${userStore.userID})`)
        closeLogin()

      }
    }).catch((err) => {
      console.log(err);
    });
}
// 注册
async function register() {
let t = true
await formRef.value?.validate().catch(()=>{
  ElMessage.error("注册信息不符合规范")
  t = false
})
  if(t){
    if (passwordsMatch.value) {
    const formData = new window.FormData()
    formData.append('userName', form.regusername)
    // console.log("用户名为：",form.regusername)
    formData.append('userPassword', form.regpassword)

    axios.post('/register', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
      .then((res) => {
        if (res.data == 1) {
          form.regusername = ''
          form.regpassword = ''
          form.confirmPassword= ''
          if (window.confirm("注册成功，是否立即登录？")) {
            closeLogin()
            showlogin()
          } else {
            return
          }
        }
        if (res.data == 0) {
          return alert('该用户名已经存在！')

        }
      }).catch((err) => {
        console.log(err);
      });

  } else {
    return alert('两次输入的密码不相同，请确认密码')
  }
  }


}



function getImage(database:any) {
    const formData = new FormData()

    formData.append('database',database)

    axios.post('/getRandom',formData)
        .then(Response => {
            // 接收数据
            const {filename,caption1,caption2,caption3,caption4,caption5,data} = Response.data
            // 赋值文件名和描述
            Filename.value=filename
            captions.caption1.value=caption1
            captions.caption2.value=caption2
            captions.caption3.value=caption3
            captions.caption4.value=caption4
            captions.caption5.value=caption5

            console.log(data)
            // 解码data赋值给图片
            imageSrc.value = 'data:image/jpeg;base64,' + data
        }).catch(error => {
            console.error('获取图片错误:', error);
        })
}

function random(x:any){
  if (x==0){
    const database ='usercaption'
    getImage(database)
  }
  if (x==1){
    const database ='imagecaption'
    getImage(database)
  }
}

</script>

<style scoped>
@import url('./assets/css/app.css');
@import url('./assets/css/login.css');
</style>