<template>
    <div>
        <div class="text">感谢您(用户ID：{{ userStore.username }})为数据库提供内容，图像描述内容请简单明了，仅描述植物外观特征，不涉及生长环境和用途等</div>
        <div class="text">您可以选择描述数据库中已经存储的图片，也可以上传您自己的图片</div>
        <hr>
        <button @click="handoff">{{ button }}</button>
        <div v-if="user == 0">
            <input type="file" accept="image/*" @change="upFile">
            <button @click="show">预览文件</button>

            <div class="input">
                <div class="userinput">
                    <p>请至少输入一条描述</p>
                    caption1: <input type="text" v-model="captions.caption1.value">
                    caption2: <input type="text" v-model="captions.caption2.value">
                    caption3: <input type="text" v-model="captions.caption3.value">
                    caption4: <input type="text" v-model="captions.caption4.value">
                    caption5: <input type="text" v-model="captions.caption5.value">
                </div>
                <div class="img"><img class="show" v-if="imageUrl" :src="imageUrl" /></div>
            </div>
            <div style="font-size: 12px;" ref="reimage"></div>
            <div style="font-size: 12px;" ref="re"></div>

            <div class="inputbutton"><button @click="submitForm">提交</button></div>

        </div>
        <div v-if="user == 1">
            <button @click="getImage" class="getImage">获取一张数据库图片</button>
            <div>{{ Filename }}</div>
            <div class="input">
                <div class="userinput">
                    <p>请至少输入一条描述</p>
                    caption1: <input type="text" v-model="captions.caption1.value">
                    caption2: <input type="text" v-model="captions.caption2.value">
                    caption3: <input type="text" v-model="captions.caption3.value">
                    caption4: <input type="text" v-model="captions.caption4.value">
                    caption5: <input type="text" v-model="captions.caption5.value">
                </div>
                <div class="img"><img class="show" v-if='imageSrc' :src="imageSrc"></div>
            </div>
            <div style="font-size: 12px;" ref="re"></div>

            <div class="inputbutton"><button @click="submitForm">提交</button></div>

        </div>
    </div>
</template>

<script lang='ts' setup>
import axios from 'axios';
import { ref } from 'vue';

import {useUserStore} from '@/assets/store/user'
const userStore = useUserStore()


const imageSrc = ref('')
const imageUrl = ref('')
const userInput = ref('')
const file = ref()
const Filename = ref()
const user = ref(0)
const button = ref('描述数据库中的内容')
const captions = {
    caption1: ref(''),
    caption2: ref(''),
    caption3: ref(''),
    caption4: ref(''),
    caption5: ref('')
};

// 切换上传方案
function handoff() {
    if (user.value == 0) {
        button.value = '描述本地图片的内容'
        user.value = 1
        file.value = ''
        getImage(   )
    }
    else {
        button.value = '描述数据库中的内容'
        user.value = 0
    }
}
// 读取用户输入
function submitForm() {
    // 获取用户输入的文本
    if (user.value == 0) {
        uploadFile()
        uploadCaption()
    }
    else {
        uploadCaption()
    }
    const inputText = userInput.value;
    console.log(inputText)
}

// 上传图片
const re = ref()
const reimage = ref()
function uploadFile() {
    const formData = new window.FormData()

    formData.append('file', file.value)
    console.log(formData.get('file'))
    axios.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
        .then((res) => {
            console.log(res);
            reimage.value.innerHTML = res.data
        }).catch((err) => {
            console.log(err);
        });
}
// 上传图片名称和图片描述
function uploadCaption() {
    const formData = new window.FormData()

    formData.append('file', file.value)
    formData.append('username', userStore.username)
    formData.append('caption1', captions.caption1.value)
    formData.append('caption2', captions.caption2.value)
    formData.append('caption3', captions.caption3.value)
    formData.append('caption4', captions.caption4.value)
    formData.append('caption5', captions.caption5.value)
    formData.append('filename', Filename.value)


    axios.post('/uploadCaption', formData, {
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

//读取用户上传的文件保存到file
function upFile(event: any) {
    file.value = event.target.files[0];
    console.log(file.value)
    captions.caption1.value=''
    captions.caption2.value=''
    captions.caption3.value=''
    captions.caption4.value=''
    captions.caption5.value=''
}

// 展示图片
function show() {
    const reader = new FileReader();
    reader.readAsDataURL(file.value);
    reader.onload = () => {
        // 指定类型为string
        imageUrl.value = reader.result as string;
    };

}
// 获取一张数据库图片
function getImage() {
    const formData = new FormData()

    formData.append('database','usercaption')

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

</script>

<style scoped>
@import url('../css/upcaption.css');
</style>