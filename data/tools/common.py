#-*- coding:utf-8 –*-
import json
import os
import shutil
# 获取源路径的所有图片目录
def getAllPath(dirpath, *suffix):
    PathArray = []
    for r, ds, fs in os.walk(dirpath):
        for fn in fs:
            if os.path.splitext(fn)[1] in suffix:
                fname = os.path.join(r, fn)
                PathArray.append(fname)
    return PathArray
# 从源路径中读取所有图片放入一个list，然后逐一进行检查，把其中的脸扣下来，存储到目标路径中
def rename(dir, name,*suffix):    
    try:
        ImagePaths = getAllPath(dir, *suffix)
        #print len(ImagePaths)
        count = 971
        for imagePath in ImagePaths:
            print(imagePath)
            os.rename(imagePath,dir+'/'+name+'_%d'%count+'.jpg')
            count +=1
          
    except IOError:
        print
        "Error"

    else:
        print
        'Find ' + str(count - 1) + '  to Destination '

def load_json(filenamejson):
    with open(filenamejson) as f:
        raw_data = json.load(f)
    return raw_data

#统计图片数量
# 读取json文件，将标注图片移动到已标注图片文件夹，删除没有目标的标注信息
def main(imgsrc_dir, imgdes_img, jsonsrc_dir,jsondes_dir, merge_flag, merge_json):
    json_paths = getAllPath(jsonsrc_dir, '.json')
    for json_path in json_paths:
        # 读取 json 文件数据
        with open(json_path, 'r') as load_f:
            print (json_path)
            content = json.load(load_f)
        new_dict = {}
        # 循环处理
        for t in content:
            filename = content[t]['filename']
            regions =  content[t]['regions']
            if(len(regions)==0):
                print (filename+':no regions')
                continue
            else:
                print (filename+':*****')
                print (len(regions))
                new_dict.update({t:content[t]})
                shutil.copy(imgsrc_dir+filename,imgdes_img+filename)
                
        with open(jsondes_dir + os.path.basename(json_path), "w") as f:
            json.dump(new_dict, f)
    
    if(merge_flag):
        merge_dict = {}
        i = 0
        for json_path in getAllPath(jsondes_dir, '.json'):
            print(json_path)
            with open(json_path, 'r') as load_f:
                content = json.load(load_f)
            for t in content:
                merge_dict[str(i)] = content[t]
                i += 1
        with open(merge_json, "w") as f:
            json.dump(merge_dict, f)  

if __name__ == '__main__':
    isrename =0
    if isrename ==1:
        dir ='../PZ_image'
        rename(dir, 'pz','.jpg')
    else:
        imgsrc_dir ='/home/yly/work/dataset/CNL_imgs/'
        imgdes_img ='/home/zq/work/SOLO/data/road/val/'
        jsonsrc_dir ='/home/zq/work/SOLO/data/annotation/val/'
        jsondes_dir ='/home/zq/work/SOLO/data/annotation/merge/val/'
        merge_json = '/home/zq/work/SOLO/data/annotation/merge/merge_val_json.json'
        merge_flag = True

        # imgsrc_dir ='/home/yly/work/dataset/CNL_imgs/'
        # imgdes_img ='/home/zq/work/SOLO/data/road/train/'
        # jsonsrc_dir ='/home/zq/work/SOLO/data/annotation/train/'
        # jsondes_dir ='/home/zq/work/SOLO/data/annotation/merge/train/'
        # merge_json = '/home/zq/work/SOLO/data/annotation/merge/merge_train_json.json'
        # merge_flag = True

        if not os.path.exists(imgdes_img):
            os.makedirs(imgdes_img)
        if not os.path.exists(jsondes_dir):
            os.makedirs(jsondes_dir)
        main(imgsrc_dir,imgdes_img,jsonsrc_dir,jsondes_dir,merge_flag,merge_json)