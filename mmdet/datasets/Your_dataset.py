from .coco import CocoDataset
from .registry import DATASETS
 
#add new dataset
@DATASETS.register_module
class Your_Dataset(CocoDataset):
    CLASSES = ['road']
 