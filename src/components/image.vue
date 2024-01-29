<template>
  <div>
<h1>image</h1>
<button @click="getImage" class="getImage">获取一张数据库图片</button>
<img v-if='imageSrc' :src="imageSrc" alt="image">
  </div>
</template>

<script lang='ts' setup>
import { ref } from 'vue';
import axios from 'axios';

const imageSrc = ref('')

function getImage(){
    axios.get('/getImage/1',{responseType:'arraybuffer'})
    .then(Response=>{
      const base64Image = btoa(
        new Uint8Array(Response.data).reduce(
          (data,byte)=>data +String.fromCharCode(byte),''
        )
      )
      imageSrc.value = `data:${Response.headers['content-type']};base64,${base64Image}`; 
    }).catch(error => {  
          console.error('Error fetching image:', error); 
        })
    
      }

</script>

<style  scoped>

</style>