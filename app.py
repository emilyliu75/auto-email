from flask import Flask, request, render_template, Response
from functools import wraps
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file variables into environment

app = Flask(__name__)

def check_auth(username, password):
    # Use environment variables for credentials
    return (
        username == os.environ.get('BASIC_USER')
        and password == os.environ.get('BASIC_PASS')
    )

def authenticate():
    resp = Response(
        'Could not verify your access level.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print('requires_auth triggered on Railway')
        auth = request.authorization
        print('Auth info:', auth)
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('subscribe.html')


@app.route('/subscribe', methods=['POST'])
@requires_auth
def subscribe():
    firstname = request.form['firstname']
    email = request.form['email']
    service = request.form['service']

    sender = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS')

    message = MIMEText(f"Hello {firstname},\n\nThank you for your query regarding {service}. subscribing to our newsletter!")
    message['Subject'] = "Subscription Confirmed"
    message['From'] = sender
    message['To'] = email
    print(firstname, email, sender, password)  # Debugging output
    try:
        with smtplib.SMTP('smtp-relay.brevo.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender, password)
            smtp.sendmail(sender, email, message.as_string())
        return "Thank you for subscribing! Check your email."
    except Exception as e:
        return f"Failed to send email: {e}"

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8000)
