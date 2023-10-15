import os
import cv2

input_dir = "./widerface/WIDER_val/images"
input_texts = "./runs/detect/exp81/labels"
output_dir = "./runs/detect/exp81/verify"

for folder in os.listdir(input_dir):
    if not os.path.exists(os.path.join(output_dir, folder)):
        os.makedirs(os.path.join(output_dir, folder))

    for img_name in os.listdir(os.path.join(input_dir, folder)):
        img = cv2.imread(os.path.join(input_dir, folder, img_name))
        txt_file = os.path.join(input_texts, folder, img_name).replace("jpg", "txt")
        with open(txt_file, 'r') as f:
            obj_lines = [l.strip() for l in f.readlines()]

        for i, obj_line in enumerate(obj_lines):
            try:
                print(i, obj_line)
                cx, cy, nw, nh, _ = [float(item) for item in obj_line.split(' ')]
                color = (0, 255, 0)
                cv2.rectangle(img, (int(cx), int(cy)), (int(cx+nw), int(cy+nh)), color, 1)
            except:
                pass
        cv2.imwrite(os.path.join(output_dir, folder, img_name), img)
