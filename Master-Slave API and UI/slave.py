from fastapi import FastAPI
import subprocess
import json

app = FastAPI()

@app.post("/scan")
async def scan():
    try:
        # Replace "audit_script.py" with the actual script path
        result = subprocess.run(["python", "audit.py"], capture_output=True, text=True)
        return {"status": "success", "report": result.stdout}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)  # Slave runs on port 8001
