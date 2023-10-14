## What's New
## Introduction

Yolov5-face is a real-time,high accuracy face detection.

![](data/images/yolov5-face-p6.png)

## Data preparation

1. Download WIDERFace datasets.
2. Download annotation files from [google drive](https://drive.google.com/file/d/1tU_IjyOwGQfGNUvZGwWWM4SwxKp2PUQ8/view?usp=sharing).

```shell
cd data
python3 train2yolo.py /path/to/original/widerface/train [/path/to/save/widerface/train]
python3 val2yolo.py  /path/to/original/widerface [/path/to/save/widerface/val]
```



## Training

```shell
CUDA_VISIBLE_DEVICES="0,1,2,3" python3 train.py --data data/widerface.yaml --cfg models/yolov5s.yaml --weights 'pretrained models'
```

## WIDERFace Evaluation

```shell
python3 test_widerface.py --weights 'your test model' --img-size 640

cd widerface_evaluate
python3 evaluation.py
```
