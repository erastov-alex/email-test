import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import REAL_DB_PATH, SMTP_SERVER, SMTP_PORT, MAIL_PASSWORD, FROM_MAIL, TO_MAIL

class EmailSender:
    def __init__(self):
        self.from_mail = FROM_MAIL
        self.mail_password = MAIL_PASSWORD
        self.path2database = REAL_DB_PATH
    
    def _send_email_via_stmp(self, to_mail, verification_code):
        # Формирование письма
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Подтверждение Регистрации'
        msg['From'] = self.from_mail
        msg['To'] = to_mail

        # Текстовое содержимое
        text_content = f"""\
            Тест отправки кода {verification_code}
        """

        # HTML-содержимое
        html_content = f"""\
        <html>
        <head>
            <style>
                .container {{
                    width: 90%;
                    margin: auto;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: #f9f9f9;
                    border: 1px solid #ececec;
                    padding: 20px;
                    border-radius: 8px;
                }}
                h1 {{
                    color: #333;
                }}
                p {{
                    color: #666;
                    font-size: 14px;
                }}
                .code {{
                    font-size: 24px;
                    color: #2a7ae2;
                    font-weight: bold;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>test</h1>
                <div class="code">{verification_code}</div>
            </div>
        </body>
        </html>
        """

        # Присоединение текстового и HTML-содержимого к сообщению
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        '''
        
        Старый код, локально работает
        На хостинге ошибка  535, b'Incorrect authentication data' при 
        SMTP_SERVER = 'server190.hosting.reg.ru'
        SMTP_PORT = 465
        
        При использовании 
        SMTP_SERVER = 'server190.hosting.reg.ru'
        SMTP_PORT = 587 
        Ошибка [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1122)
        и локально и на хостинге
        '''
        
        # try:
        #     with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        #         server.login(self.from_mail, self.mail_password)
        #         server.sendmail(self.from_mail, to_mail, msg.as_string())
        #     print("Письмо отправлено успешно!")
        #     return "200"
        # except Exception as e:
        #     print(f"Ошибка при отправке письма: {e}")
        #     return f"Ошибка при отправке письма: {e}"
        
        
        '''
        
        Новый код, локально работает
        На хостинге при этом коде сайт падает ( Error ID: 9106651f) 
        SMTP_SERVER = 'server190.hosting.reg.ru'
        SMTP_PORT = 587
        
        '''
        
        # https://stackoverflow.com/questions/57715289/how-to-fix-ssl-sslerror-ssl-wrong-version-number-wrong-version-number-ssl
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(self.from_mail, self.mail_password)
                server.sendmail(self.from_mail, to_mail, msg.as_string())
            print("Письмо отправлено успешно!")
            return "200"
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
            return f"Ошибка при отправке письма: {e}"


if __name__ == "__main__":
    to_mail, verification_code = 'erastov.alex@gmail.com', '0000'
    sender = EmailSender()
    sender._send_email_via_stmp(TO_MAIL, verification_code)
    