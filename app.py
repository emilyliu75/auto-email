from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file variables into environment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('subscribe.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    firstname = request.form['firstname']
    email = request.form['email']

    sender = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS')

    message = MIMEText(f"Hello {firstname},\n\nThank you for subscribing to our newsletter!")
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
