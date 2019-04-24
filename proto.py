import sys
import os
import re
import fileinput
import math

def fix_prototxt(prototxt_path, prototxt_filename, num_epochs, size_training_set):
    file = fileinput.FileInput(prototxt_path + '/' + prototxt_filename, inplace=True, backup='.bak')
    for line in file:
            if "max_iter" in line:
                print("max_iter: " + str(math.ceil((num_epochs * size_training_set) / size_training_set)))
                # if size_training_set < 32:
                #     print("max_iter: "+str(math.ceil((num_epochs * size_training_set) / size_training_set)))
                # else:
                #     print("max_iter: "+str(math.ceil((num_epochs * size_training_set) / 32)))
                #print(re.sub("^batch_size:\s..$", "die", line), end='')
            else:
                print(line, end='')


def fix_train_val_prototxt(prototxt_path, prototxt_filename, count, toggle_batch_max):
    file = fileinput.FileInput(prototxt_path + '/' + prototxt_filename, inplace=True, backup='.bak')
    occurence_counter = 0
    for line in file:
        if occurence_counter < 1:
            if "    batch_size" in line:
                if count < 32 or toggle_batch_max:
                    print("    batch_size: "+str(count))
                else:
                    print("    batch_size: 32")
                occurence_counter += 1
            else:
                print(line, end='')
        else:
            print(line, end='')



fix_train_val_prototxt('./models/ucf101', 'tsn_bn_inception_flow_train_val.prototxt', 100, True)

fix_prototxt('./models/ucf101', 'tsn_bn_inception_flow_solver.prototxt', 10, 60000)