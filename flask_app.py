# # File: flask_app.py
import re
from flask import Flask, request, jsonify
from tasks import make_celery, send_mail_task
from datetime import datetime
import os

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = make_celery(app)

log_file_path = '/var/log/messaging_system.log'

def is_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.search(email_regex, email):
        return True
    return False

@app.route('/')
def index():
    if 'sendmail' in request.args:
        recipient = request.args.get('sendmail')
        send_mail_task.delay(recipient)
        return jsonify({'message': f"Email queued for sending to {recipient}"})
    
    if 'talktome' in request.args:
            log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Logged at\n"
            with open('/var/log/messaging_system.log', 'a') as log_file:
                log_file.write(log_message)
                return jsonify({'message': f"Logged at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}), 200

    return "Specify 'sendmail' or 'talktome' parameter."

if __name__ == '__main__':
    app.run(debug=True)

