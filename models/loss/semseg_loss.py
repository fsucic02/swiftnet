from torch import nn as nn
from torch.nn import functional as F
import torch
from models.util import upsample
import numpy as np
from PIL import Image

class SemsegCrossEntropy(nn.Module):
    def __init__(self, num_classes, ignore_id=-100, print_each=20):
        super(SemsegCrossEntropy, self).__init__()
        self.num_classes = num_classes
        self.ignore_id = ignore_id
        self.step_counter = 0
        self.print_each = print_each

    def loss(self, y, t):
        kl_loss = F.kl_div(F.log_softmax(y / 5, dim=1), t, reduction='sum')
        
        loss = kl_loss * 25/ (3*448*448)
        
        return loss

    def forward(self, logits, labels, **kwargs):
        loss = self.loss(logits, labels)
        if (self.step_counter % self.print_each) == 0:
            print(f'Step: {self.step_counter} Loss: {loss.data.cpu().item():.4f}')
        self.step_counter += 1
        return loss
