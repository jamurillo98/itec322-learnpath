from fastapi import FastAPI


app = FastAPI()


@app.get("/api/recommend")
def recommend():
    return {"message": "Backend is running", "recommendations": []}
