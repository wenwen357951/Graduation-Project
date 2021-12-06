import os


dirname = ["A", "B", "C", "D", "E"]

if __name__ == '__main__':

    # verify train val in same layer using intersection
    for i in range(len(dirname)):
        trainpath = '/home/j2031linux3090/Graduation-Project/resources/k-fold/{}/train'.format(dirname[i])
        valpath = '/home/j2031linux3090/Graduation-Project/resources/k-fold/{}/val'.format(dirname[i])

        train_file = os.listdir(trainpath)
        val_file = os.listdir(valpath)

        print("\nmaindir:{}".format(dirname[i]))
        # val_set = set(train_file).intersection(set(val_file))
        # print(val_set)

        # very train dir from diff layer using intersection
        # dataset sort to 5 portion one to val else to train,so we have 5 val fold it can sort to A,B,C,D,E
        # val fold cant be the same even one image
        # DIR EXPLANATION
        # A FOLD TRAIN:1,2,3,4 VAL:5
        # B FOLD TRAIN:2,3,4,5 VAL:1
        # C FOLD TRAIN:3,4,5,1 VAL:2
        # D FOLD TRAIN:4,5,1,2 VAL:3
        # E FOLD TRAIN:5,1,2,3 VAL:4
        for idx in range(len(dirname)):
            trainpath_nextlayr ='/home/j2031linux3090/Graduation-Project/resources/k-fold/{}/train'.format(dirname[idx])
            train_file_nextlayr = os.listdir(trainpath_nextlayr)
            print("comperdir:{}".format(dirname[idx]))
            train_file_nextlayr_set = set(train_file).intersection(set(train_file_nextlayr))
            print(len(train_file_nextlayr_set))


