from functools import lru_cache
import cv2
import glob
import os
import numpy as np
import json


def getAllImg(path, type):
    '''
    读取文件夹下所有同类型文件
    '''
    imgs = glob.glob(os.path.join(path, '*.{}'.format(type)))
    return imgs

def load_json(filenamejson):
    '''
    读取json文件
    '''
    with open(filenamejson) as f:
        raw_data = json.load(f)
    return raw_data

def merge_img(path_r50, path_r18, path_merge):
    '''
    横向合并图片，用于比较不同模型的预测效果
    '''
    if not os.path.exists(path_merge):
        os.mkdir(path_merge)

    imgs1 = getAllImg(path_r50, 'jpg')
    imgs2 = getAllImg(path_r18, 'jpg')

    for img in imgs1:
        img1 = cv2.imread(img)
        img2 = cv2.imread(os.path.join(path_r18, os.path.basename(img)))
        h = max(img1.shape[0], img2.shape[0])
        w = max(img1.shape[1], img2.shape[1])
        img1_resized = cv2.resize(img1, (w, h))
        img2_resized = cv2.resize(img2, (w, h))
        img_merge = np.zeros([h, 2 * w, 3])
        img_merge[:,:w, :] = img1_resized
        img_merge[:,w:, :] = img2_resized
        cv2.imwrite(os.path.join(path_merge, os.path.basename(img)),img_merge)
    
def vis_seg(path_seg, save_dir):
    '''
    使mask可视化
    '''
    img_segs = getAllImg(path_seg, "png")
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    for seg in img_segs:
        img = cv2.imread(seg)
        img_vis = img * (0, 0, 255)
        cv2.imwrite(os.path.join(save_dir, os.path.basename(seg)),img_vis)

def gt_mask_generate(path_gt, save_dir, json_gt):
    '''
    根据gt的标注生成mask
    '''
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    img_gt = getAllImg(path_gt, 'jpg')
    content = load_json(json_gt)
    for t in content:
        w = content[t]['file_attributes']['width']
        h = content[t]['file_attributes']['height']
        mask = np.zeros((h, w))
        filename_img = os.path.join(save_dir, content[t]['filename'])
        l_regions = []
        for region in content[t]['regions']:
            l_region = []
            all_points_x = region['shape_attributes']['all_points_x']
            all_points_y = region['shape_attributes']['all_points_y']
            for i in range(len(all_points_x)):
                l_region.append([all_points_x[i], all_points_y[i]])
            l_regions += l_region
        mask = cv2.fillPoly(mask, [np.array(l_regions, dtype=int)], 1)
        cv2.imwrite(filename_img, mask)
        
# path_r50 = "/home/zq/work/SOLO/work_dirs/vis_solov2_r50/"
# path_r18 = "/home/zq/work/SOLO/work_dirs/vis_solov2_r18/"
# path_merge = "/home/zq/work/SOLO/work_dirs/vis_solov2_r50_r18/"

# merge_img(path_r50, path_r18, path_merge)

# path_seg = '/home/zq/work/SOLO/work_dirs/vis_solov2_test/'
# save_dir = '/home/zq/work/SOLO/work_dirs/vis_solov2_test_vis/'

# vis_seg(path_seg, save_dir)

# gt_mask_generate('/home/zq/work/SOLO/data/road/val/', '/home/zq/work/SOLO/data/road/val-mask/', '/home/zq/work/SOLO/data/tools/VIA/tutorial/jsons/merge_val_json.json')

