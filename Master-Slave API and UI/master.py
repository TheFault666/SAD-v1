from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import httpx
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Move CORS middleware setup here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend files from the "static" directory
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# List of slave nodes
SLAVE_NODES = ["http://127.0.0.1:8001"]  # Adjust if testing multiple slaves

# Pydantic model for request validation
class ScanRequest(BaseModel):
    target: str

@app.get("/get_targets")
async def get_targets():
    return SLAVE_NODES

@app.post("/run_scan/")
async def run_scan(request: ScanRequest): #Triggers a security scan on the selected slave machine.
    target = request.target
    
    if target not in SLAVE_NODES:
        raise HTTPException(status_code=400, detail="Invalid target node")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{target}/scan")
            response.raise_for_status()  # Raise error if response is not 200
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Master runs on port 8000
