from fastapi import FastAPI, UploadFile
import uvicorn
from model import Mymodel
import torch
from torchvision import transforms
from PIL import Image

model=Mymodel().to('cuda')
model.load_state_dict(torch.load('flower_model1.1.pth',map_location='cuda'))
model.eval()

app=FastAPI()



@app.get('/home')
async def home():
    return{
        'message':'ML API function normally'
    }



@app.post('/Upload_file',tags=['模型使用'])
async def use(file:UploadFile):
    print('file',file)
    image = Image.open(file.file).convert("RGB")
    file_transform=transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor()               
    ])
    file_t=file_transform(image)
    file_t=file_t.unsqueeze(0).to('cuda')
    with torch.no_grad():
        output=model(file_t)
        value, indice = torch.max(output,1)
        flowers=['daisy','dandelion','rose','sunflower','tulip']
        flower_name=flowers[indice.item()]
    return {'flower_name':flower_name}






if __name__=='__main__':
    uvicorn.run('app1:app',port=8000,reload=True)