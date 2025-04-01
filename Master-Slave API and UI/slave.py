from fastapi import FastAPI
import subprocess
import json
from fastapi.responses import HTMLResponse

app = FastAPI()

# Store report globally
report_data = None  

@app.post("/scan")
async def scan():
    """Runs the audit script (audit.py) and stores the JSON output."""
    global report_data
    try:
        # Run security audit script
        result = subprocess.run(["python", "audit.py"], capture_output=True, text=True)
        
        # Check if script executed successfully
        if result.returncode != 0:
            return {"status": "error", "message": f"Script execution failed: {result.stderr}"}
        
        # Ensure output is valid JSON
        try:
            report_data = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON format from audit script"}

        return {"status": "success", "report": report_data}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def convert_json_to_html(data):
    """Recursively converts JSON data into an HTML table."""
    if isinstance(data, dict):
        return "".join(
            f"<tr><td>{key}</td><td>{convert_json_to_html(value)}</td></tr>"
            for key, value in data.items()
        )
    elif isinstance(data, list):
        return "<ul>" + "".join(f"<li>{convert_json_to_html(item)}</li>" for item in data) + "</ul>"
    else:
        return str(data)  # Convert basic types to string

@app.get("/report", response_class=HTMLResponse)
async def get_report():
    """Generates an HTML report from JSON data."""
    global report_data
    if not report_data:
        return HTMLResponse(content="<h1>No report available</h1>", status_code=404)

    # Convert JSON to formatted HTML
    html_table = convert_json_to_html(report_data)

    html_content = f"""
    <html>
    <head>
        <title>Audit Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
            h1 {{ text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background: #007bff; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Audit Report</h1>
            <table>
                <tr><th>Check</th><th>Status</th></tr>
                {html_table}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
