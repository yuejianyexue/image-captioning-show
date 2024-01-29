// const UserApi = require('src\api\SysUser.js')

import UserApi from '../api/SysUser.js';

import bodyParser from 'body-parser';

import express from 'express';

const app = express()

app.all("*",function(req,res,next) {
// 设置运行跨域的域名，*代表允许任意
    res.header("Access-Control-Allow-Origin", "*");

// 允许的header类型
res.header("Access-Control-Allow-Headers", "content-type");

// 跨域允许的请求方式
res.header("Access-Control-Allow-Methods", "DELETE,PUT,POST,GET,OPTIONS");

if (req.method.toLowerCase() == 'options')
    res.send(200); //让option尝试请求快速结束
else
    next()
})

//以JSON格式返回
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:false}))

// 后端api路由

app.use('/api/sysuser',UserApi)

app.listen(3000)
    console.log('服务已经启动，正在监听端口：3000')