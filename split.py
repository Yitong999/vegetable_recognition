# -*- coding: utf-8 -*-

import os
import random
from shutil import copy2

'''
    read from the src_data_folder, and seperate data into three folders --train, val, test 
    @param src_data_folder: source data folder
    @param target_data_folder: target data folder
    @param train_scale: the precentage of data for training
    @param val_scale: the precentage of data for evaluation
    @param test_scale: the precentage of data for testing
    :return:
    '''
def data_set_split(src_data_folder, target_data_folder, train_scale=0.8, val_scale=0.2, test_scale=0.0):

    print("Start spliting the data")
    class_names = os.listdir(src_data_folder)
    # create three files under the path
    split_names = ['train', 'val', 'test']
    for split_name in split_names:
        split_path = os.path.join(target_data_folder, split_name)
        if os.path.isdir(split_path):
            pass
        else:
            os.mkdir(split_path)
        # create vegetable category files under train, val, test files
        for class_name in class_names:
            class_split_path = os.path.join(split_path, class_name)
            if os.path.isdir(class_split_path):
                pass
            else:
                os.mkdir(class_split_path)

    # Copy the images to the right place according to the defined retio
    for class_name in class_names:
        current_class_data_path = os.path.join(src_data_folder, class_name)
        current_all_data = os.listdir(current_class_data_path)
        current_data_length = len(current_all_data)
        current_data_index_list = list(range(current_data_length))
        random.shuffle(current_data_index_list)

        train_folder = os.path.join(os.path.join(target_data_folder, 'train'), class_name)
        val_folder = os.path.join(os.path.join(target_data_folder, 'val'), class_name)
        test_folder = os.path.join(os.path.join(target_data_folder, 'test'), class_name)
        train_stop_flag = current_data_length * train_scale
        val_stop_flag = current_data_length * (train_scale + val_scale)
        current_idx = 0
        train_num = 0
        val_num = 0
        test_num = 0
        for i in current_data_index_list:
            src_img_path = os.path.join(current_class_data_path, current_all_data[i])
            if current_idx <= train_stop_flag:
                copy2(src_img_path, train_folder)

                train_num = train_num + 1
            elif (current_idx > train_stop_flag) and (current_idx <= val_stop_flag):
                copy2(src_img_path, val_folder)

                val_num = val_num + 1
            else:
                copy2(src_img_path, test_folder)

                test_num = test_num + 1

            current_idx = current_idx + 1

        print("--------------------------{}--------------------------".format(class_name))
        print(
            "{} images are splited into three groups according to radio{}：{}：{}. There are totally{}images".format(class_name, train_scale, val_scale, test_scale, current_data_length))
        print("Train Set{}：{}".format(train_folder, train_num))
        print("Valuation Set{}：{}".format(val_folder, val_num))
        print("Testing Set{}：{}".format(test_folder, test_num))


if __name__ == '__main__':
    src_data_folder = "ori_data"   #origin data path
    target_data_folder = "data"  #the path for splited data
    isExist = os.path.exists(target_data_folder)
    if not isExist:
        os.makedirs(target_data_folder)
    data_set_split(src_data_folder, target_data_folder)
