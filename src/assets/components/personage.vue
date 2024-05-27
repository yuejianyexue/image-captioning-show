<template>
    <div class="main">
        <div class="left">
            <div class="left-div">ID：{{ userStore.userID }}</div>
            <div class="left-div">用户名：{{ userStore.username }}</div>
            <div class="left-div">获取描述：{{ userAutoCaptionSum}}次</div>
            <div class="left-div">提交描述：{{ userCationSum}}条</div>

        </div>
        <div class="right">
            <div class="images">
                <div v-for="(item, index) in images" :key="index" class="imageshow">
                    <img :src="item.data">
                    <div class="text">{{ item.caption }}</div>
                </div>

            </div>
        </div>

        <div class="history">
            <table id="contentTable">
                <thead>
                    <tr>
                        <th style="width: 35px;">序号</th>
                        <th style="width: 70px;">文件名</th>
                        <th>描述1</th>
                        <th>描述2</th>
                        <th>描述3</th>
                        <th>描述4</th>
                        <th>描述5</th>
                        <th style="width: 80px;">查看详情</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    <tr v-for="(item, index) in database" :key="index">
                        <td>{{ index + 1 }}</td>
                        <td class="ellipsis" :title="item.filename"> {{ item.filename }}</td>
                        <td class="ellipsis" :title="item.captions1">{{ item.captions1 }}</td>
                        <td class="ellipsis" :title="item.captions2">{{ item.captions2 }}</td>
                        <td class="ellipsis" :title="item.captions3">{{ item.captions3 }}</td>
                        <td class="ellipsis" :title="item.captions4">{{ item.captions4 }}</td>
                        <td class="ellipsis" :title="item.captions5">{{ item.captions5 }}</td>
                        <td><button @click="getImage(item.filename)">图片详情</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <img class="showImage" v-if='imageSrc' :src="imageSrc" alt="image">

        <div v-if="imageSrc" class="overlay" @click="close"></div>
    </div>
</template>

<script lang='ts' setup>
import { useUserStore } from '@/assets/store/user'
const userStore = useUserStore()

import { computed, ref } from 'vue'
import axios from 'axios';

const database = ref([
    {
        filename: '',
        captions1: '',
        captions2: '',
        captions3: '',
        captions4: '',
        captions5: '',
    }
])
const imageSrc = ref('')

const userCationSum = ref()
const userAutoCaptionSum = ref()


// 显示图片
function getImage(fn: any) {

    const formData = new window.FormData()

    formData.append('filename', fn)

    axios.post('/getImage', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
        .then(Response => {
            const data = Response.data.data
            imageSrc.value = 'data:image/jpeg;base64,' + data
        }).catch(error => {
            console.error('Error fetching image:', error);
        })

}

// 获取列表 
const images = ref([{
    data: '',
    caption: ''
}]);

function getHistory() {
    axios.get(`/getHistory?username=${userStore.username}`)
        .then(function (response) {
            // 请求成功处理
            console.log(response.data);
            // 解码图片数据
            response.data.Auto_data.forEach((item: any) => {
                item.data = 'data:image/jpeg;base64,' + item.data;
            });  
            database.value = response.data.data
            images.value = response.data.Auto_data
            userCationSum.value = response.data.user_caption_sum
            userAutoCaptionSum.value = response.data.user_AutoCaption_sum
            console.log(images.value,userAutoCaptionSum.value,userCationSum.value)

        })
        .catch(function (error) {
            // 请求失败处理
            console.log(error);
        });


};
function close(){
    imageSrc.value=''
}
getHistory()
</script>

<style scoped>
@import url('../css/personage.css');
</style>