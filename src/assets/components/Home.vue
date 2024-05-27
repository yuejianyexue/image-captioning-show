<template>
  <div class="main">
    <!-- 获取图像描述组件 -->
    <div class="left">
      <h1>上传你的图片获取文本描述</h1>
      <div>
        <input type="file" accept="image/*" @change="upFile">
        <button @click="show">预览文件</button>
        <input style="margin-left: 15px;" type="submit" value="获取文字描述" @click="getCaption">
        <hr>
        <div class="imagecaption">{{ re }}</div>
        <img class="show" v-if="imageUrl" :src="imageUrl" />

      </div>
    </div>
    
    <!-- 展示数据库内容组件 -->
    <div class="right">
      <div class="title">
        <h1>数据库中的数据</h1>
        <button @click="getList">刷新</button>
      </div>

      <hr>
      <div class="images">
        <div v-for="(item, index) in images" :key="index" class="imageshow">
          <img :src="item.image_data">
          <div class="text">{{ item.caption}}</div>
        </div>

      </div>
    </div>

  </div>

</template>

<script lang='ts' setup>

import { ref } from 'vue';
import axios from 'axios';
const imageUrl = ref('')
const file = ref()
const re = ref('示例文本:一片叶子 ')
const images = ref([{
  image_data:'',
  caption:''
}]);
import {useUserStore} from '@/assets/store/user'

const userStore = useUserStore()


//读取用户上传的文件保存到file
function upFile(event: any) {
  file.value = event.target.files[0];
  console.log(file.value)
}

// 展示用户选择的图片
function show() {
  const reader = new FileReader();
  reader.readAsDataURL(file.value);
  reader.onload = () => {
    // 指定类型为string
    imageUrl.value = reader.result as string;
  };

}

// 获取文本描述
function getCaption() {
  const formData = new window.FormData()

  formData.append('file', file.value)
  formData.append('userName', userStore.username)

  console.log(formData.get('file'))
  re.value = '数据解析中...'
  axios.post('/getCaption', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
    .then((res) => {
      console.log(res);
      // 将返回结果赋值给re
      re.value = res.data
    }).catch((err) => {
      console.log(err);
      re.value = '解析错误,请尝试重新上传'
    });

}

function getList(){
  axios.get('/getList')
  .then(function (response) {
    // 请求成功处理
    console.log(response.data);
    // 解码图片数据
    response.data.forEach((item:any) => {
        item.image_data = 'data:image/jpeg;base64,' + item.image_data;
      });
    images.value=response.data
    console.log(images.value)
  })
  .catch(function (error) {
    // 请求失败处理
    console.log(error);
  });
  

};

getList();

</script>

<style scoped>
@import url('../css/Home.css');
</style>