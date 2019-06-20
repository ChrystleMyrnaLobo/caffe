#!/bin/bash
# Usage parse_log.sh caffe.log
# It creates the following two text files, each containing a table:
# caffe.log.monitor (columns: '#Iters Seconds TrainLoss LearningRate TestLoss TestMAP TestAPCow TestAPDog TestARCow TestARDog')

# get the dirname of the script
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

if [ "$#" -lt 1 ]
then
echo "Usage parse_log_v2.sh /path/to/your.log"
exit
fi
LOG=`basename $1`
sed -n '/Iteration .* Testing net/,/Iteration *. loss/p' $1 > aux.txt
sed -i '/Waiting for data/d' aux.txt
sed -i '/prefetch queue empty/d' aux.txt
sed -i '/Iteration .* loss/d' aux.txt
sed -i '/Iteration .* lr/d' aux.txt
sed -i '/Train net/d' aux.txt
sed -i '/Missing true_pos for label/d' aux.txt
# #iters
grep 'Iteration ' aux.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > aux0.txt
# Test mAP
grep 'Test net output #0' aux.txt | awk '{print $11}' > aux1.txt
# Test loss
grep 'Test loss:' aux.txt | awk '{print $7}' > aux2.txt
#grep 'Test net output #1' aux.txt | awk '{print $11}' > aux2.txt

## Class wise accuracy
grep 'APclass1:' aux.txt | awk '{print $6}' > ap_c1.txt
grep 'APclass2:' aux.txt | awk '{print $6}' > ap_c2.txt
## Class wise recall
grep 'ARclass1:' aux.txt | awk '{print $6}' > ar_c1.txt
grep 'ARclass2:' aux.txt | awk '{print $6}' > ar_c2.txt

# Extracting elapsed seconds
# For extraction of time since this line contains the start time
grep '] Solving ' $1 > aux3.txt
grep 'Testing net' $1 >> aux3.txt
$DIR/extract_seconds.py aux3.txt aux4.txt

# For extraction of time since this line contains the start time
grep '] Solving ' $1 > aux.txt
grep ', loss = ' $1 >> aux.txt
# Train loss
grep ', loss = ' $1 | awk '{print $9}' > aux5.txt
# Learning rate
grep ', lr = ' $1 | awk '{print $9}' > lr.txt

## Generating
echo "#Iters Seconds TrainLoss LearningRate TestLoss TestMAP TestAPCow TestAPDog TestARCow TestARDog" > $LOG.monitor
paste aux0.txt aux4.txt aux5.txt lr.txt aux2.txt aux1.txt ap_c2.txt ap_c1.txt ar_c2.txt ar_c1.txt | column -t >> $LOG.monitor
rm aux.txt aux0.txt aux1.txt aux2.txt aux3.txt aux4.txt ap_c1.txt ap_c2.txt ar_c1.txt ar_c2.txt aux5.txt lr.txt
