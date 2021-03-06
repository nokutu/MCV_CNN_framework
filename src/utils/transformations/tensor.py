import numpy as np
import torch


class ToTensor:
    def __call__(self, image):

        # image = torch.from_numpy(np.flip(image.transpose((2, 0, 1)),axis=0).copy())
        image = image[...,::-1]
        image = torch.from_numpy(image.transpose((2, 0, 1)).copy())
        image = image.float()#.div(255)
        return image


class ToTensorPIL:
    def __call__(self, image):
        image = np.array(image)
        # image = torch.from_numpy(np.flip(image.transpose((2, 0, 1)),axis=0).copy())
        image = image[...,::-1]
        image = torch.from_numpy(image.transpose((2, 0, 1)).copy())
        image = image.float()#.div(255)
        return image
