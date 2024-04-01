from io import BytesIO
from flask_cors import CORS

from flask import Flask, make_response, send_file, request  # 导入make_response函数
from flask_sqlalchemy import SQLAlchemySQLAlchemy
from sqlalchemy import text, func
from sqlalchemy.dialects.mysql import MEDIUMBLOB


app = Flask(__name__)
CORS(app, supports_credentials=True)  # 允许所有来源的跨域请求，并且支持凭证（如 cookies


@app.route('/getA')
def GetA():
    response = make_response('这是一个图片描述！')  # 创建一个响应对象
    response.headers['Access-Control-Allow-Origin'] = '*'  # 添加一个响应头
    return response  # 返回响应对象


# 连接数据库
# 设置连接参数
HOSTNAME = 'localhost'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'test'

# 配置连接数据库参数
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
db = SQLAlchemy(app)
# 测试数据库连接，成功返回 1
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())


# 设置一个数据库模型
# 表结构为：name：image，主键id自增1，data类型为Blob，time类型为timestamp，默认值为插入时间
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(MEDIUMBLOB)
    time = db.Column(db.TIMESTAMP, server_default=func.CURRENT_TIMESTAMP())


@app.route('/getImage/<int:image_id>')
def getImage(image_id):
    image = Image.query.get_or_404(image_id)
    # image.headers['Access-Control-Allow-Origin'] = '*'
    return send_file(BytesIO(image.data), mimetype='image/jpg')


@app.route('/upload', methods=['POST'])
def upload():
    # 接收数据
    file = request.files['file']
    # 将数据转化为二进制数据
    file_data = file.read()
    new_file = Image(data=file_data)
    # 在数据库添加数据
    db.session.add(new_file)
    # 提交更改
    db.session.commit()
    return '成功上传数据'


if __name__ == '__main__':
    # 如果数据库中没有image表则创建
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=8000, debug=True)
