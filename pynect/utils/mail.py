import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from typing import Any, Optional
from os.path import basename


class SMTPServer:
    """ Stores the SMTP Server configuration information """

    def __init__(self, port: int, sender_email: str, password: str, name: Any):
        self.port = port
        self.sender_email = sender_email
        self.password = password
        self.name = name
        self.server = smtplib.SMTP(name, self.port)


class EmailSender:
    """
    Email Helper Class for sending emails in html format.
    It handles the SMTP server authentication.
    """

    def __init__(self, server: SMTPServer):
        self.smtp_server = server
        self.__logger = logging.getLogger(f'Email Sender {server.name}')

    def login(self):
        # Performs akthentication based on the provided SMTP Server configs
        context = ssl.create_default_context()
        server = self.smtp_server.server
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(self.smtp_server.sender_email,
                     self.smtp_server.password)
        self.__logger.debug(
            'Logged in to smtp server' +
            f'{self.smtp_server.name}:{self.smtp_server.port}'
        )

    def logout(self):
        self.smtp_server.server.quit()
        self.__logger.debug(
            'Logged out of smtp server' +
            f'{self.smtp_server.name}:{self.smtp_server.port}'
        )

    def send_html_email(
        self,
        to: str,
        subject: str,
        plain_msg: str,
        html_msg: str,
        file_paths: Optional[list[str]] = None
    ):
        """ Sends a HTML email

        Args:
            to (str): to email address
            subject (str): email subject
            plain_msg (str): email body in plain text
            html_msg (str): email body in HTML format
        """
        try:
            self.__logger.info('Creating email')
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.smtp_server.sender_email
            message["To"] = to
            part1 = MIMEText(plain_msg, "plain")
            part2 = MIMEText(html_msg, "html")
            message.attach(part1)
            message.attach(part2)

            for f in file_paths or []:
                self.__logger.info(f'Adding attachment: {f}')
                with open(f, "rb") as fil:
                    ext = f.split('.')[-1:][0]
                    attached_file = MIMEApplication(fil.read(), _subtype=ext)
                    attached_file.add_header(
                        'content-disposition',
                        'attachment',
                        filename=basename(f)
                    )
                    message.attach(attached_file)

            self.__logger.debug(f'Sending email to:\t{to}')
            self.__logger.debug(f'{subject} | {plain_msg}')
            self.smtp_server.server.sendmail(
                self.smtp_server.sender_email, to, message.as_string()
            )
        except Exception as e:
            self.__logger.error(e)
