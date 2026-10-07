from fastapi import FastAPI

app = FastAPI(title = "Pulsewatch")




@app.get("/health")
def health():
    return{"status": "ok"}