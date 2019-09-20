# import cv2
# import os
import tensorflow as tf
import keras
import numpy as np
from PIL import Image
from keras.backend import tensorflow_backend as backend
from django.conf import settings
from . import cnn_model


labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
im_size = (32 * 32 * 3)
# path = os.path.dirname(os.path.abspath(__file__))

# kerasキャッシュ削除
# keras.backend.clear_session()

# Tensor("dense_2/Softmax:0", shape=(?, 10), dtype=float32) is not an element of this graph.対応
graph = tf.get_default_graph()

# モデルデータ読み込み
model_file_path = settings.MODEL_FILE_PATH
model = cnn_model.get_model()
model.load_weights(model_file_path)

def check_photo(upload_image):
    # アップロードされた画像ファイルをメモリ上でOpenCVのimageに格納
    # img = np.asarray(Image.open(upload_image))
    img = Image.open(upload_image)
    img = img.convert("RGB")    # 色空間をRGBにする
    img = img.resize((32, 32))    # サイズ変更

    # データに変換
    x = np.asarray(img)
    x = x.reshape(-1, 32, 32, 3)
    x = x / 255

    # 予測
    pre = model.predict([x])[0]
    idx = pre.argmax()
    per = int(pre[idx] * 100)
    return (idx, per)

def check_photo_str(upload_image):
    global graph
    with graph.as_default():
        idx, per = check_photo(upload_image)
        # 答えを表示
        print('この写真は、', labels[idx], 'です。')
        print('可能性は、', per, '%です。')
    return labels[idx], per

if __name__ == '__main__':
    check_photo_str('test_airplane.jpg')
    check_photo_str('test_horse.jpg')
    check_photo_str('test_cat.jpg')
    check_photo_str('test_truck.jpg')




