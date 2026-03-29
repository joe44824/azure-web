from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

from services.file_service import save_uploaded_file, list_uploaded_files, format_size

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Helper: map statuses (you can extend this later)
def classify_status(filename: str) -> str:
    # For now, assume all saved files are "uploaded".
    # With DB or logs, you can return "processing", "failed", etc.
    return "uploaded"


@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload")
async def handle_upload(files: List[UploadFile] = File(...)):
    for file in files:
        if not file.filename:
            raise HTTPException(status_code=400, detail="File has no name")
        save_uploaded_file(file)
    return RedirectResponse("/", status_code=303)


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    raw_files = list_uploaded_files()
    history = []

    for filename, size, mtime in raw_files:
        history.append({
            "filename": filename,
            "uploaded_at": mtime.strftime("%H:%M"),
            "size": format_size(size),
            "status": classify_status(filename),  # can be augmented later
        })

    # Sort newest first
    history.sort(key=lambda x: x["filename"], reverse=True)

    return templates.TemplateResponse(
        "history.html",
        {"request": request, "history": history}
    )