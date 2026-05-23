from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    print("Hello, World!")
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}
