from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime
import os

app = FastAPI()

# Diretório onde os arquivos serão salvos
UPLOAD_DIR = Path("uploads")
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
    return {"info": f"arquivo '{file.filename}' salvo em '{file_location}'"}

@app.get("/images/{filename}")
async def get_image(filename: str):
    file_location = UPLOAD_DIR / filename
    if not file_location.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(file_location)

@app.get("/manage-uploads", response_class=HTMLResponse)
async def manage_uploads(request: Request):
    files = os.listdir(UPLOAD_DIR)
    return templates.TemplateResponse("manage_uploads.html", {"request": request, "files": files})

@app.delete("/delete-file/{filename}")
async def delete_file(filename: str):
    file_location = UPLOAD_DIR / filename
    if file_location.exists():
        file_location.unlink()
        return JSONResponse(content={"message": "File deleted successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
