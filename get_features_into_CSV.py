# created at 2018-05-11
# updated at 2018-07-26

# By coneypo
# Blog: http://www.cnblogs.com/AdaminXie
# GitHub: https://github.com/coneypo/Dlib_face_recognition_from_camera

#   return_128d_features()          获取某张图像的128d特征
#   write_into_csv()                将某个文件夹中的图像读取特征兵写入csv
#   compute_the_mean()              从csv中读取128d特征，并计算特征均值

# 增加录入多张人脸的功能

import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np
import pandas as pd

path_pics = "F:/code/python/P_dlib_face_reco/data/faces_from_camera/"
path_csv = "F:/code/python/P_dlib_face_reco/data/csvs/"

# detector to find the faces
detector = dlib.get_frontal_face_detector()

# shape predictor to find the face landmarks
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")

# face recognition model, the object maps human faces into 128D vectors
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")


# 返回单张图像的128D特征
def return_128d_features(path_img):
    img = io.imread(path_img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dets = detector(img_gray, 1)

    print("检测的人脸图像：", path_img, "\n")

    # 因为有可能截下来的人脸再去检测，检测不出来人脸了
    # 所以要确保是 检测到人脸的人脸图像 拿去算特征
    if len(dets) != 0:
        shape = predictor(img_gray, dets[0])
        face_descriptor = facerec.compute_face_descriptor(img_gray, shape)
    else:
        face_descriptor = 0
        print("no face")

    print(face_descriptor)
    return face_descriptor

return_128d_features(path_pics+"/2018-05-21-14-19-05/img_face_2.jpg")

# 将文件夹中照片特征提取出来，写入csv
# 输入input:
#   path_pics:  图像文件夹的路径
#   path_csv:   要生成的csv路径

def write_into_csv(path_pics, path_csv):
    dir_pics = os.listdir(path_pics)

    with open(path_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(dir_pics)):
            # 调用return_128d_features()得到128d特征
            print("正在读的人脸图像：", path_pics + dir_pics[i])
            features_128d = return_128d_features(path_pics + dir_pics[i])
            #  print(features_128d)
            # 遇到没有检测出人脸的图片跳过
            if features_128d == 0:
                i += 1
            else:
                writer.writerow(features_128d)


#write_into_csv(path_pics, path_csv + "default_person.csv")

#path_csv_rd = "F:/code/python/P_dlib_face_reco/data/csvs/default_person.csv"


# 从csv中读取数据，计算128d特征的均值
def compute_the_mean(path_csv_rd):
    column_names = []

    # 128列特征
    for i in range(128):
        column_names.append("features_" + str(i + 1))

    # 利用pandas读取csv
    rd = pd.read_csv(path_csv_rd, names=column_names)

    # 存放128维特征的均值
    feature_mean = []

    for i in range(128):
        tmp_arr = rd["features_" + str(i + 1)]
        tmp_arr = np.array(tmp_arr)

        # 计算某一个特征的均值
        tmp_mean = np.mean(tmp_arr)

        feature_mean.append(tmp_mean)

    print(feature_mean)
    return feature_mean

# compute_the_mean(path_csv_rd)
path_faces = r"F:\code\python\P_dlib_face_reco\data\faces_from_camera"

# 存放所有特征均值的csv的路径
path_csv_feature_all = "F:/code/python/P_dlib_face_reco/data/csvs/features_all.csv"


# 存放人脸的文件夹们
folder_face = os.listdir(path_faces)

# 存放人脸特征的csv的路径
path_csv_rd = "F:/code/python/P_dlib_face_reco/data/csvs/faces_rd/"

# 对每个存放人脸的文件夹遍历
# 计算提取每个文件夹中人脸的特征值存入csv中
# for i in range(len(folder_face)):
#     print("########## 分隔符 ############")
#     print(folder_face[i])
#
#     # 单个文件夹下的读取到的照片们
#     pic_face = os.listdir(path_faces + "/" + folder_face[i])
#
#     for j in range(len(pic_face)):
#         print(pic_face[j])
#
#     print('\n', "读取检测人脸获取特征: ")
#     write_into_csv(path_faces + "/" + folder_face[i]+"/", path_csv_rd+folder_face[i]+".csv")
#     print("写入的csv: ")
#     print(path_csv_rd+folder_face[i]+".csv")
#
#     print('\n')

# 读取人脸csv的数据，然后对每个csv求均值
# # 将特征值的均值存入一个csv中
# with open(path_csv_feature_all, "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     csv_rd = os.listdir(path_csv_rd)
#     print("特征均值: ")
#     for i in range(len(csv_rd)):
#         feature_mean = compute_the_mean(path_csv_rd+csv_rd[i])
#         writer.writerow(feature_mean)
#
