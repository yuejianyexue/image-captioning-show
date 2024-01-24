// 创建一个路由器，并暴露出去

//引入createRouter
import { createRouter ,createWebHistory} from "vue-router";

// 引入需要用到的组件
import Home from '@/components/Home.vue'
import About from '@/components/About.vue'
import Databases from '@/components/Databases.vue'
import image from '@/components/image.vue'
import caption from "@/components/caption.vue"

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
        // 重定向到home，使得打开的第一个页面是/home
        path:'/',
        redirect:'/home'
    }
]
})

//暴露

export default router