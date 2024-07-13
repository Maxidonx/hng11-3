# Messaging Application Development

This document outlines the development process of a messaging application, focusing on the integration of asynchronous task processing with Celery, a web framework using Flask, and the utilization of external services like ngrok for tunneling and RabbitMQ for message queuing.

## Overview

The messaging application is designed to facilitate the sending and receiving of messages asynchronously. It employs Celery for managing background tasks efficiently, ensuring high availability and responsiveness. The application also features a web interface built with Flask, enabling users to interact with the messaging system seamlessly.

## Technologies Utilized

- **Python**: As the core programming language for the application.
- **Flask**: A lightweight web framework for constructing the web interface.
- **Celery**: An asynchronous task queue/job queue based on distributed message passing, enhancing the application's efficiency.
- **RabbitMQ**: An open-source message broker that mediates communication between message producers and consumers.
- **ngrok**: A tool for creating secure tunnels to localhost, facilitating remote access to the local server.
- **nginx**: A tool used to serve my application on the localhost at port 5000
- **SMTP**

## Setup and Configuration
### Python installation
- **installation**: Followed the standard procedure to install Python on the system. [follow this link](https://www.python.org/downloads/)
- **ensure that python is set to the right part**
### flask instalation
```
pip install flask
```
### RabbitMQ Installation and Configuration

- **Installation**: Followed the standard procedure to install RabbitMQ on the system.
[follow this link](https://www.rabbitmq.com/docs)
- **Configuration**: Configured RabbitMQ to serve as the message broker for Celery, ensuring efficient task management.
```
sudo systemctl status rabbitmg-server
```
```
sudo rabbitmq-plugins list'''this enabbles you to see all rabbitmq plugings'''
```
```
sudo rabbitmq-plugins enable rabbitmq_management
```
```
sudo service rabbitmq-server start
```
***Rabbitmg will run on local host at port 15672***: Username and Password are: ```guest```

### Celery Integration

- **Setup**: Integrated Celery within the Flask application, adhering to best practices for asynchronous task execution.
```
pip install celery 
```
- **Configuration**: Configured Celery to utilize RabbitMQ as its message broker, optimizing the flow of tasks.
```
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = Celery('flask_app', broker='pyamqp://guest@localhost//', backend='rpc://')
```

### ngrok Usage

- **Installation**: Installed ngrok to enable secure remote access to the local server.
[follow this link](https://ngrok.com/download)
- **signin** sign in to ngrok and retive authtoken and authenticate with it
```
ngrok config add-authtoken <token>
```
- **Usage**: Leveraged ngrok to expose the Flask application to the internet securely, facilitating testing and deployment.

### niginx Installation and configuration
```
sudo apt install nginx
```
- **create an nginx.conf**: to alloe nginx to serve the flask app.

### SMTP configuration
- Go to any email service you use
- create an app and unique password
- use these credentials for the SMTP setup in the mail.py file
```
import smtplib
def send_mail(email):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(getenv('EMAIL_USERNAME'), getenv('EMAIL_PASSWORD'))
```

## General usage
- clone this repository
- ```python -m venv venv```
- ```pip install python-dotenv```
- creat a .env file to store you password and email
- ```pip install flask celery```
- open a second terminal run this command in the first terminal
- ```celery -A flask_app.celery worker --loglevel=info```
- in the second terminal run this
- ```python flask_app.py```
- open a third terminal run the ngrok 
- ```ngrok http 5000```
***Ensure your rabbit server stays up.***
- copy the link on the ngrok terminal and expose https to the browser
- configure nginx
- ```sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/```
- ```sudo systemctl restart nginx```

## How to test
on the brrowser,
```curl "https://<ngrok http:5000>/?talktome"```
```curl "https://<ngrok http:5000>/?sendmail=email@example.com"```



## Application Functionality

The application comprises several key components:

- **Web Interface**: Developed using Flask, offering a user-friendly interface for sending messages.
- **Background Processing**: Critical tasks, such as sending emails, are executed asynchronously by Celery workers, maintaining application responsiveness.
- **Message Queuing**: User-generated messages are temporarily stored in RabbitMQ until they can be processed by available Celery workers.
- **Asynchronous Task Execution**: Celery handles tasks asynchronously, significantly enhancing the application's performance and scalability.

## Conclusion

This document provides a comprehensive overview of the technologies and methodologies employed in the development of a scalable messaging application. By harnessing the power of Celery for asynchronous task processing and integrating RabbitMQ for effective message queuing, the application ensures efficient operation while delivering a superior user experience through its Flask-based web interface.