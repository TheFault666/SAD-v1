from fastapi import FastAPI
import subprocess
import json

app = FastAPI()

@app.post("/scan")
async def scan():
    try:
        result = subprocess.run(["python", "audit.py"], capture_output=True, text=True)
        report_data = result.stdout.strip()

        # Debugging: Print raw output from audit.py
        print("Raw audit.py output:", report_data)

        # Convert audit.py output to JSON
        try:
            parsed_data = json.loads(report_data)
            return {"status": "success", "report": parsed_data}
        except json.JSONDecodeError:
            return {"status": "error", "message": f"Invalid JSON received from audit.py: {report_data}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)  # Slave runs on port 8001
