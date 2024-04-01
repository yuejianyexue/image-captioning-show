<template>
  <div class="building">
<h1>home</h1>
  </div>
  <div @click="test" >node测试</div >


</template>

<script lang='ts' setup>
// import { ref } from 'vue';
import axios from 'axios';


function test(){
//  console.log("11")
axios.get('/get')
.then(Response=>{
  console.log('成功获取数据:', Response.data);
  // console.log(Response.data)
}).catch(error=>{
  console.error('Error fetching image:', error); 

})
}
</script>

<style scoped>

</style>