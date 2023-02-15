import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import json

config_file_path = Path(__file__).parent.parent / "config.json"
with open(config_file_path, 'r') as f:
  config = json.load(f)


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, deals):
        self.deals = deals
        self.message = f""

    def get_message(self):
        for deal in self.deals:
            city = deal[0]
            price = deal[1]
            link = deal[2]
            departure = deal[3]
            return_date = deal[4]
            self.message += f"<a href='{link}'>{city}: From {departure} to {return_date} - ${price}</a><br>"
        return self.message


class EmailManager:
    def __init__(self, email_message):
        self.email_message = email_message
        self.sender_email = config["from"]
        self.receiver_email = config["receiver"]
        self.password = config["password"]
        self.smtp_port = config["smtp port"]
        self.smtp_server = config["smtp server"]

        message = MIMEMultipart("alternative")
        message["Subject"] = "Flight Deals"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        ssl_context = ssl.create_default_context()

        html = f"""\
      <html>
        <body>
          <p>
          {self.email_message}
          </p>
        </body>
      </html>
      """

        part2 = MIMEText(html, "html")
        message.attach(part2)

        with smtplib.SMTP_SSL(
            self.smtp_server, self.smtp_port, context=ssl_context
        ) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
