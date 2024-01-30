<template>
    <div>
        <input type="file" accept="image/*" @change="upFile">
         <button @click="show">预览文件</button>
         <input type="submit" @click="uploadFile">
         <div ref="re"></div>
         <div>
            <hr>
             <img class="show" v-if="imageUrl" :src="imageUrl" />
         </div>
         <!-- <button @click="uploadFile" :disabled="!upFile">上传文件</button> -->
    </div>
</template>

<script lang='ts' setup>
import axios from 'axios';
import {ref} from 'vue';

const imageUrl =ref('')
const file = ref()


//读取用户上传的文件保存到file
function upFile(event: any) {
    file.value = event.target.files[0]; 
   console.log(file.value)
}

// 展示图片
function show(){
    const reader = new FileReader();
    reader.readAsDataURL(file.value);
    reader.onload = () => {
        // 指定类型为string
    imageUrl.value = reader.result as string;
    };
    
} 
const re = ref()
function uploadFile(){
      const formData = new window.FormData()
      
      formData.append('file',file.value)
    console.log(formData.get('file'))
    axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then((res) => {
        console.log(res);
        re.value.innerHTML = res.data
      }).catch((err) => {
        console.log(err);
      });
}   
</script>

<style scoped>
.show{
    max-height: 500px;
    max-width: 500px;
}
</style>