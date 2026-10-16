import os
from PIL import Image
import torch
from torch import nn
from model import Mymodel
import matplotlib.pyplot as plt
# 异常或者损坏的图片（假设图片在与.py程序并列的data文件夹里）
def check_image(path):
    bad_files=[]
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith((".jpg",".jpeg",".png",".bmp")):
                img_path=os.path.join(root,file)
                try:
                    img=Image.open(img_path)
                    img.verify()
                except:
                    bad_files.append(img_path)
    return bad_files
bad=check_image('./data')
print('损坏图片：')
print(bad)

#划分数据集
if not bad==[]:        #剔除坏文件
    for file in bad:
        os.remove(file)
from torchvision.datasets import ImageFolder
train_datasets=ImageFolder(root='./data/train')       #ImageFolder负责：找到图片在哪里
test_datasets=ImageFolder(root='./data/test')
print(train_datasets.classes)
print(test_datasets.classes)


#数据增强&改变形状和张量（读取时输出这种）
from torchvision import transforms                   #transform负责：图片如何处理
train_transform=transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
    transforms.ToTensor()
])
test_transform=transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()               #注意：这里的Totensor函数只是说之后读取时自动读取其张量形式，在test_transform里储存还是路径+数字类别
])
train_datasets=ImageFolder(root='./data/train',transform=train_transform)
test_datasets=ImageFolder(root='./data/test',transform=train_transform)


#处理图片按批次喂给CNN
from torch.utils.data import DataLoader
train_loader=DataLoader(                #注意：这里的train_loader本质上只是一个不断生成batch的迭代器，并没有真正储存所有转化后的train_datasets
    train_datasets,
    batch_size=32,
    shuffle=True
)

test_loader=DataLoader(
    test_datasets,                
    batch_size=32,
    shuffle=False
)

model = Mymodel()
device="cuda"
model=model.to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer=torch.optim.SGD(model.parameters(),lr=0.01)
loss_history=[]
epoch_history=[]
test_accuracy_history=[]
for epoch in range(100):
    total_loss = 0
    batch_num=0
    for imgs,labels in train_loader:                    #每次取出的imgs格式torch.Size([32, 3, 224, 224])，torch不断迭代直到全部取出为止
        batch_num += 1
        imgs=imgs.to(device)
        labels=labels.to(device)
        outputs=model(imgs)
        loss=loss_fn(outputs,labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss+=loss.item()
    epoch_history.append(epoch)
    loss_history.append(total_loss/batch_num)
    with torch.no_grad():
        correct=0
        total=0
        for imgs,labels in test_loader: 
            imgs=imgs.to(device)
            labels=labels.to(device)
            test_outputs=model(imgs)
            values, indices = torch.max(test_outputs,1)
            total+=labels.size(0)
            correct+=(indices==labels).sum().item()
    test_accuracy=correct/total
    test_accuracy_history.append(test_accuracy)
    if epoch%1==0:
        print(f'当前训练轮次{epoch+1},loss={loss}')

torch.save(model.state_dict(),'flower_model1.1.pth')


plt.figure(figsize=(10, 6))
plt.plot(epoch_history,loss_history,color='red',linewidth=2,label='loss')
plt.title(f'train final loss:{loss_history[-1]:.4f}')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend()
plt.grid(True)
plt.savefig('loss_curve1.1.png',dpi=300,)
plt.show()



plt.figure(figsize=(10, 6))
plt.plot(epoch_history,test_accuracy_history,color='blue',linewidth=2,label='test_accuracy')
plt.title(f'test final accuracy:{test_accuracy_history[-1]:.4f}')
plt.xlabel('epoch')
plt.ylabel('test_accuracy')
plt.legend()
plt.grid(True)
plt.savefig('accuracy_curve1.1.png',dpi=300,)
plt.show()
