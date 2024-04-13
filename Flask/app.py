from io import BytesIO
from flask_cors import CORS

from flask import Flask, make_response, send_file, request, jsonify  # 导入make_response函数
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from concurrent.futures import ThreadPoolExecutor
from inference.inference import extract_caption
import random
import base64

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 允许所有来源的跨域请求，并且支持凭证（如 cookies


# @app.route('/getA')
# def GetA():
#     # 接收一个文件并保存为text.jpg，覆盖保存。
#     image_path = 'test.jpg'
#     future = executor.submit(extract_caption, image_path)
#     caption = future.result()  # 等待 extract_caption 执行完成
#     response = make_response(caption)  # 创建一个响应对象
#     response.headers['Access-Control-Allow-Origin'] = '*'  # 添加一个响应头
#     return response  # 返回响应对象

# 初始页面
@app.route('/')
def t():
    r = '这是一个空页面'
    return r


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


# 按照ID查询图片
@app.route('/getImage/<int:image_id>')
def getImage(image_id):
    # 使用get_or_404方法，如果没有查询到结果会返回404
    image = Image.query.get_or_404(image_id)
    # image.headers['Access-Control-Allow-Origin'] = '*'
    return send_file(BytesIO(image.data), mimetype='image/jpg')


# 用户上传图片
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


executor = ThreadPoolExecutor(max_workers=1)
# 用户获取图片的文字描述
@app.route('/getCaption', methods=['POST'])
def getCaption():
    file = request.files['file']
    # 将数据转化为二进制数据
    file_data = file.read()

    # 保存到本地文件夹
    local_folder = 'test.jpg'
    with open(local_folder, 'wb') as f:
        f.write(file_data)

    image_path = 'test.jpg'
    future = executor.submit(extract_caption, image_path)
    caption = future.result()  # 等待 extract_caption 执行完成
    response = make_response(caption)  # 创建一个响应对象
    response.headers['Access-Control-Allow-Origin'] = '*'  # 添加一个响应头
    return response  # 返回响应对象


# 获取数据库中随机一页数据
@app.route('/getList')
def getList():
    # 获取图片总数
    total_images_query = text("SELECT COUNT(id) FROM images")
    # 执行查询并获取结果
    total_images = db.session.execute(total_images_query).scalar()

    # 如果数据库中没有图片数据，返回空列表
    if total_images == 0:
        return jsonify({'message': 'No images found'}), 404

    # 每页显示的图片数量
    per_page = 10
    # 随机选择要查询的页数
    random_page = random.randint(1, total_images // per_page + 1)

    # 分页查询图片数据
    paginate_query = text("SELECT * FROM images LIMIT :offset, :limit")
    offset = (random_page - 1) * per_page
    # 执行查询并获取结果
    random_images = db.session.execute(paginate_query, {'offset': offset, 'limit': per_page})

    # 构建返回的数据列表
    response_data = []
    for image in random_images:
        # 获取图片名
        image_name = image.filename
        # 获取图片数据
        image_data = base64.b64encode(image.data).decode('utf-8')
        # 查询对应图片名的标题的
        caption_query = text("SELECT caption3 FROM image_captions WHERE image = :image_name")
        # 执行查询并获取结果
        caption = db.session.execute(caption_query, {'image_name': image_name}).fetchone()
        # 如果没有找到标题，将其设为 None
        if not caption:
            caption_text = None
        else:
            caption_text = caption[0]

        # 构建图片数据字典
        image_info = {
            'image_name': image_name,
            'image_data': image_data,
            'caption': caption_text
        }
        response_data.append(image_info)

    return jsonify(response_data)


# 获取一张随机图片
# @app.route('/getRandom')

if __name__ == '__main__':
    # 如果数据库中没有image表则创建
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=8000, debug=True)
