#!/bin/bash

# visualization

config='solov2_r50_fpn_8gpu_3x'
# model='solov2_release_r50_fpn_8gpu_3x_scale'
model='solov2_release_r50_fpn_8gpu_3x'
epoch='20'

python tools/test_ins_vis.py configs/solov2/$config.py  work_dirs/$model/epoch_$epoch.pth --show --save_dir  work_dirs/vis/$model"_epoch"$epoch


















# test_evaluate

# config='solov2_r50_fpn_8gpu_3x'
# model='solov2_release_r50_fpn_8gpu_3x'
# epoch='30'

# config='solov2_r50_fpn_8gpu_3x'
# model='solov2_release_r50_fpn_8gpu_3x_scale'
# epoch='30'

# python tools/test_ins.py configs/solov2/$config.py work_dirs/$model/epoch_$epoch.pth --show --out  work_dirs/$model/results_solo.pkl --eval segm >> eval/$model"_epoch_"$epoch.txt