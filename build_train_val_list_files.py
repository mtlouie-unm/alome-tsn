import os
import sys
import argparse
import subprocess
import fileinput
import re

def make_filter(label):
    def my_filter(x):
        if label in x:
            return True
        else:
            return False
    return my_filter

def fix_train_val_prototxt(prototxt_path, prototxt_filename, count, toggle_batch_max):
    file = fileinput.FileInput(prototxt_path + '/' + prototxt_filename, inplace=True, backup='.bak')
    occurence_counter = 0
    for line in file:
        if occurence_counter < 1:
            if "    batch_size" in line:
                if count < 32 or toggle_batch_max:
                    sys.stdout.write("    batch_size: "+str(count))
                else:
                    sys.stdout.write("    batch_size: 32")
                occurence_counter += 1
            else:
                sys.stdout.write(line)
        else:
            sys.stdout.write(line)


def main(number_examples, classInd_path, frame_path, train_file_path):
    # classInd_path = ./100_data/classInd.txt
    f = open(classInd_path + '/classInd.txt', 'r')
    labels = f.readlines()

    class_label_list = []
    index = []

    # Build lists for class indices and class labels
    for label in labels:
        class_label = label.split(' ')
        class_label_list.append(class_label[1].replace('\n', '').replace('\r', ''))
        index.append(class_label[0])

    # Get a list of classes from directories
    # frame_path = ./100_videos
    directories = [x for x in os.listdir(frame_path)]

    # train_file_path = ./100_data/trainlist01.txt
    train_file = open(train_file_path + '/trainlist01.txt', 'w')
    val_file = open(train_file_path + '/testlist01.txt', 'w')
    test_file = open(train_file_path + '/TESTING_FILE.txt', 'w')
    for i, j in zip(class_label_list, index):
        filter14 = make_filter(i)
        filtered = filter(filter14, directories)
        result = [str(i) + '/' + k + '.avi ' + str(j) + '\n' for k in filtered]

        train_file.writelines(result[:number_examples])
        val_file.writelines(result[-2])
        test_file.writelines(result[-1])
        #print(result)

    train_file.close()
    val_file.close()
    test_file.close()

    # Fix Prototxts
    #fix_train_val_prototxt('/app/models/ucf101', 'tsn_bn_inception_flow_train_val.prototxt', number_examples, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('number_examples', type=int, help='The number of examples you want to construct')
    parser.add_argument('classInd_path', type=str, help='Path to the classInd.txt')
    parser.add_argument('frame_path', type=str, help="root directory holding the frames")
    parser.add_argument('train_file_path', type=str, help='path to write trainlist file')

    args = parser.parse_args()

    number_examples = args.number_examples
    classInd_path = args.classInd_path
    frame_path = args.frame_path
    train_file_path = args.train_file_path


    # num_data = 100
    # for count in xrange(10, num_data+1):
    #     main(count)
    #     break
    main(number_examples, classInd_path, frame_path, train_file_path)





