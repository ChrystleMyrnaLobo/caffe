#!/bin/bash
# Parse the log geberated during test.sh (which evaluates a trained model) to class wise accuracy, precision and recall values VOC2007 style
# Usage parse_log_test.sh caffe.log
# It creates a text files with class accuracy and pr at each point
#     caffe.log.prcurve (columns: 'Recall PrecisionClass1 PrecisionClass2 PrecisionClass3')
#     caffe.log.summary (colums: '#Iter TestLoss TestAccuracy TestClass1Accuracy TestClass2Accuracy TestClass3Accuracy')

# get the dirname of the script
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

if [ "$#" -lt 1 ]
then
echo "Usage parse_log.sh /path/to/your.log"
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
grep 'Iteration ' aux.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > aux0.txt
grep 'Test net output #0' aux.txt | awk '{print $11}' > aux1.txt
grep 'Test loss:' aux.txt | awk '{print $7}' > aux2.txt

# Precision Recall Curve table
# Extract class wise precision and recall values from the log
echo "" > pr.txt
for idx in 1 2 3
do
  grep "class${idx} p-r value " aux.txt | awk '{print $9}' > pr_class.txt  
  paste pr.txt pr_class.txt | column -t  > tmp.txt
  mv tmp.txt pr.txt
  grep "class${idx} p-r value " aux.txt | awk '{print substr($8, 1, length($8)-1) }' > rc.txt
done

# Make table of pr values
echo 'Recall PrecisionDog PrecisionCow PrecisionSignboard ' > $LOG.prcurve
paste rc.txt pr.txt | column -t >> $LOG.prcurve
rm pr_class.txt pr.txt rc.txt

# Class wise accuracy
grep 'class1:' aux.txt | awk '{print $6}' > class1.txt
grep 'class2:' aux.txt | awk '{print $6}' > class2.txt
grep 'class3:' aux.txt | awk '{print $6}' > class3.txt

# Summary of accuracy
echo '#Iters TestAccuracy TestLoss TestDogAccuracy TestCowAccuracy TestSignboardAccuracy'> $LOG.summary
paste aux0.txt aux1.txt aux2.txt class1.txt class2.txt class3.txt | column -t >> $LOG.summary
rm aux.txt aux0.txt aux1.txt aux2.txt class1.txt class2.txt class3.txt

