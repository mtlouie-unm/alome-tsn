#!/bin/bash

mkdir /app/training_logs
mkdir /app/testing_logs
mkdir /app/test_scores

cd /app/data/ucf101_splits
touch trainlist02.txt trainlist03.txt testlist02.txt testlist03.txt

cd /app

cp tools/eval_net.py /app

start=1
end=10
for((i=start; i<=end; i++))
do
    echo "Training with $i examples per class"
    python /app/data/ucf101_splits/build_train_val_list_files.py $i /app/data/ucf101_splits /mnt/out /app/data/ucf101_splits
    bash /app/scripts/build_file_list.sh ucf101 /mnt/out

    echo "Begin Training with $i example per class"
    bash /app/scripts/train_tsn.sh ucf101 flow 2>&1 | tee /app/training_logs/train_log_$i.txt


    echo "Begin Testing with Test set"
    rm /app/data/ucf101_splits/ucf101_flow_val_split_1.txt
    cp test_set.txt ucf101_flow_val_split_1.txt
    python eval_net.py ucf101 1 flow /mnt/out \
     models/ucf101/tsn_bn_inception_flow_deploy.prototxt models/ucf101_split1_tsn_flow_bn_inception_iter_2000.caffemodel \
    --num_worker 1 --save_scores /app/test_scores/score_test_$i > /app/testing_logs/test_log_$i.txt
done