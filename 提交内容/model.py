import torch
from torch import nn
import torch.nn.functional as F

class Mymodel(nn.Module):
    def __init__(self):
        super(Mymodel, self).__init__()
        self.conv1 = nn.Conv2d(3,96,kernel_size=(11,11),padding=2,stride=4)
        self.conv2 = nn.Conv2d(96,256,kernel_size=5,padding=2,stride=1)
        self.conv3 = nn.Conv2d(256,384,kernel_size=3,padding=1,stride=1)
        self.conv4 = nn.Conv2d(384,384,kernel_size=3,padding=1,stride=1)
        self.conv5 = nn.Conv2d(384,256,kernel_size=3,padding=1,stride=1)
        
        
        self.pool = nn.MaxPool2d(3,padding=0,stride=2)
        
        self.fc1 = nn.Linear(6*6*256, 4096)
        self.fc2 = nn.Linear(4096, 4096)
        self.fc3 = nn.Linear(4096, 5)

    def forward(self, x):
        x=self.conv1(x)
        x=F.relu(x)
        x=self.pool(x)
        x=self.conv2(x)
        x=F.relu(x)
        x=self.pool(x)
        x=self.conv3(x)
        x=F.relu(x)
        x=self.conv4(x)
        x=F.relu(x)
        x=self.conv5(x)
        x=F.relu(x)
        x=self.pool(x)
        x=torch.flatten(x,start_dim=1)
        x=self.fc1(x)
        x=F.relu(x)
        x=self.fc2(x)
        x=F.relu(x)
        x=self.fc3(x)
        return x