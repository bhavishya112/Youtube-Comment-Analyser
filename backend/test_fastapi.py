from fastapi import FastAPI

app = FastAPI()

@app.post("/getmedata")
def get_data():
    return {"name":"bhavishya","age":20}