// 导入http模块

// const { response } = require('express')
import { createServer } from 'http';

// 创建服务对象

const sever = createServer((request,response)=>{
    let method = request.method;
    let {pathname} = new URL(request.url,'http://localhost');
    response.setHeader('Access-Control-Allow-Origin', '*');

    response.setHeader("Content-Type","text/html;charset=utf-8");

    // 判断

    if(method ==='GET' && pathname ==='/get'){
        response.end('成功')
    }else {
        response.end('erro')
    }

})

// 设置监听

sever.listen(8000,()=>{
    console.log('已经启动监听')
})