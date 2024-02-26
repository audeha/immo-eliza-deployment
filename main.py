from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data':'This API is working fine'}
