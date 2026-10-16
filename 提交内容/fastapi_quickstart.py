from fastapi import FastAPI, Form, File, UploadFile  #一个具体的类
import uvicorn
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List,Union,Optional
import os


app = FastAPI()

@app.get('/')   #是一个映射，每个路由对应它的映射函数，还有把get变成post就成了post请求，put delete等等
async def home():
    return {'user_id':1003}    #会帮你转成json字符串
#uvicorn本质上就是给中间层，负责接收封装等等

@app.get('/shop')   #是一个映射，每个路由对应它的映射函数，还有把get变成post就成了post请求，put delete等等
async def home():
    return {'haha':114514}    #会帮你转成json字符串
#uvicorn本质上就是给中间层，负责接收封装等等

@app.post('/item',tags=['这是一个items的测试接口'],
            summary='this is item 测试 summary',
            description='this is item 测试 description...',
            response_description='this is item 测试 respones_description...'
          )
async def test():
    return {'items':'items数据'}


class Addr(BaseModel):
    province:str
    city:str

class User(BaseModel):
    #name:str = Field(regex='^a')    #要求一定要以a开头     或者name = 'root' 代表默认是root
    name:str 
    age:int = Field(default=0,gt=0,lt=100)
    birth: Union[date,None]=None 
    friends:List[int]=[]
    description:Optional[str]=None
    addr:Addr

    #校验字段
    @field_validator('name')         #name是限定字段
    def name_must_alpha(cls,value):   #限定对象和上一行限定字段的value值
        assert value.isalpha(),'name must be alpha'
        return value


class Data(BaseModel):
    data:List[User]


@app.post('/user',tags=['请求体数据'])
async def user_data(user:User):
    print(user,type(user))
    print(user.name,user.birth)
    print(user.model_dump())
    return user

@app.post('/data',tags=['请求体数据'])
async def user_data(data:Data):
    return data





@app.post('/regin',tags=['注册'])
async def reg(name:str=Form(),password:str=Form()):    #与前面的请求名字对应
    print(f'username:{name},password={password}')
    #注册，实现数据库的添加操作
    return {
        'username':name
    }





@app.post('/file',tags=['文件传输'])
async def get_file(file:bytes=File()):   
    #适合小文件上传，直接到用户内存了
    return {
        'file':len(file)
    }

@app.post('/files',tags=['文件传输'])
async def get_file(files:List[bytes]=File()):   
    #适合小文件上传，直接到用户内存了
    for file in files:
        print(len(file))
    return {
        'files':len(files)  #上传了多少个文件
    }



@app.post('/Upload_file',tags=['文件传输'])
async def upload_file(file:UploadFile):   
    print('file',file)
    #文件保存
    path=os.path.join('imgs',file.filename)
    with open(path,'wb') as f:
        for line in file.file:
            f.write(line)

    return {
        'file':file.filename
    }

#上传保存多个文件
@app.post('/Upload_files',tags=['文件传输'])
async def upload_files(files:List[UploadFile]):   
    
    return {
        'names':[file.filename for file in files]
    }



if __name__== '__main__':
    uvicorn.run('fastapi_quickstart:app',port=8080,reload=True)