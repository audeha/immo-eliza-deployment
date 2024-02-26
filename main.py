from fastapi import FastAPI

'''from pydantic import BaseModel
from predict import predict

import sys
sys.path.append('../immo-eliza-ml')

class User_input(BaseModel):
    operat'''

app = FastAPI()

@app.get('/')
def index():
    return {'data':'This API is working fine'}
