import base64
import random
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

from flask import Flask, make_response, send_file, request, jsonify  # 导入make_response函数
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func
from sqlalchemy.dialects.mysql import MEDIUMBLOB

from inference.inference import extract_caption

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


# 设置一个用户上传的数据的数据库表模型
# 表结构为：name：image，主键id自增1，data类型为Blob，time类型为timestamp，默认值为插入时间
class userImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(MEDIUMBLOB)
    time = db.Column(db.TIMESTAMP, server_default=func.CURRENT_TIMESTAMP())
    filename = db.Column(db.String(128))


class userCaption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))
    time = db.Column(db.TIMESTAMP, server_default=func.CURRENT_TIMESTAMP())
    username = db.Column(db.String(128))
    caption1 = db.Column(db.String(256))
    caption2 = db.Column(db.String(256))
    caption3 = db.Column(db.String(256))
    caption4 = db.Column(db.String(256))
    caption5 = db.Column(db.String(256))


class ImageCaption(db.Model):
    __tablename__ = 'image_captions'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(length=255))
    time = db.Column(db.TIMESTAMP, server_default=func.CURRENT_TIMESTAMP())
    caption1 = db.Column(db.String(length=255))
    caption2 = db.Column(db.String(length=255))
    caption3 = db.Column(db.String(length=255))
    caption4 = db.Column(db.String(length=255))
    caption5 = db.Column(db.String(length=255))


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(length=255))
    data = db.Column(MEDIUMBLOB)
    time = db.Column(db.TIMESTAMP, server_default=func.CURRENT_TIMESTAMP())


class userInfo(db.Model):
    __tablename__ = 'userInfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(length=128))
    userPassword = db.Column(db.String(length=128))
    time = db.Column(db.TIMESTAMP, server_default=func.CURRENT_TIMESTAMP())


class AutoCaption(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(length=128))
    time = db.Column(db.TIMESTAMP, server_default=func.CURRENT_TIMESTAMP())
    filename = db.Column(db.String(length=255))
    caption = db.Column(db.String(length=255))
    data = db.Column(MEDIUMBLOB)

# 按照图片名查询图片
@app.route('/getImage', methods=['POST'])
def getImage():
    image_name = request.form['filename']
    user_image = userImage.query.filter_by(filename=image_name).first()
    data_image = Image.query.filter_by(filename=image_name).first()
    if user_image:
        print('查询用户表')
        # 获取data字段数据
        data = user_image.data
        # 编码
        data_base64 = base64.b64encode(data).decode('utf-8')
        return jsonify({'data': data_base64})
    if data_image:
        # 获取data字段数据
        print('查询数据库表')

        data = data_image.data
        # 编码
        data_base64 = base64.b64encode(data).decode('utf-8')
        return jsonify({'data': data_base64})


# 用户上传图片
@app.route('/upload', methods=['POST'])
def upload():
    # 接收数据
    file = request.files['file']
    filename = file.filename
    # 将数据转化为二进制数据
    file_data = file.read()
    # 检查数据库中是否已经存在相同文件名的记录
    existing_file = userImage.query.filter_by(filename=filename).first()

    if existing_file:
        # 如果记录已经存在，则更新数据
        existing_file.data = file_data
    else:
        # 如果记录不存在，则创建新记录
        new_file = userImage(filename=filename, data=file_data)
        # 在数据库添加数据
        db.session.add(new_file)
    # 提交更改
    db.session.commit()
    return '图片上传成功'


# 用户上传图片描述
@app.route('/uploadCaption', methods=['POST'])
def uploadCaption():
    # 接收数据
    filename = request.form['filename']
    username = request.form['username']
    caption1 = request.form['caption1']
    caption2 = request.form['caption2']
    caption3 = request.form['caption3']
    caption4 = request.form['caption4']
    caption5 = request.form['caption5']
    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
    # 检查数据库中是否已经存在相同用户的同文件名的记录
    existing_file = userCaption.query.filter_by(username=username, filename=filename).first()

    if existing_file:
        # 如果记录已经存在，则更新描述
        print('更新描述')
        existing_file.caption1 = caption1
        existing_file.caption2 = caption2
        existing_file.caption3 = caption3
        existing_file.caption4 = caption4
        existing_file.caption5 = caption5
    else:
        # 如果记录不存在，则创建新记录
        new_file = userCaption(filename=filename, username=username, caption1=caption1, caption2=caption2,
                               caption3=caption3,
                               caption4=caption4, caption5=caption5)
        # 在数据库添加数据
        db.session.add(new_file)
    # 提交更改
    db.session.commit()
    re = filename + '数据上传成功'
    return re


executor = ThreadPoolExecutor(max_workers=1)


# 用户获取图片的文字描述
@app.route('/getCaption', methods=['POST'])
def getCaption():
    file = request.files['file']
    # 将数据转化为二进制数据
    file_data = file.read()
    # 获取用户名称
    username = request.form['userName']

    # 保存到本地文件夹
    local_folder = 'test.jpg'
    with open(local_folder, 'wb') as f:
        f.write(file_data)

    image_path = 'test.jpg'
    future = executor.submit(extract_caption, image_path)
    caption = future.result()  # 等待 extract_caption 执行完成

    # 生成的描述记录到表AutoCaption
    new_data = AutoCaption(userName=username,caption=caption,data=file_data)

    response = make_response(caption)  # 创建一个响应对象
    db.session.add(new_data)
    db.session.commit()
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
        caption_query = text("SELECT caption3 FROM image_captions WHERE filename = :image_name")
        # 执行查询并获取结果
        caption = db.session.execute(caption_query, {'image_name': image_name}).fetchone()
        # 如果没有找到标题，将其设为 None
        if not caption:
            caption_text = None
        else:
            caption_text = caption[0]

        # 构建数据字典
        image_info = {
            'image_name': image_name,
            'image_data': image_data,
            'caption': caption_text
        }
        response_data.append(image_info)

    return jsonify(response_data)


# 获取一张随机图片
@app.route('/getRandom', methods=['POST'])
def getRandom():
    # 查询表中的随机一条数据
    database = request.form['database']
    if database == 'usercaption':
        random_caption = userCaption.query.order_by(func.rand()).first()
    elif database == 'imagecaption':
        random_caption = ImageCaption.query.order_by(func.rand()).first()
    else:
        return jsonify({'error': '数据不存在'}), 404

    if random_caption:
        filename = random_caption.filename
        caption1 = random_caption.caption1
        caption2 = random_caption.caption2
        caption3 = random_caption.caption3
        caption4 = random_caption.caption4
        caption5 = random_caption.caption5

        # 根据filename查询userImage表中的对应数据
        if database == 'usercaption':
            user_image = userImage.query.filter_by(filename=filename).first()

        elif database == 'imagecaption':
            user_image = Image.query.filter_by(filename=filename).first()
        else:
            return jsonify({'error': '数据不存在'}), 404
        if user_image:
            # 获取data字段数据
            data = user_image.data
            # 编码
            data_base64 = base64.b64encode(data).decode('utf-8')
            # 返回查询结果
            return jsonify({
                'filename': filename,
                'caption1': caption1,
                'caption2': caption2,
                'caption3': caption3,
                'caption4': caption4,
                'caption5': caption5,
                'data': data_base64
            })

    # 如果没有找到数据，返回错误信息
    return jsonify({'error': '数据不存在'}), 404


# 获取数据库中指定页数据
@app.route('/dataList')
def dataList():
    page = request.args.get('page', default=1, type=int)
    database = request.args.get('database')

    per_page = 10  # 每页显示的数据条数
    offset = (page - 1) * per_page
    if database == 'imageCaption':
        image_captions = ImageCaption.query.offset(offset).limit(per_page).all()
        total_records = ImageCaption.query.count()
    if database == 'userCaption':
        image_captions = userCaption.query.offset(offset).limit(per_page).all()
        total_records = userCaption.query.count()
    # 将查询结果转换成字典列表
    data = []
    pages = (total_records + per_page - 1) // per_page
    for caption in image_captions:
        data.append({
            'id': caption.id,
            'filename': caption.filename,
            'time': caption.time,
            'captions1': caption.caption1,
            'captions2': caption.caption2,
            'captions3': caption.caption3,
            'captions4': caption.caption4,
            'captions5': caption.caption5
        })

    return {'data': data,
            'pages': pages}


# 用户登录
@app.route('/login', methods=['POST'])
def login():
    userName = request.form['userName']
    userPassword = request.form['userPassword']
    user = userInfo.query.filter_by(userName=userName).first()
    if user:
        if user.userPassword == userPassword:
            return str(user.id)
        else:
            return '0'
    return '0'


# 用户注册
@app.route('/register', methods=['POST'])
def register():
    userName = request.form['userName']
    print("1",userName)
    userPassword = request.form['userPassword']
    user = userInfo.query.filter_by(userName=userName).first()

    if user:
        print('用户存在')
        return '0'
    else:
        # 如果记录不存在，则创建新记录
        print('创建用户', userName)
        new_data = userInfo(userName=userName, userPassword=userPassword)
        # 在数据库添加数据
        db.session.add(new_data)
        db.session.commit()

        return '1'


# 查询用户历史记录
@app.route('/getHistory')
def getHistory():
    userName = request.args.get('username')
    # 获取所有用户ID=username的数据
    image_captions = userCaption.query.filter_by(username=userName).all()
    user_caption_sum = userCaption.query.filter_by(username=userName).count()
    user_AutoCaption_sum = AutoCaption.query.filter_by(userName=userName).count()
    Auto_Caption = AutoCaption.query.filter_by(userName=userName).all()
    data = []
    Auto_data = []
    for caption in image_captions:
        data.append({
            'id': caption.id,
            'filename': caption.filename,
            'time': caption.time,
            'captions1': caption.caption1,
            'captions2': caption.caption2,
            'captions3': caption.caption3,
            'captions4': caption.caption4,
            'captions5': caption.caption5
        })
    for AC in Auto_Caption:
        Auto_data.append({
            'data':base64.b64encode(AC.data).decode('utf-8'),
            'caption':AC.caption
        })
    return {'data': data,
            'Auto_data':Auto_data,
            'user_caption_sum':user_caption_sum,
            'user_AutoCaption_sum':user_AutoCaption_sum}


if __name__ == '__main__':
    # 如果数据库中没有表则创建
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=8000, debug=True)
