from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import the router from controllers (kept minimal)
from app.controllers.inference_controller import router as inference_router

app = FastAPI(title="Inference API")

# Basic CORS — adjust origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inference_router)


@app.get("/")
def read_root():
    return {"message": "Inference API is up"}
    