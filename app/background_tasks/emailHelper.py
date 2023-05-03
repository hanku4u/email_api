from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import List

class EmailHelper:
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_email(self, to: List[str], subject: str, body: str):
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = ', '.join(to)
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(body, 'html'))

        try:
            # Open connection to SMTP server and login
            smtp_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp_server.starttls()
            smtp_server.login(self.email, self.password)

            # Send email and close connection
            smtp_server.sendmail(self.email, to, msg.as_string())
            smtp_server.quit()
        except smtplib.SMTPException as e:
            # Handle SMTP errors
            print(f"Error: {e}")
            raise Exception("Failed to send email")
        except Exception as e:
            # Handle other errors
            print(f"Error: {e}")
            raise Exception("Failed to send email")



    # generate an HTML email body with the specified title and message
    # does not require instace of class or any class variables so it is static
    @staticmethod 
    def generate_html_body(title: str, message: str) -> str:
        """
        Generate an HTML email body with the specified title and message.
        """
        # TODO: Add CSS styling to HTML
        # interpolate title and message into HTML template
        html = f"""
        <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <p>{message}</p>
        </body>
        </html>
        """
        return html
