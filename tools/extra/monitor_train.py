import pandas as pd
import os
import matplotlib.pyplot as plt

mode="VGG_ca_SSD_300x300"

path_to_log = "/home/chrystle/MTP2/ssd_caffe/jobs/VGGNet/CuratedAnimal/SSD_300x300/VGG_ca_SSD_300x300.log"

#os.chdir("monitor")
parse_log_script = "/home/chrystle/MTP2/ssd_caffe/tools/extra/parse_log_check.sh"
os.system('%s %s' % (parse_log_script, path_to_log))

hdr = "Iters Seconds TestLoss TestMAP TestAPCow TestAPDog TestARCow TestARDog".split()
file_name = mode + ".log.test"
df = pd.read_csv(file_name, delimiter='\s+', skiprows=1, names=hdr)
#df= df.drop([0]) # Skip initial state OR iter 0 
test_loss = df['TestLoss']
test_iters = df['Iters']

hdr = 'Iters Seconds TrainLoss LearningRate'.split()
file_name = mode + ".log.train"
df_tr =  pd.read_csv(file_name, delimiter='\s+', skiprows=1, names=hdr)
train_loss = df_tr['TrainLoss']
train_iters = df_tr['Iters']

# Plot Iters vs Loss (Train and Test)
plt.plot(train_iters, train_loss, '-go', label="Train")
plt.plot(test_iters, test_loss, '-bo', label="Val")
plt.legend(loc='upper right')
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.savefig(mode+"_loss.png") #save before show
plt.show()

test_map = df['TestMAP']
test_ap_cow = df['TestAPCow']
test_ap_dog = df['TestAPDog']

# Plot Iters vs Precision (mAP and AP cow dog)
plt.plot(test_iters, test_map, '--ko', label="Val mAP")
plt.plot(test_iters, test_ap_dog, '-mo', label="Val AP Dog")
plt.plot(test_iters, test_ap_cow, '-bo', label="Val AP Cow")

plt.legend(loc='lower right')
plt.xlabel('Iteration')
plt.ylabel('Val Average Precision')
plt.savefig(mode+"_precision.png") #save before show 
plt.show()

test_ar_cow = df['TestARCow']
test_ar_dog = df['TestARDog']

# Iter vs Recall (AR per class)
plt.plot(test_iters, test_ar_dog, '-ro', label="Val AR Dog")
plt.plot(test_iters, test_ar_cow, '-go', label="Val AR Cow")
plt.legend(loc='lower right')
plt.xlabel('Iteration')
plt.ylabel('Val Average Precision')
plt.savefig(mode+"_recall.png") #save before show 
plt.show()

