from email.mime.text import MIMEText
import smtplib


def send_email(email, height, average_height,count):
    from_email = "pamchinyemba@gmail.com"
    from_password = "nzsgyflsjmbuolvg"
    to_email=email

    subject="Height data"
    message = "Hey there, you height is <strong>{}</strong> and the average height for {} entries is {}".format(height, count, average_height)

    msg = MIMEText(message,"html")
    msg["Subject"] =subject
    msg["To"]=to_email
    msg["From"]=from_email


    #Loging into gmail

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)






