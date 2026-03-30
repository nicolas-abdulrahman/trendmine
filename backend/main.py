from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def root(request: Request):
    data = await request.json()
    print("FROM FRONTEND:", data)
    return {"message": "received", "data": data}
@app.get("/")
def root_get():
    return {"message": "backend is running"}

