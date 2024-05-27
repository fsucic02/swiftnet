from torch import nn as nn
from torch.nn import functional as F

from models.util import upsample


class SemsegCrossEntropy(nn.Module):
    def __init__(self, num_classes, ignore_id=-100, print_each=20):
        super(SemsegCrossEntropy, self).__init__()
        self.num_classes = num_classes
        self.ignore_id = ignore_id
        self.step_counter = 0
        self.print_each = print_each

    def loss(self, y, t):
        #if y.shape[2:4] != t.shape[1:3]:
        #    y = upsample(y, t.shape[1:3])
        y_prob = F.softmax(y, dim=1)
        kl_loss = F.kl_div(y_prob.log(), t, reduction='batchmean')

        return kl_loss

    def forward(self, logits, labels, **kwargs):
        loss = self.loss(logits, labels)
        if (self.step_counter % self.print_each) == 0:
            print(f'Step: {self.step_counter} Loss: {loss.data.cpu().item():.4f}')
        self.step_counter += 1
        return loss
