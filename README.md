# Fake News Detector
by Niyazi Garagashli for LSML2 course of HSE.

## Overview

This project aims to provide a simple interface for fake news detection. It is based on [DistilBERT](https://huggingface.co/transformers/model_doc/distilbert.html#distilbertforsequenceclassification) model, that has been fine-tuned on [Kaggle's Fake news dataset](https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset). <br>
**Only articles in English language are accepted!**

## Requirements 

Please view <code>requirements.txt</code> for a full list of dependencies. <br>
**Note:** if you intend to run this application in a stand-alone environment (and not through Docker), PyTorch installation and MySQL DB are required.

## Installation

You can download this repo on your local machine in whichever manner suits you best:
* git clone
* wget
* manual download

### Docker Build
This method will require you to manually install and configure MySQL database. <br> 
Use db_setup.py file for general guidance. Other files might require tuning too. <br>
<code>docker build .</code> within the project directory will build the application.

### Docker Compose
This method will pull MySQL database for you and run all necessary post-installation scripts. <br>
This is a **recommended** method, as it will provide you with a fully functional application. <br>
Only tuning you might need is to specify particular locations for database persistent files. <br>
<code>docker-compose up</code>

### Manual stand-alone installation
The application itself can be used in standalone mode, provided all the requirements are satisfied. <br>
<code>uvicorn main:app --reload</code>

## Usage
This application is built using FastAPI. It provides fast asynchronous endpoints to obtain predictions over given news articles. <br>
FastAPI provides out-of-the-box endpoint <code>/docs/</code>, that shows all available endpoints with short description of each. <br>

### Functional Endpoints
#### / (main page)
The main page of the application provides simple html-based interface to feed news article information into the predictive model.
From any given news article, provided that it has a title and a body of text, copy and paste relevant parts into the relevant forms of the main page, then click "Check this news!".
#### /check (prediction retrieval page)
After submitting news article to the application, it will redirect you to this endpoint where final prediction of the model will be displayed
#### /history (prediction history API)
This endpoint retrieves history of submitted articles along with predictions for them by the model in a JSON-like format. This can be useful when additional fine-tuning is required. Obviously, in that case labeling would need to be re-done manually to ensure better results. <br>
History can also be used in other data analytical task that are beyond the scope of this project.
#### /logs (deployment log file)
During the container deployment, automated tests are run. The results of these tests can be obtained through this endpoint. It is paramount for the application to work correctly that all tests are passed.

## Model details

### Model
Base model is [DistilBERT](https://huggingface.co/transformers/model_doc/distilbert.html#distilbertforsequenceclassification) that has been fine-tuned for a specific task of fake news classification. <br>
Model training procedure and all relevant information is available at <code>model_training.ipynb</code> notebook.

### Model metrics
Accuracy was chosen as a metric for the particular task. Since the task at hand is, in essence, binary classification and the distribution of classes is balanced enough, accuracy is unbiased and appropriate metric.

### Model Accuracy
Fine-tuned model achieved accuracy of 99.997% on withheld test dataset.

## Architecture Defence
Answers to possible questions on why certain decisions were made.

#### Why FastAPI (and not Flask, for example)?
FastAPI is at least 10 times faster than Flask, according to some benchmarks. It also provides a better out-of-the-box support for asynchronous programming. <br>
In other words, it does not require additional modules like Celery to serve requests asynchronously. <br>
Author is also more familiar with this particular module.

#### Why MySQL?
For no particular reason. MySQL is fast and light-weight enough. And this project does not require additional power that some other RDBMS like PostgreSQL provide. <br>
Simple SQLite would work as well, but there are no official Docker image I could find for it, - and composing several containers within one project is one of the stated goals.

#### Why DistilBERT?
Most transformer NLP model would most likely work without any issues. However, DistilBERT is lighter (as it is initially trained on distilled BERT dataset, hence the name) and, therefore, faster to train.
No other models were considered, because DistilBERT showed almost perfect accuracy during fine-tuning stage.

#### Why Fake News?
Well, why not? Problem statement for the project included dataset selection, and that dataset should be big enough. While it is a pretty vague description, in my opinion, Fake News dataset satisfied this criteria. <br>
And it allows for a fun project, that can still be done within given time constraints. 