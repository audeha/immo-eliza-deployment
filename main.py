from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data':{'name':'Audrey'}}

@app.get('/about')
def index():
    return {'data':'About this page'}
