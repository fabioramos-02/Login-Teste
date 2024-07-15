from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from auth.authentication import authenticate_user
from database import init_db
from crud import create_user, get_user_by_username, get_all_users

app = FastAPI()

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        response = RedirectResponse(url="/content", status_code=302)
        response.set_cookie(key="session_token", value="your_session_token")
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Login ou senha inválidos."})

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("session_token")
    return response

@app.get("/content", response_class=HTMLResponse)
async def content(request: Request):
    return templates.TemplateResponse("content.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    existing_user = get_user_by_username(username)
    if existing_user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuário já existe."})
    create_user(username, password)
    return RedirectResponse(url="/", status_code=302)

@app.post("/api/register")
async def api_register(username: str = Form(...), password: str = Form(...)):
    existing_user = get_user_by_username(username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe.")
    create_user(username, password)
    return {"message": "Usuário criado com sucesso"}

@app.get("/api/users")
async def list_users():
    users = get_all_users()
    return {"users": users}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
