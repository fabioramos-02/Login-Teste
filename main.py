from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from database import add_file, retrieve_file
from datetime import datetime
import os

app = FastAPI()

# Diretório onde as imagens serão salvas
UPLOAD_DIR = Path("images")
UPLOAD_DIR.mkdir(exist_ok=True)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="templates")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    file_data = {
        "filename": file.filename,
        "upload_time": datetime.utcnow()
    }
    
    new_file = await add_file(file_data)
    return {"info": f"file '{file.filename}' saved at '{file_location}'", "file_id": new_file["id"]}

@app.get("/images/{image_id}")
async def get_image(image_id: str):
    file = await retrieve_file(image_id)
    if not file:
        raise HTTPException(status_code=404, detail="Image not found")
    
    file_location = UPLOAD_DIR / file["filename"]
    if not file_location.exists():
        raise HTTPException(status_code=404, detail="Image file not found on disk")
    
    return FileResponse(file_location)

@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
