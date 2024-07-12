from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from auth.authentication import authenticate_user  # type: ignore

app = FastAPI()

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if user:
        response = RedirectResponse(url="/content", status_code=302)
        # Adicione um cookie ou sessão para identificar o usuário logado
        response.set_cookie(key="session_token", value="your_session_token")
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Login ou senha inválidos."})

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("session_token")
    # Se estiver usando sessões, remova a sessão aqui
    return response

@app.get("/content", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse("content.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
