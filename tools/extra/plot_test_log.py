 #!/usr/bin/env python

# https://blog.csdn.net/xunan003/article/details/79252162
# coding:utf-8

import inspect
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def get_log_parsing_script():
    dirname = os.path.dirname(os.path.abspath(inspect.getfile(
        inspect.currentframe())))
    return dirname + '/parse_log_test.sh'

def get_log_file_suffix():
  return 'log'

def get_data_file_suffix():
  return 'prcurve'
  
def get_summary_file_suffix():
  return 'summary'
  
def get_data_file(path_to_log):
  return (os.path.basename(path_to_log) + '.' + get_data_file_suffix())

def get_summary_file(path_to_log):
  return (os.path.basename(path_to_log) + '.' + get_summary_file_suffix())

def plot_curve(title, recall, precision, path_to_save):
  tick = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
  plt.figure()
  plt.title("PR curve on test data for " + title)
  plt.xlabel('Recall')
  plt.ylabel('Precision')
  plt.axis([0, 1, 0, 1.05])
  plt.xticks(tick)
  plt.yticks(tick)
  plt.plot(recall, precision)
  
  plt.savefig(path_to_save)
  plt.show()

def plot_chart(path_to_png, path_to_log):
  # Parse and create .prcurve and .summary files
  os.system('%s %s' % (get_log_parsing_script(), path_to_log))
  data_file = get_data_file(path_to_log)
  data = np.loadtxt(data_file, skiprows=1)
  
  # #Iter Loss Accuracy DogAccuracy CowAccuracy SignboardAccuracy
  data_file = get_summary_file(path_to_log)
  smm = np.loadtxt(data_file, skiprows=1)
  
  mean_precision = np.mean(data[:,1:],axis=1)
  recall = np.divide(data[:,0],10)

  title = 'Dog, AP={}'.format(smm[3]*100)
  plot_curve(title, recall, data[:,1], "dog_"+path_to_png)
  
  title = 'Cow, AP={}'.format(smm[4]*100)
  plot_curve(title, recall, data[:,2], "cow_"+path_to_png)
 
  title ='Signboard, AP={}'.format(smm[5]*100)
  plot_curve(title, recall, data[:,3], "signboard_"+path_to_png)

  title = 'Overall, AP={}'.format(smm[2]*100)
  plot_curve(title, recall, mean_precision, path_to_png)

if __name__ == '__main__':
  if len(sys.argv) < 1:
    print """ Usage :
    ./plot_prcurve.py /where/to/save.png /path/to/.log.prcurve
     """
    sys.exit()
  else:
    path_to_png = sys.argv[1]
    if not path_to_png.endswith('.png'):
       print 'Path must ends with png' % path_to_png
       sys.exit()
    path_to_log = sys.argv[2]
    if not os.path.exists(path_to_log):
       print 'Path does not exist: %s' % path_to_log
       sys.exit()
    if not path_to_log.endswith(get_log_file_suffix()):
       print 'Log file must end in %s.' % get_log_file_suffix()
       sys.exit()
    plot_chart(path_to_png, path_to_log)
