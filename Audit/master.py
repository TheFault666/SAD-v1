# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# import httpx
# from pydantic import BaseModel

# # Initialize FastAPI app
# app = FastAPI()

# # CORS Middleware (Allow requests from frontend)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Serve frontend files (optional)
# app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# # List of slave nodes
# SLAVE_NODES = ["http://127.0.0.1:8001"]  # You can add more nodes if needed

# # Pydantic model for request validation
# class ScanRequest(BaseModel):
#     target: str

# @app.get("/get_targets")
# async def get_targets():
#     """Returns available slave nodes for scanning."""
#     return {"available_nodes": SLAVE_NODES}

# @app.post("/run_scan/")
# async def run_scan(request: ScanRequest):
#     """Triggers a security scan on the selected slave machine."""
#     target = request.target

#     if target not in SLAVE_NODES:
#         raise HTTPException(status_code=400, detail="Invalid target node")

#     # async with httpx.AsyncClient() as client:
#     #     try:
#     #         print(f"[*] Sending scan request to {target}/scan...")
#     #         response = await client.post(f"{target}/scan")
#     #         response.raise_for_status()  # Raise error if response is not 200

#     #         try:
#     #             data = response.json()
#     #             print(f"[+] Received response from {target}: {data}")
#     #             return data
#     #         except ValueError:
#     #             print("[!] Received invalid JSON from slave.")
#     #             raise HTTPException(status_code=500, detail="Invalid JSON response from slave.")

#     #     except httpx.HTTPError as e:
#     #         print(f"[!] Scan request failed: {str(e)}")
#     #         raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")
#     async with httpx.AsyncClient() as client:
#         try:
#             print(f"[*] Sending scan request to {target}/scan...")
#             response = await client.post(f"{target}/scan")
#             print("[+] Raw Response:", response.text)  # Debugging step to check raw response

#             # Raise an error if the status code is not 200
#             response.raise_for_status()  # <-- This may be throwing the 500 error

#             # Ensure the response is not empty
#             if not response.text.strip():
#                 print("[!] Error: Empty response from slave.")
#                 raise HTTPException(status_code=500, detail="Slave returned empty response")

#             try:
#                 data = response.json()
#                 print(f"[+] Received response from {target}: {data}")
#                 return data
#             except ValueError:
#                 print("[!] Error: Received invalid JSON from slave.")
#                 raise HTTPException(status_code=500, detail="Invalid JSON response from slave.")

#         except httpx.HTTPError as e:
#             print(f"[!] Scan request failed: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")
#         except Exception as e:
#             print(f"[!] Unexpected error: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

        
# @app.get("/fetch_report/")
# async def fetch_report(target: str):
#     """Fetches the latest report from the selected slave."""
#     if target not in SLAVE_NODES:
#         raise HTTPException(status_code=400, detail="Invalid target node")

#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(f"{target}/report", timeout=10)
#             response.raise_for_status()
#             return response.text  # Return raw HTML report

#         except httpx.HTTPError as e:
#             raise HTTPException(status_code=500, detail=f"Failed to fetch report: {str(e)}")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)  # Master runs on port 8000
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import httpx
from pydantic import BaseModel
import os

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware (Allow requests from frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend files (optional)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# List of slave nodes
SLAVE_NODES = ["http://127.0.0.1:8001"]  # You can add more nodes if needed

# Pydantic model for request validation
class ScanRequest(BaseModel):
    target: str

@app.get("/get_targets")
async def get_targets():
    """Returns available slave nodes for scanning."""
    return {"available_nodes": SLAVE_NODES}

@app.post("/run_scan/")
async def run_scan(request: ScanRequest):
    """Triggers a security scan on the selected slave machine."""
    target = request.target

    if target not in SLAVE_NODES:
        raise HTTPException(status_code=400, detail="Invalid target node")

    async with httpx.AsyncClient() as client:
        try:
            print(f"[*] Sending scan request to {target}/scan...")
            response = await client.post(f"{target}/scan", timeout=15)
            
            print("[+] Raw Response:", response.text)  # Debugging log
            response.raise_for_status()  # Ensure we got a valid response

            # Ensure response is not empty
            if not response.text.strip():
                print("[!] Error: Empty response from slave.")
                raise HTTPException(status_code=500, detail="Slave returned an empty response")

            try:
                data = response.json()
                print(f"[+] Received response from {target}: {data}")
                return data
            except ValueError:
                print("[!] Error: Invalid JSON response from slave.")
                raise HTTPException(status_code=500, detail="Invalid JSON response from slave.")

        except httpx.RequestError as e:
            print(f"[!] HTTP Request Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Scan request failed: {str(e)}")
        except httpx.HTTPStatusError as e:
            print(f"[!] HTTP Status Error: {str(e)}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Scan request failed: {str(e)}")
        except Exception as e:
            print(f"[!] Unexpected Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/fetch_report/")
async def fetch_report(target: str):
    """Fetches the latest PDF report from the selected slave."""
    if target not in SLAVE_NODES:
        raise HTTPException(status_code=400, detail="Invalid target node")

    pdf_filename = "fetched_report.pdf"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{target}/report/pdf", timeout=20)
            response.raise_for_status()

            # Save the PDF locally
            with open(pdf_filename, "wb") as pdf_file:
                pdf_file.write(response.content)

            print(f"[+] Report fetched successfully from {target}")
            return FileResponse(pdf_filename, media_type="application/pdf", filename="security_audit_report.pdf")

        except httpx.RequestError as e:
            print(f"[!] Failed to fetch report: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch report: {str(e)}")
        except Exception as e:
            print(f"[!] Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Master runs on port 8000