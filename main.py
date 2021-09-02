# A simple webservice to detect fake news by Niyazi Garagashli

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
import numpy as np
import base64
import mysql.connector

# Initializing FastAPI
app = FastAPI()
# Mounting static for HTML files
app.mount("/static", StaticFiles(directory="static"), name="static")
# Creating templates object
templates = Jinja2Templates(directory="templates")
# Model and tokenizer initialization
dbert = DistilBertForSequenceClassification.from_pretrained('model/model/')
dbert_token = DistilBertTokenizerFast.from_pretrained('model/tokenizer/')
# Logfile
log_path = "test.log"
# DB connection

mydb = mysql.connector.connect(
    host="mysqldb",
    user="fake_news",
    password="f@ke_n3ws",
    database="news"
)


# Application definition
async def make_prediction(title: str, text: str,
                          tokenizer: DistilBertTokenizerFast = dbert_token,
                          model: DistilBertForSequenceClassification = dbert) -> int:
    """
    Returns prediction by model given the input
    :param title: str: title of the news article
    :param text: str: body of text of the news article (max length truncated to 512)
    :param tokenizer: DistilBertTokenizerFast: tokenizer object from transformers module
    :param model: DistilBertForSequenceClassification: pre-trained model object from transformers module
    :return: int: 1 for Truth article, 0 for Fake article
    """
    full_text = title + ' ' + text
    text_enc = tokenizer(full_text, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**text_enc)
    logits = outputs[0].detach().numpy()
    pred = np.argmax(logits, axis=-1)[0]
    cursor = mydb.cursor()
    sql = "INSERT INTO news_articles (title, article_text, prediction) VALUES (%s, %s, %s)"
    val = (title[:255], text[:512], int(pred))
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()

    return pred


@app.get('/')
async def main_get(request: Request):
    """
    Renders the main page of the application
    :param request:
    :return: TemplateResponse: main page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/logs", response_class=FileResponse)
async def log():
    """
    Renders the log file, created by automated testing procedure
    :return: FileResponse: log file
    """
    return log_path


@app.post('/check')
async def main_post(request: Request, title: str = Form(...), text: str = Form(...)):
    """
    Renders the prediction of the model to the client
    :param request: Request: FastAPI object containing request from client
    :param title: str: title of the news article
    :param text: str: body of text of the news article (max length truncated to 512)
    :return: TemplateResponse: object of FastAPI module that renders the output to client
    """
    int_prediction = await make_prediction(title, text)
    if int_prediction == 1:
        prediction = "This news article seems legit!"
        with open('static/trump_happy.jpg', "rb") as image_file:
            encoded_img = base64.b64encode(image_file.read()).decode('ascii')
    else:
        prediction = "This news article seems fake!"
        with open('static/trump_sad.jpg', "rb") as image_file:
            encoded_img = base64.b64encode(image_file.read()).decode('ascii')

    return templates.TemplateResponse("results.html", {"request": request, 'Title': title,
                                                       'Prediction': prediction, 'img': encoded_img})


@app.get('/history')
async def show_history():
    """
    Returns JSON-like object of all previously checked articles in database
    :return: list of dictionaries
    """
    cursor = mydb.cursor()
    sql = "SELECT * from news_articles;"
    cursor.execute(sql)
    results = cursor.fetchall()
    response = []
    for r in results:
        mid_resp = {'title': r[0], 'text': r[1], 'verdict': r[2]}
        response.append(mid_resp)
    cursor.close()
    return response
