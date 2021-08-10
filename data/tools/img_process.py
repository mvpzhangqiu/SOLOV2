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


def merge_img(path_gt, path_baseline, path_new, path_merge):
    '''
    横向合并图片，用于比较不同模型的预测效果
    '''
    if not os.path.exists(path_merge):
        os.mkdir(path_merge)

    imgs1 = getAllImg(path_baseline, 'jpg')
    imgs2 = getAllImg(path_new, 'jpg')

    for img in imgs1:
        img1 = cv2.imread(img)
        img2 = cv2.imread(os.path.join(path_new, os.path.basename(img)))
        img_gt = cv2.imread(os.path.join(path_gt, os.path.basename(img)))
        try:
            h = max(img1.shape[0], img2.shape[0])
            w = max(img1.shape[1], img2.shape[1])
        except:
            import ipdb
            ipdb.set_trace()

        img2_resized = cv2.resize(img2, (w, h))
        try:
            img_gt_resized = cv2.resize(img_gt, (w, h))
        except:
            import ipdb
            ipdb.set_trace()
        img_merge = np.zeros([h, 3 * w, 3])
        img_merge[:, :w, :] = img1_resized
        img_merge[:, w:2 * w, :] = img2_resized
        img_merge[:, 2 * w:, :] = img_gt_resized
        cv2.imwrite(os.path.join(path_merge, os.path.basename(img)), img_merge)


def vis_seg(seg_dir, filetype, img_dir, save_dir):
    '''
    使mask可视化
    '''
    img_segs = getAllImg(seg_dir, filetype)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    # 将mask可视化后与原图拼接
    if os.path.exists(img_dir):
        for seg in img_segs:
            img_seg = cv2.imread(seg)
            img = cv2.imread(os.path.join(img_dir, os.path.basename(seg)))
            img_vis = img_seg * (0, 0, 255) * 0.5 + img * 0.5
            cv2.imwrite(os.path.join(save_dir, os.path.basename(seg)), img_vis)
    # 不与原图拼接
    else:
        for seg in img_segs:
            img = cv2.imread(seg)
            img_vis = img * (0, 0, 255)
            cv2.imwrite(os.path.join(save_dir, os.path.basename(seg)), img_vis)


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
            # l_regions += l_region
            # l_regions.append(l_region)
        # import ipdb
        # ipdb.set_trace()
            mask = cv2.fillPoly(mask, [np.array(l_region, dtype=int)], 1)

        # mask = cv2.fillPoly(mask, [np.array(l_regions, dtype=int)], 1)
        cv2.imwrite(filename_img, mask)


path_gt = "/home/zq/work/SOLO/data/road/val-mask-merge/"
path_baseline = "/home/zq/work/SOLO/work_dirs/vis/solov2_release_r50_fpn_8gpu_3x_epoch36/"
path_new = "/home/zq/work/SOLO/work_dirs/vis/solov2_release_r50_fpn_8gpu_3x_scale_epoch36/"
path_merge = "/home/zq/work/SOLO/work_dirs/vis/merge/3x_epoch36_scale"

merge_img(path_gt, path_baseline, path_new, path_merge)

# seg_dir = '/home/zq/work/SOLO/data/road/val-mask-1/'
# save_dir = '/home/zq/work/SOLO/data/road/val-mask-merge/'
# img_dir = '/home/zq/work/SOLO/data/road/val/'
# filetype = 'jpg'

# vis_seg(seg_dir, filetype, img_dir, save_dir)

# gt_mask_generate('/home/zq/work/SOLO/data/road/val/', '/home/zq/work/SOLO/data/road/val-mask-1/',
#                  '/home/zq/work/SOLO/data/tools/VIA/tutorial/jsons/merge_val_json.json')
