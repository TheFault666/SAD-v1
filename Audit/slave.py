# # # from fastapi import FastAPI
# # # import subprocess
# # # import json
# # # from fastapi.responses import HTMLResponse

# # # app = FastAPI()

# # # # Store report globally
# # # report_data = None  

# # # @app.post("/scan")
# # # async def scan():
# # #     """Runs the audit script (audit.py) and stores the JSON output."""
# # #     global report_data
# # #     try:
# # #         # Run security audit script
# # #         result = subprocess.run(["python", "audit.py"], capture_output=True, text=True)
        
# # #         # Check if script executed successfully
# # #         if result.returncode != 0:
# # #             return {"status": "error", "message": f"Script execution failed: {result.stderr}"}
        
# # #         # Ensure output is valid JSON
# # #         try:
# # #             report_data = json.loads(result.stdout.strip())
# # #         except json.JSONDecodeError:
# # #             return {"status": "error", "message": "Invalid JSON format from audit script"}

# # #         return {"status": "success", "report": report_data}

# # #     except Exception as e:
# # #         return {"status": "error", "message": str(e)}

# # # def convert_json_to_html(data):
# # #     """Recursively converts JSON data into an HTML table."""
# # #     if isinstance(data, dict):
# # #         return "".join(
# # #             f"<tr><td>{key}</td><td>{convert_json_to_html(value)}</td></tr>"
# # #             for key, value in data.items()
# # #         )
# # #     elif isinstance(data, list):
# # #         return "<ul>" + "".join(f"<li>{convert_json_to_html(item)}</li>" for item in data) + "</ul>"
# # #     else:
# # #         return str(data)  # Convert basic types to string

# # # @app.get("/report", response_class=HTMLResponse)
# # # async def get_report():
# # #     """Generates an HTML report from JSON data."""
# # #     global report_data
# # #     if not report_data:
# # #         return HTMLResponse(content="<h1>No report available</h1>", status_code=404)

# # #     # Convert JSON to formatted HTML
# # #     html_table = convert_json_to_html(report_data)

# # #     html_content = f"""
# # #     <html>
# # #     <head>
# # #         <title>Audit Report</title>
# # #         <style>
# # #             body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
# # #             .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
# # #             h1 {{ text-align: center; }}
# # #             table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
# # #             th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
# # #             th {{ background: #007bff; color: white; }}
# # #         </style>
# # #     </head>
# # #     <body>
# # #         <div class="container">
# # #             <h1>Audit Report</h1>
# # #             <table>
# # #                 <tr><th>Check</th><th>Status</th></tr>
# # #                 {html_table}
# # #             </table>
# # #         </div>
# # #     </body>
# # #     </html>
# # #     """

# # #     return HTMLResponse(content=html_content)

# # # if __name__ == "__main__":
# # #     import uvicorn
# # #     uvicorn.run(app, host="127.0.0.1", port=8001)
# # from fastapi import FastAPI
# # import subprocess
# # import json
# # from fastapi.responses import HTMLResponse
# # import uvicorn

# # app = FastAPI()

# # # Store report globally
# # report_data = None  

# # @app.post("/scan")
# # async def scan():
# #     """Runs the security audit and stores the JSON output."""
# #     global report_data
# #     try:
# #         # Run security audit script
# #         result = subprocess.run(["python", "audit.py"], capture_output=True, text=True)

# #         # Check if script executed successfully
# #         if result.returncode != 0:
# #             return {"status": "error", "message": f"Script execution failed: {result.stderr}"}
        
# #         # Ensure output is valid JSON
# #         try:
# #             report_data = json.loads(result.stdout.strip())
# #         except json.JSONDecodeError:
# #             return {"status": "error", "message": "Invalid JSON format from audit script"}

# #         return {"status": "success", "report": report_data}

# #     except Exception as e:
# #         return {"status": "error", "message": str(e)}

# # def convert_json_to_html(data):
# #     """Recursively converts JSON data into an HTML table format."""
# #     if isinstance(data, dict):
# #         return "".join(
# #             f"<tr><td>{key}</td><td>{convert_json_to_html(value)}</td></tr>"
# #             for key, value in data.items()
# #         )
# #     elif isinstance(data, list):
# #         return "<ul>" + "".join(f"<li>{convert_json_to_html(item)}</li>" for item in data) + "</ul>"
# #     else:
# #         return str(data)  

# # @app.get("/report", response_class=HTMLResponse)
# # async def get_report():
# #     """Generates an HTML report from stored JSON data."""
# #     global report_data
# #     if not report_data:
# #         return HTMLResponse(content="<h1>No report available</h1>", status_code=404)

# #     # Convert JSON to formatted HTML
# #     html_table = convert_json_to_html(report_data)

# #     html_content = f"""
# #     <html>
# #     <head>
# #         <title>Audit Report</title>
# #         <style>
# #             body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
# #             .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
# #             h1 {{ text-align: center; }}
# #             table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
# #             th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
# #             th {{ background: #007bff; color: white; }}
# #         </style>
# #     </head>
# #     <body>
# #         <div class="container">
# #             <h1>Audit Report</h1>
# #             <table>
# #                 <tr><th>Check</th><th>Status</th></tr>
# #                 {html_table}
# #             </table>
# #         </div>
# #     </body>
# #     </html>
# #     """

# #     return HTMLResponse(content=html_content)

# # if __name__ == "__main__":
# #     uvicorn.run(app, host="127.0.0.1", port=8001)
# from fastapi import FastAPI
# import subprocess
# import json
# from fastapi.responses import FileResponse, JSONResponse
# from fpdf import FPDF

# app = FastAPI()

# # Store report globally 
# report_data = {}  # Global variable to store the latest audit data

# def generate_pdf_report(json_data, output_filename="security_audit_report.pdf"):
#     """Generates a PDF security audit report from JSON data."""
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
    
#     # Title
#     pdf.set_font("Arial", style='B', size=16)
#     pdf.cell(200, 10, "Security Audit Report", ln=True, align='C')
#     pdf.ln(10)

#     pdf.set_font("Arial", size=12)
    
#     def add_section(title):
#         """Adds a section title in the PDF."""
#         pdf.set_font("Arial", style='B', size=14)
#         pdf.cell(0, 10, title, ln=True)
#         pdf.set_font("Arial", size=12)
#         pdf.ln(5)
    
#     def add_text(label, text):
#         """Adds key-value pair data to the PDF."""
#         pdf.set_font("Arial", style='B', size=12)
#         pdf.cell(0, 8, label, ln=True)
#         pdf.set_font("Arial", size=12)
#         pdf.multi_cell(0, 8, text)
#         pdf.ln(3)
    
#     def add_table(headers, data):
#         """Creates a table for installed software list."""
#         pdf.set_fill_color(200, 200, 200)
#         pdf.set_font("Arial", style='B', size=12)
        
#         col_widths = [80, 40, 50]  # Adjust width as needed
        
#         # Print headers
#         for i, header in enumerate(headers):
#             pdf.cell(col_widths[i], 8, header, border=1, fill=True)
#         pdf.ln()
        
#         # Print rows
#         pdf.set_font("Arial", size=12)
#         for row in data:
#             pdf.cell(col_widths[0], 8, row.get("DisplayName", "Unknown"), border=1)
#             pdf.cell(col_widths[1], 8, row.get("DisplayVersion", "-"), border=1)
#             pdf.cell(col_widths[2], 8, row.get("Publisher", "-"), border=1)
#             pdf.ln()
#         pdf.ln(5)
    
#     for section, content in json_data.items():
#         add_section(section)
        
#         if isinstance(content, dict):
#             for key, value in content.items():
#                 add_text(key, str(value))
#         elif isinstance(content, list):
#             if section == "Installed Software":
#                 headers = ["Software Name", "Version", "Publisher"]
#                 add_table(headers, content)
#             else:
#                 for item in content:
#                     add_text("-", str(item))
#         else:
#             add_text("Details", str(content))
    
#     pdf.output(output_filename)

# @app.post("/scan")
# async def scan():
#     """Runs the audit script (audit.py) and stores the JSON output."""
#     global report_data
#     try:
#         # Run security audit script
#         result = subprocess.run(["python", "audit.py"], capture_output=True, text=True)
        
#         # Check if script executed successfully
#         if result.returncode != 0:
#             return {"status": "error", "message": f"Script execution failed: {result.stderr}"}
        
#         # Ensure output is valid JSON
#         try:
#             report_data = json.loads(result.stdout.strip())
#         except json.JSONDecodeError:
#             return {"status": "error", "message": "Invalid JSON format from audit script"}

#         return {"status": "success", "report": report_data}

#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# @app.get("/report/json", response_class=JSONResponse)
# async def get_report_json():
#     """Returns the audit report in JSON format."""
#     global report_data
#     if not report_data:
#         return JSONResponse(content={"status": "error", "message": "No report available"}, status_code=404)
#     return JSONResponse(content=report_data)

# def generate_pdf(data):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", style='B', size=16)
#     pdf.cell(200, 10, "Security Audit Report", ln=True, align='C')
#     pdf.ln(10)
#     pdf.set_font("Arial", size=12)
    
#     def add_data(data, indent=0):
#         if isinstance(data, dict):
#             for key, value in data.items():
#                 pdf.cell(0, 10, f"{' ' * indent}{key}: {value if not isinstance(value, (dict, list)) else ''}", ln=True)
#                 add_data(value, indent + 2)
#         elif isinstance(data, list):
#             for item in data:
#                 add_data(item, indent + 2)
#         else:
#             pdf.cell(0, 10, f"{' ' * indent}{data}", ln=True)
    
#     add_data(data)
    
#     pdf_file = "audit_report.pdf"
#     pdf.output(pdf_file)
#     return pdf_file

# @app.get("/report/pdf")
# async def get_report_pdf():
#     """Returns the audit report as a downloadable PDF file."""
#     global report_data
#     if not report_data:
#         return JSONResponse(content={"status": "error", "message": "No report available"}, status_code=404)
    
#     output_filename = "security_audit_report.pdf"
#     generate_pdf_report(report_data, output_filename)

#     return FileResponse(output_filename, media_type="application/pdf", filename=output_filename)
# @app.post("/report/update")
# async def update_report(data: dict):
#     """Updates the global audit report data."""
#     global report_data
#     report_data = data
#     return {"status": "success", "message": "Report data updated"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8001)
from fastapi import FastAPI
import subprocess
import json
from fastapi.responses import FileResponse, JSONResponse
from fpdf import FPDF

app = FastAPI()

# Store report globally 
report_data = {}  # Global variable to store the latest audit data

def generate_pdf_report(json_data, output_filename="security_audit_report.pdf"):
    """Generates a PDF security audit report from JSON data."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Security Audit Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    
    def add_section(title):
        """Adds a section title in the PDF."""
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", size=12)
        pdf.ln(5)
    
    def add_text(label, text):
        """Adds key-value pair data to the PDF."""
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 8, label, ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, str(text))  # Ensure text is converted to a string
        pdf.ln(3)
    
    def add_table(headers, data):
        """Creates a table for installed software list."""
        pdf.set_fill_color(200, 200, 200)
        pdf.set_font("Arial", style='B', size=12)
        
        col_widths = [80, 40, 50]  # Adjust width as needed
        
        # Print headers
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 8, header, border=1, fill=True)
        pdf.ln()
        
        # Print rows
        pdf.set_font("Arial", size=12)
        for row in data:
            pdf.cell(col_widths[0], 8, str(row.get("DisplayName", "Unknown")), border=1)
            pdf.cell(col_widths[1], 8, str(row.get("DisplayVersion", "-")), border=1)
            pdf.cell(col_widths[2], 8, str(row.get("Publisher", "-")), border=1)
            pdf.ln()
        pdf.ln(5)
    
    for section, content in json_data.items():
        add_section(section)
        
        if isinstance(content, dict):
            for key, value in content.items():
                add_text(key, value)
        elif isinstance(content, list):
            if section == "Installed Software":
                headers = ["Software Name", "Version", "Publisher"]
                add_table(headers, content)
            else:
                for item in content:
                    add_text("-", item)
        else:
            add_text("Details", content)
    
    pdf.output(output_filename)

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

@app.get("/report/json", response_class=JSONResponse)
async def get_report_json():
    """Returns the audit report in JSON format."""
    global report_data
    if not report_data:
        return JSONResponse(content={"status": "error", "message": "No report available"}, status_code=404)
    return JSONResponse(content=report_data)

@app.get("/report/pdf")
async def get_report_pdf():
    """Returns the audit report as a downloadable PDF file."""
    global report_data
    if not report_data:
        return JSONResponse(content={"status": "error", "message": "No report available"}, status_code=404)
    
    output_filename = "security_audit_report.pdf"
    generate_pdf_report(report_data, output_filename)

    return FileResponse(output_filename, media_type="application/pdf", filename=output_filename)

@app.post("/report/update")
async def update_report(data: dict):
    """Updates the global audit report data."""
    global report_data
    report_data = data
    return {"status": "success", "message": "Report data updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
