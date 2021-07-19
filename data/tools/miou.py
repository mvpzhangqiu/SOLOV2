import numpy as np
import argparse
import json
from PIL import Image
from os.path import join
import glob 
import os 

def fast_hist(a, b, n):
    '''
    np.bincount计算了从0到n**2-1这n**2个数中每个数出现的次数，返回值形状(n, n)
    '''
    # k = (a >= 0) & (a < n) # 加上背景
    k = (a > 0) & (a < n) 
    return np.bincount(n * a[k].astype(int) + b[k], minlength=n ** 2).reshape(n, n)

def per_class_iu(hist):
    '''
    计算miou，对角线（交集）/并集
    '''
    return np.diag(hist) / (hist.sum(1) + hist.sum(0) - np.diag(hist))


def compute_mIoU(gt_dir, pred_dir):
    num_classes = 2
    name_classes = ['bg', 'road']
    hist = np.zeros((num_classes, num_classes))
    image_path_list = glob.glob(os.path.join(pred_dir, '*.{}'.format('png')))
    label_path_list = glob.glob(os.path.join(gt_dir, '*.{}'.format('jpg')))

    for ind in range(len(label_path_list)):
        pred = np.array(Image.open(image_path_list[ind]))
        label = np.array(Image.open(label_path_list[ind]))
        if len(label.flatten()) != len(pred.flatten()):
            print('Skipping: len(gt) = {:d}, len(pred) = {:d}, {:s}, {:s}'.format(len(label.flatten()), len(pred.flatten()), label_path_list[ind], image_path_list[ind]))
            continue
        try:
            hist += fast_hist(label.flatten(), pred.flatten(), num_classes)
        except:
            continue
        if ind > 0 and ind % 10 == 0:
            print('{:d} / {:d}: {:0.2f}'.format(ind, len(label_path_list), 100*np.mean(per_class_iu(hist))))
    
    mIoUs = per_class_iu(hist)
    for ind_class in range(num_classes):
        print('===>' + name_classes[ind_class] + ':\t' + str(round(mIoUs[ind_class] * 100, 2)))
    print('===> mIoU: ' + str(round(np.nanmean(mIoUs) * 100, 2)))
    return mIoUs

def main(args):
   compute_mIoU(args.gt_dir, args.pred_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('gt_dir', type=str, help='directory which stores gt images')
    parser.add_argument('pred_dir', type=str, help='directory which stores pred images')
    args = parser.parse_args()
    main(args)
