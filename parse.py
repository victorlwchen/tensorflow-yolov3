# convert labeled file
import os
from PIL import Image

label_path='/notebooks/datasets/certis_old_label'

type_ary=[]

def new_class(num):
    numbers = {
        '18' : "0",
        '37' : "1",
        '38' : "2"
    }

    return numbers.get(num, None)

def convert_all_files(path, target):
    img_path_root='/notebooks/datasets/certis'
    ary=[]
    count=0
    for f in os.listdir(path):
        img_path=os.path.join(img_path_root, f.replace('.txt','.jpg'))
        try:
            im = Image.open(img_path)
            width, height = im.size
            count+=1
            with open(os.path.join(label_path,f), 'r') as txt:
                lines = txt.readlines()
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
            pass
    print(count)    
    with open(target, "w") as txt_file:
        for line in ary:
            txt_file.write(line + "\n")

                
convert_all_files(label_path, '/notebooks/tensorflow-yolov3/data/dataset/certis_train.txt')
