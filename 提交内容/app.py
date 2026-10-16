from fastapi import FastAPI, Form
import uvicorn
from pydantic import BaseModel, Field, field_validator


app=FastAPI()

@app.get('/home')
async def home():
    return{
        'message':'ML API function normally'
    }


#class Data(BaseModel):
    Data_A:int=Field(default=0)
    Operation:str = 'sum'
    Data_B:int=Field(default=0)



@app.post("/form_test")
async def form_test(
    Data_A: int = Form(),
    Operation: str = Form(),
    Data_B: int = Form()
):
    if Operation == "sum":
        result = Data_A + Data_B
    elif Operation == "subtract":
        result = Data_A - Data_B
    elif Operation == "multiply":
        result = Data_A * Data_B
    elif Operation == "divide":
        if Data_B == 0:
            raise ValueError("除数不能为零")
        return Data_A / Data_B
    return {"Result": result}





if __name__=='__main__':
    uvicorn.run('app:app',port=8000,reload=True)