#tensorflow checkpoint file is almost the same with yolov3 weight file, we can add header from original weight  

header_size = 20
header_file = 'yolov3.weights'  
source_file = 'yolov3.weights'  #check point file
target_file = 'yolov3_new.weights'

with open(header_file,'rb') as hf, open(source_file,'rb') as sf,open(target_file,'wb') as tf:
    header = hf.read(header_size)
    data = sf.read()
    tf.write(header + data)
