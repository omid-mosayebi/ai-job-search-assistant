from fastapi import FastAPI

app = FastAPI(title="AI Job Search Assistant")


@app.get("/")
def root():
    return {
        "message": "Backend is running"
    }
