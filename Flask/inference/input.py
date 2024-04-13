# main.py

from inference import extract_caption


image_path = '../th.jpg'
caption = extract_caption(image_path)
print("图像描述：", caption)
