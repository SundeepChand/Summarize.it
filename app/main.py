import uvicorn
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .summarize.generate_summary import summarize_text

app = FastAPI()


class TodoTask(BaseModel):
    id: int
    task: str
    is_over: bool


templates = Jinja2Templates(directory='app/templates')
app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.get('/', response_class=HTMLResponse)
def get_home_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'summary': ''})


@app.get('/summarize', response_class=RedirectResponse)
def redirect_to_home():
    return '/'


@app.post('/summarize', response_class=HTMLResponse)
def generate_summary(request: Request, input_text: str = Form(...)):
    summarized_text = summarize_text(input_text)
    return templates.TemplateResponse('index.html', {'request': request, 'summary': summarized_text})


if __name__ == '__main__':
    uvicorn.run(app)
