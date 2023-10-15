"""Import Modules"""
import os
import shutil
import cv2 as cv
import argparse


# ARGPARSE
parser = argparse.ArgumentParser(description='Process some aurguments')
parser.add_argument('--source_folder', default="./Face-Detection-Datasets", type=str, help='dataset source folder address')
args = parser.parse_args()

source = args.source_folder
file_dir = os.path.join(source, "wider_face_split")

train_image_dir = os.path.join(source, "WIDER_train/images/")
val_image_dir = os.path.join(source, "WIDER_val/images/")
train_output_dir = os.path.join(source, "labels/train")
val_output_dir = os.path.join(source, "labels/val")
img_train_out_dir = os.path.join(source, "images/train")
img_val_out_dir = os.path.join(source, "images/val")
train_filename_dir = file_dir + '/wider_face_train_bbx_gt.txt'
val_filename_dir = file_dir + '/wider_face_val_bbx_gt.txt'


if not os.path.exists(train_output_dir):
    os.makedirs(train_output_dir)
else:
    os.system("rm -r " + train_output_dir)
    os.mkdir(train_output_dir)

if not os.path.exists(img_train_out_dir):
    os.makedirs(img_train_out_dir)
else:
    os.system("rm -r " + img_train_out_dir)
    os.mkdir(img_train_out_dir)

if not os.path.exists(val_output_dir):
    os.makedirs(val_output_dir)
else:
    os.system("rm -r " + val_output_dir)
    os.mkdir(val_output_dir)

if not os.path.exists(img_val_out_dir):
    os.makedirs(img_val_out_dir)
else:
    os.system("rm -r " + img_val_out_dir)
    os.mkdir(img_val_out_dir)


class Convert_widerface2yolo:
    """
    Convert widerface dataset to yolo format
    """
    def __init__(self):
        pass

    def modify_name(self, path):
        """
        Get path and return name and dir
        """
        actname = str(path).strip('/.jpg\n')
        hash_position = actname.find('/')
        name = str(actname[hash_position+1:])
        dir_ = str(actname[:hash_position])
        return name, dir_

    def modify_label(self, label_ori, org_shape):
        """
        Find labels and normalize
        """
        tem_lab = label_ori.split()
        tem_label = list(map(int, tem_lab[:4]))

        tem_label_new = {}
        x1 = tem_label[0] / org_shape[1] #x1
        y1 = tem_label[1] / org_shape[0] #y1
        w = tem_label[2] / org_shape[1] #w
        h = tem_label[3] / org_shape[0] #h
        x = x1 + w/2
        y = y1 + h/2
        tem_label_new[0] = x
        tem_label_new[1] = y
        tem_label_new[2] = w
        tem_label_new[3] = h

        str_label = list(map(str, list(tem_label_new.values())))
        label = ' '.join(str_label)
        return label

    def read_imageshape(self, dir):
        """
        Get image shape
        """
        img = cv.imread(dir)
        shape = img.shape[:2]  # (H, W)
        return shape

    def convert(self, list_content, image_dir, out_dir):
        """
        Convert labels
        """
        i = 0
        while i < len(list_content):
            if '.jpg' in str(list_content[i]):
                image_name, image_ab_dir = self.modify_name(list_content[i])
                img_shape = self.read_imageshape(image_dir + image_ab_dir + '//' + image_name + '.jpg')
                num_face = int(list_content[i + 1])
                labels = ''
                lab = {}
                for j in range(num_face):  # find labels
                    lab[j] = str('0 ' + self.modify_label(list_content[i + 1 + j + 1], img_shape) + '\n')
                    labels = labels + lab[j]
                i = i + num_face + 2
                with open(os.path.join(out_dir, image_name + '.txt'), 'w') as file_write:
                    file_write.write(labels)
            else:
                i = i + 1
            print(i)

    def widerface2yolo(self, filename_dir, image_dir, output_dir):
        """
        Read input text files
        """
        with open(filename_dir, 'r') as train_file:
            list_train_content = train_file.readlines()
            self.convert(list_train_content, image_dir, output_dir)

    def image_copy(self, image_dir, img_out_dir):
        """
        Copy images
        """
        list_doc_name = os.listdir(image_dir)
        for i, _ in enumerate(list_doc_name):
            list_file_name = os.listdir(image_dir+list_doc_name[i])
            for j, _ in enumerate(list_file_name):
                shutil.copyfile(image_dir+'//'+list_doc_name[i]+'//'+list_file_name[j], img_out_dir+'//'+list_file_name[j])

    def draw_bb(self, image_dir, label_dir, out_path):
        """
        Draw bbox
        """
        img = cv.imread(image_dir)
        with open(label_dir, 'r') as f:
            list_label = f.readlines()
            for i in range(len(list_label)):
                list_label_tem = list_label[i].strip('\n')
                new_list = list_label_tem.split(" ")
                list_label_tem2 = list(map(int, new_list[:5]))
                x, y, w, h = int(list_label_tem2[0]), int(list_label_tem2[1]), int(list_label_tem2[2]), int(list_label_tem2[3])
                cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1) #(, (x1,y1), (x2,y2),...) corner points
        cv.imwrite(out_path+'test.jpg', img)


widerface2yolo_cls = Convert_widerface2yolo()

widerface2yolo_cls.widerface2yolo(train_filename_dir, train_image_dir, train_output_dir)
widerface2yolo_cls.widerface2yolo(val_filename_dir, val_image_dir, val_output_dir)
widerface2yolo_cls.image_copy(train_image_dir, img_train_out_dir)
widerface2yolo_cls.image_copy(val_image_dir, img_val_out_dir)
