'''

Author: nyismaw
Main program for Casava image files as a part of an in-class kaggle competition
https://www.kaggle.com/c/cassava-disease/

https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
'''

import torch
import torchvision
import torchvision.transforms as transforms
import data_loader
import constants as C
import model
import time
import train
import sys
import argparse
from torchsummary import summary

def main(argv):

    parser = argparse.ArgumentParser(description='Cassava Disease Classification')
    parser.add_argument("-m","--model_path", help="Model path extention."
                , type=str)
    args = parser.parse_args(argv[1:])
    model_path = args.model_path

    print("Model path is %s" %(model_path))

    print("Program started ")

    print("Creating a transform ... ")

    transform = transforms.Compose(
        [
        transforms.ToPILImage(),
        torchvision.transforms.Resize((C.AVERAGE_HEIGHT, C.AVERAGE_WIDTH)),
        transforms.ToTensor()
        # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    # transform = None
    print("Creating train data set ... ")
    train_data_set = data_loader.CassavaImagesDataset(C.TRAIN_DATA_PATH, C.TRAIN_LABEL_PATH
                                                                        , transform)
    print("Creating train data loader ... ")
    train_loader = torch.utils.data.DataLoader(train_data_set, batch_size=4,
                                              shuffle=True, num_workers=2)

    print("Creating val data set ... ")
    val_data_set    = data_loader.CassavaImagesDataset(C.VAL_DATA_PATH, C.VAL_LABEL_PATH
                                                                        , transform)
    print("Creating a val data loader ... ")
    val_loader = torch.utils.data.DataLoader(val_data_set, batch_size=4,
                                             shuffle=False, num_workers=2)

    print("Creating a model ... ")
    casava_model = model.ResNet()
    if model_path is not None:
        # if there is a saved model, try to load it
        try:
            casava_model.load_state_dict(torch.load( model_path  ))
            print("Model %s loaded " %(model_path))
        except Exception as e:
            print("Failed to load model %s. %s" %(model_path, str(e)))


    train.train(train_loader, casava_model)


if __name__ == '__main__':
    main(sys.argv)
