# convert labeled file
import os
from PIL import Image



train_file_path='/mnt/darknet_VOC/train.txt'
test_file_path='/mnt/darknet_VOC/2007_test.txt'
train_target_path = '/mnt/darknet_VOC/tensor_train.txt'
test_target_path = '/mnt/darknet_VOC/tensor_test.txt'



def new_class(num):
    numbers = {
        '18' : "0",
        '37' : "1",
        '38' : "2"
    }

    return numbers.get(num, None)

def convert_all_files(path, target):
    
    ary=[]
    count=0
    with open(path,'r') as fp:
        img_paths = fp.readlines()
        for img_path in img_paths:
            img_path = img_path.strip()
            label_path=img_path.replace('.jpg','.txt')
            try:
                im = Image.open(img_path)
                width, height = im.size
                count+=1
                with open(label_path, 'r') as label:
                    lines = label.readlines()
                    new_line=''
                    objs=[]
                    for line in lines:
                        items=line.splitlines()[0].split(' ')

                        x_center=float(items[1])*width
                        y_center=float(items[2])*height
                        obj_w=float(items[3])*width
                        obj_h=float(items[4])*height

                        x_min=str(int(x_center-(obj_w/2)))
                        y_min=str(int(y_center-(obj_h/2)))
                        x_max=str(int(x_center+(obj_w/2)))
                        y_max=str(int(y_center+(obj_h/2)))
                        #class_id=new_class(items[0])
                        class_id=items[0]

                        if (int(x_min) < 0):
                            x_min=str(int(x_min)+1)
                        if (int(y_min) < 0):
                            y_min=str(int(y_min)+1)
                        if (int(x_max) > width ):
                            x_max=str(int(x_max)-1)
                        if(int(y_max) > height):
                            y_max=str(int(y_max)-1)

                        if class_id is None:
                            continue

                        objs.append(x_min+','+y_min+','+x_max+','+y_max+','+class_id)

                    if len(objs) != 0:
                        for obj in objs:
                            new_line+=' '+obj
                        ary.append(img_path+new_line)
            except Exception as e:
                print('Exception '+str(e))
                pass
    print(count)    
    with open(target, "w") as txt_file:
        for line in ary:
            txt_file.write(line + "\n")

                
convert_all_files(train_file_path, train_target_path)
convert_all_files(test_file_path, test_target_path)