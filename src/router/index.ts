// 创建一个路由器，并暴露出去

//引入createRouter
import { createRouter ,createWebHistory} from "vue-router";

// 引入需要用到的组件
import Home from '@/assets/components/Home.vue'
import About from '@/assets/components/About.vue'
import Databases from '@/assets/components/Databases.vue'
import image from '@/assets/components/image.vue'
import caption from "@/assets/components/caption.vue"
import imageCaptioning from '@/assets/components/imageCaptioning.vue'
// import xx from '@/assets/components/'
// 创建路由器
const router = createRouter({
    history:createWebHistory(), //设置路由器的工作模式
    routes:[
        {
            
        path:'/home',
        component:Home
    },
        {
        path:'/databases',
        component:Databases,
        children:[
{
    name:'图片',
    path:'image',
    component:image
},
{
    name:'描述',
    path:'caption',
    component:caption
}            
        ]
    },
        {
        path:'/about',
        component:About
    },
    {
        name:'imagecaptioning',
        path:'/imagecaption',
        component:imageCaptioning
    },
    {
        // 重定向到home，使得打开的第一个页面是/home
        path:'/',
        redirect:'/home'
    }
]
})

//暴露

export default router