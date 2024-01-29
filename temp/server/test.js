import express from 'express';
import cors  from 'cors';
import mysql from 'mysql';

const app = express()

app.use(cors())
const db = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'root',
    database:'test'
})

app.get('/getA',(req,res)=>{
    db.query('select * from test'),(err,results)=>{
        if(err){
            results = {
                warn:'error',
                message:'获取数据库时发生错误'
            },
            res.send(JSON.stringify(results))
        }else{
            console.log('111')
            res.send(JSON.stringify(results))
        }
    }
})

// 挂载监听

app.listen(5173,()=>{
    console.log('服务器已启动！')
})