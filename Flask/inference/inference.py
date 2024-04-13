import os

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import DenseNet201
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def extract_caption(image_path):
    # 加载预训练模型
    model = tf.keras.models.load_model('inference/model/model.h5')

    # 读取图像并调整大小和归一化
    def readImage(path, img_size=224):
        #     加载图像，转换为RGB并调整大小为“img_size”
        img = load_img(path, color_mode='rgb', target_size=(img_size, img_size))
        img = img_to_array(img)
        #     归一化到[0,1]
        img = img / 255.
        return img

    # 特征提取
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
        return feature

    # 加载词汇表
    def load_word_index(file_path):
        word_index = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                word, index = line.strip().split(': ')
                word_index[word] = int(index)
        return word_index

    # 将传入的索引转换为文字
    def idx_to_word(integer, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    def predict_caption(model, tokenizer, max_length, features):
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

        # 加载词汇表

    word_index_file = 'inference/model/word_index.txt'
    # 加载进行推理的图片
    image_path = image_path  # 替换为你实际图片的路径
    loaded_word_index = load_word_index(word_index_file)
    # 创建tokenizer实例
    tokenizer = Tokenizer()
    tokenizer.word_index = loaded_word_index
    # 获取特征

    features = tztq(image_path)
    text = predict_caption(model=model, features=features, tokenizer=tokenizer, max_length=21)
    text = text.replace(" ", "")
    text = text.replace("endseq", "")
    text = text.replace("startseq", "")

    return text


if __name__ == '__main__':
    image_path = 'test.jpg'  # 替换为你实际图片的路径
    caption = extract_caption(image_path)
    print(caption)
