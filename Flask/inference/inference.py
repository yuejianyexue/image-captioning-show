import os

import tensorflow as tf
import numpy as np
from tqdm import tqdm

from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.applications import VGG16, ResNet50, DenseNet201

# 加载预训练模型
model = tf.keras.models.load_model('model/model.h5')

# 加载进行推理的图片
image_path = 'test_image/OIP-C.jpg'  # 替换为你实际图片的路径


def tztq(image_path):
    # 加载DenseNet201
    model = DenseNet201()
    # 定义一个新的模型fe，将输入层设置为DenseNet201的输入层，输出层设置为倒数第二层
    # 这样做的目的是使用DenseNet201模型作为一个特征提取器，提取图像的高级特征，而不是直接进行图像分类
    fe = Model(inputs=model.input, outputs=model.layers[-2].output)
    # 设置图像大小
    img_size = 224
    # 初始化一个字典用于存储图像特征
    features = {}
    # 使用tqdm库显示循环进度条，遍历data中image列的唯一值，处理每个不同的图像
    # for image in tqdm(data['image'].unique().tolist()):
    #     使用load_img函数从image_path和image拼接的路径加载图像，并将其大小调整为224x224。
    img = load_img(os.path.join(image_path), target_size=(img_size, img_size))
    #     将加载的图像转换为NumPy数组格式，以便进行后续处理。
    img = img_to_array(img)
    #     归一化
    img = img / 255.
    #     在第一个维度（即批次维度）上增加一维，Keras模型通常期望输入是批次的形式，即使我们一次只处理一张图像。
    img = np.expand_dims(img, axis=0)
    #     使用之前创建的fe模型对归一化后的图像进行预测，提取其特征。verbose=0表示在预测过程中不显示任何输出。
    feature = fe.predict(img, verbose=0)
    #     将预测结果存储到feature()
    print('预测结果：',feature)
    return feature


# 将传入的索引转换为文字
def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def predict_caption(model, image, tokenizer, max_length, features):
    feature = features
    in_text = "startseq"
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], max_length)

        y_pred = model.predict([feature, sequence])
        y_pred = np.argmax(y_pred)

        word = idx_to_word(y_pred, tokenizer)

        if word is None:
            break

        in_text += " " + word

        if word == 'endseq':
            break

    return in_text

if __name__ == '__main__':
    features = tztq(image_path)
    predict_caption(model=model,features=features,max_length=20,)








# image = Image.open(image_path)
# image = image.resize((224, 224))  # 调整图片大小以匹配模型的输入尺寸
#
# # 预处理图片（归一化像素值并添加批次维度）
# image_array = np.array(image) / 255.0
# image_array = np.expand_dims(image_array, axis=0)
#
# # 进行推理
# with tf.device('/CPU:0'):  # 使用 CPU 进行推理
#     predictions = model.predict(image_array)
#
# # 获取概率最高的类别标签
# class_index = np.argmax(predictions[0])
# class_label = f'类别 {class_index}'  # 替换为你实际的类别标签
#
# print(f"推理结果：{class_label}")
