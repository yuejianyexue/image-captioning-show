<template>
    <div>
        <input type="file" accept="image/*" @change="upFile">
         <button @click="show">预览文件</button>
         <img v-if="imageUrl" :src="imageUrl" />
         <!-- <button @click="uploadFile" :disabled="!upFile">上传文件</button> -->
    </div>
</template>

<script lang='ts' setup>
// import axios from 'axios';
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
</script>

<style scoped></style>