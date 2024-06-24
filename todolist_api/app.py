from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def readRoot() -> dict:
    return {"message": "Hello World!"}
