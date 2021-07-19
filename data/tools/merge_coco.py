#!/usr/bin/python
#-- coding:utf8 --

import os
import datetime
import random
import sys
import operator
import math
import numpy as np
import skimage.io
import matplotlib
from matplotlib import pyplot as plt
import cv2
from collections import defaultdict, OrderedDict
import json

# FILE_DIR = "/home/zq/work/SOLO/data/bak/road-bak/annotations/after_remove/train/"
FILE_DIR = "/home/zq/work/SOLO/data/bak/road-bak/annotations/after_remove/val/"

# json_des = '/home/zq/work/SOLO/data/bak/road-bak/annotations/after_merge/train/merge.json'
json_des = '/home/zq/work/SOLO/data/bak/road-bak/annotations/after_merge/val/merge.json'


 
def load_json(filenamejson):
    with open(filenamejson) as f:
        raw_data = json.load(f)
    return raw_data
 
file_count = 0
files = next(os.walk(FILE_DIR))[2]
for x in range(len(files)):
    #计数
    file_count = file_count + 1
    #组合文件路径
    filenamejson = FILE_DIR + str(files[x])
    #读取文件
    if x == 0:
        #第一个文件作为root
        root_data = load_json(filenamejson)
        image_id_dis = root_data['annotations'][-1]['image_id']
        an_id_dis = root_data['annotations'][-1]['id']
    else:
        raw_data = load_json(filenamejson)
        #追加images的数据
        for i in range(len(raw_data['images'])):
            raw_data['images'][i]['id'] += image_id_dis
            root_data['images'].append(raw_data['images'][i])
        annotation_count = str(raw_data["annotations"]).count('image_id',0,len(str(raw_data["annotations"])))

        for i in range(annotation_count):
            #追加annotations的数据
            raw_data['annotations'][i]['id'] += an_id_dis
            raw_data['annotations'][i]['image_id'] += image_id_dis
            root_data['annotations'].append(raw_data['annotations'][i])

temp = []
for m in root_data["categories"]:
    if m not in temp:
        temp.append(m)
root_data["categories"] = temp
print("共处理 {0} 个json文件".format(file_count))
print("共找到 {0} 个类别".format(str(root_data["categories"]).count('name',0,len(str(root_data["categories"])))))
 
json_str = json.dumps(root_data)
with open(json_des, 'w') as json_file:
        json_file.write(json_str)
#写出合并文件
 
print("Done!") 