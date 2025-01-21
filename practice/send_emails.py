from email.message import EmailMessage
import ssl
import smtplib  # smtps are the servers like gmail,yahoo etc
from flask import Flask, request, jsonify
app = Flask(__name__)

sender = 'saramsaeed22@gmail.com'
password = "ynoo emye cfog zdlz"  # app password


class Emails:
    # methods within a class that have no access to anything else in the class (no self keyword or cls keyword)
    @staticmethod  # They can be thought of as a special kind of function that sits inside of the class.
    def sending_email(data, files):
        receiver = data['receiver']
        subject = data['subject']
        body = data['body']

        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['subject'] = subject
        em.set_content(body)
        # ssl for keeping an internet connection secure
        # this is important in case if you are sending with some important data
        context = ssl.create_default_context()

        for file in files:
            file_name = file.filename
            file_data = file.read()
            em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, receiver, em.as_string())
                return {"Response": "Email has been sent"}, 200
        except smtplib.SMTPException as e:
            return {"Error": str(e)}, 400


emails = Emails()


@app.route('/send', methods=['POST'])
def send():
    data = {
        'receiver': request.form['receiver'],
        'subject': request.form['subject'],
        'body': request.form['body']
    }
    files = request.files.getlist('attachments')
    response, status_code = emails.sending_email(data, files)
    return jsonify(response), status_code


if __name__ == "__main__":
    app.run(debug=True)

