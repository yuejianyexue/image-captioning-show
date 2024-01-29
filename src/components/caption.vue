<template>
  <div>
<h1>caption</h1>
<button @click="getCaption">连接数据库获取一段话：</button>
<button @click="del">清空</button>
<p>返回的值：{{ caption }}</p>
  </div>
</template>

<script lang='ts' setup>
import axios from 'axios';
import { ref } from 'vue';

let caption = ref()

function getCaption(){
  console.log('正在请求数据库')
  axios.get('/getA').then(Response =>{
    caption.value = Response.data
    console.log('已接收返回')
  })
  .catch(error=>{
    console.log(error)
  }
  )
}

function del(){
  caption.value = ''
}
</script>

<style  scoped>

</style>