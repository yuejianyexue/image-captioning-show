<template>
    <div>
        <div class="title">
            <h2>数据库内容列表</h2><button @click="switchData">{{ data }}</button>
        </div>

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
        <!-- 翻页功能 -->
        <div class="next">
            <div>
                <button @click="previous">上一页 </button>

                <template v-for="(index, i) in displayedPages" :key="i">
                    <button v-if="index === '...'">{{ index }}</button>
                    <button v-else :class="{ active: index === page }" @click="getpage(index)">{{ index }}</button>
                </template>

                <button @click="next">下一页</button>
                跳转到<input v-model="p">页
                <button @click="toP">跳转</button>
                总页数{{ totalPages }}
            </div>
        </div>

    </div>
    <img class="showImage" v-if='imageSrc' :src="imageSrc" alt="image">

    <div v-if="imageSrc" class="overlay" @click="close"></div>

</template>

<script lang='ts' setup>
import { computed, ref} from 'vue'
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

const page = ref(1)
const totalPages = ref(); // 假设总页数为20

const displayedPages = computed(() => {
    const totalDisplayedPages = 15;
    let startPage = 1;
    let endPage = totalPages.value;

    if (totalPages.value > totalDisplayedPages) {
        if (page.value > Math.floor(totalDisplayedPages / 2)) {
            startPage = Math.max(1, page.value - Math.floor(totalDisplayedPages / 2));
            endPage = Math.min(totalPages.value, startPage + totalDisplayedPages - 1);
        } else {
            endPage = totalDisplayedPages;
        }
    }

    const pages = [];
    for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
    }

    if (totalPages.value > totalDisplayedPages) {
        if (startPage > 1) {
            pages.unshift('...');
        }
        if (endPage < totalPages.value) {
            pages.push('...');
        }
    }

    return pages;
});



const getdatabase = ref('imageCaption')

function dataList() {
    axios.get(`/dataList?page=${page.value}&database=${getdatabase.value}`)
        .then(function (response) {
            // 请求成功处理
            // console.log(response.data);
            database.value = response.data.data
            totalPages.value = response.data.pages
        })
        .catch(function (error) {
            // 请求失败处理
            console.log(error);
        });


};

const imageSrc = ref('')

function getImage(fn:any){

    const formData = new window.FormData()

    formData.append('filename',fn)
    
    axios.post('/getImage',formData,{
        headers: {
      'Content-Type': 'multipart/form-data'
    }
    })
    .then(Response=>{
        const data =Response.data.data
        imageSrc.value = 'data:image/jpeg;base64,' + data
    }).catch(error => {  
          console.error('Error fetching image:', error); 
        })
    
}

const data = ref('查看用户数据')
let n = true
function switchData() {
    if (n) {
        getdatabase.value = 'userCaption'
        data.value = '查看库中数据'
        n = !n
        getpage(1)


    } else {
        getdatabase.value = 'imageCaption'
        data.value = '查看用户数据'
        n = !n
        getpage(1)
    }

}

function getpage(p: any) {
    page.value = p
    dataList()
}
function previous() {
    page.value--
    dataList()
} function next() {
    page.value++
    dataList()
}

const p = ref()
function toP() {
    if (p.value > totalPages.value || p.value <= 0) {
        alert('页码错误，请重新输入')
    } else {
        getpage(p.value)
    }
}

function close(){
    imageSrc.value=''
}
dataList()
</script>

<style scoped>
@import url('../css/lookdata.css');
</style>