// export default UserApi

// import module from "../server/db.js";

import express from 'express';

// import module from "../server/db.js";

import MySQL from "mysql";

// import crypto from 'crypto'; //MD5


const router = express.Router()
// 连接数据库
const conn =MySQL.createConnection({
    host:'localhost',
    user:'root',
    password:'root',
    database:'test',
    port:'3306'})

conn.connect()

const jsonWrite = function(res,ret){
    if (typeof ret == 'undefined'){
        res.json({
            code:'1',msg:'连接失败'
        })
    }else res.json(ret)
}

router.get('/getA',(req,res)=>{
    conn.query('select * from test'),(err,results)=>{
        if(err){
            results = {
                warn:'error',
                message:'获取数据库时发生错误'
            },
            res.send(JSON.stringify(results))
        }
        if (results){
            jsonWrite(res,results)
        }
        }
    }
)

export default router