import { defineStore } from "pinia";

export const useUserStore = defineStore('user',{
    // 存储数据的地方
    state(){
        return{
            username:'未登录用户',
            userID:''
        }
    }
})