import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mbox
import pathlib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

options = {
    'email_from': '',
    'smtp': '',
    'password': '',
    'email_to': '',
    'folder': ''
}

data_correct_flag = 0


def center_window(wnd, window_width, window_height):
    shift_x = (wnd.winfo_screenwidth() - window_width) // 2
    shift_y = (wnd.winfo_screenheight() - window_height) // 2
    wnd.geometry('%dx%d+%d+%d' % (window_width, window_height, shift_x, shift_y))


def toggle_controls_state(new_state):
    email_from.configure(state=new_state)
    password.configure(state=new_state)
    smtp_address.configure(state=new_state)
    email_to.configure(state=new_state)
    folder.configure(state=new_state)


def show_alert(message):
    mbox.showerror('Ошибка', 'Не все поля заполнены')


def get_value(entry):
    global data_correct_flag
    value = entry.get().lstrip().rstrip()
    if value == '':
        return
    else:
        data_correct_flag += 1
        return value


def get_data():
    global options
    options['email_from'] = get_value(email_from)
    options['smtp'] = get_value(smtp_address)
    options['password'] = get_value(password)
    options['email_to'] = get_value(email_to)
    options['folder'] = get_value(folder)


def get_folder():
    global options
    folder_path = filedialog.askdirectory()
    options['folder'] = folder_path
    folder.delete(0, tk.END)
    folder.insert(0, options['folder'])


def get_file_list(path):
    file_list = []
    for curr_file in pathlib.Path(path).iterdir():
        file_list.append(curr_file)
    return file_list


def stop_scan():
    toggle_controls_state('normal')
    scan_btn.configure(text='Начать отслеживание')
    scan_btn.configure(command=start_scan)


def send_email(file_to_send):
    global options
    msg = MIMEMultipart()
    file_name = str(file_to_send.name)
    email_password = options['password']
    msg['From'] = options['email_from']
    msg['To'] = options['email_to']
    msg['Subject'] = 'Пришел файл'

    part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(file_name))
    part_file.set_payload(open(str(file_to_send), "rb").read())
    part_file.add_header('Content-Description', file_name)
    part_file.add_header('Content-Disposition', 'attachment; filename="{}"'.format(file_name))
    encoders.encode_base64(part_file)

    msg.attach(part_file)

    msg.attach(MIMEText(file_name, 'plain'))
    server = smtplib.SMTP(options['smtp'])
    server.starttls()
    server.login(msg['From'], email_password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def start_scan():
    global data_correct_flag, options
    data_correct_flag = 0
    get_data()
    if data_correct_flag < 5:
        show_alert('Не все поля заполнены')
        return
    toggle_controls_state('disabled')
    scan_btn.configure(text='Завершить отслеживание')
    scan_btn.configure(command=stop_scan)
    file_list = get_file_list(options['folder'])
    for file in file_list:
        send_email(file)
        sent_file_list.insert(tk.END, str(file.name)+' sent\n')


# Главное окно ----------------------------------------------------------------
main_window = tk.Tk()
favicon = tk.PhotoImage(file='favicon.png')
main_window.iconphoto(False, favicon)
main_window.title('Пересылка файлов по почте')
main_window.resizable(False, False)
center_window(main_window, 640, 480)

# Добавление панели настроек
control_panel = tk.Frame(main_window, relief=tk.RAISED, borderwidth=1)
control_panel.grid(row=0, column=0, stick='we')
# Поле для прогресса
sent_file_list = tk.Text(main_window, borderwidth=2)
sent_file_list.grid(row=1, column=0, stick='we')

# Добавление контролов на пенель E-mail отправителя
tk.Label(control_panel, text='Email отправителя').grid(row=0, column=0, stick='e', pady=5)
email_from = tk.Entry(control_panel)
email_from.grid(row=0, column=1, stick='we')

tk.Label(control_panel, text='Пароль').grid(row=0, column=2, stick='e')
password = tk.Entry(control_panel, show='*')
password.grid(row=0, column=3, stick='we')

tk.Label(control_panel, text='SMTP сервер').grid(row=1, column=0, stick='e')
smtp_address = tk.Entry(control_panel)
smtp_address.grid(row=1, column=1, stick='we')

tk.Label(control_panel, text='E-mail получателя').grid(row=2, column=0, stick='e', pady=5)
email_to = tk.Entry(control_panel)
email_to.grid(row=2, column=1, stick='we')

tk.Button(control_panel, text="Выберите папку", command=get_folder).grid(row=4, column=0, stick='we', padx=3)
folder = tk.Entry(control_panel)
folder.grid(row=4, column=1, columnspan=3, stick='we')

scan_btn = tk.Button(control_panel, text='Начать отслеживание', command=start_scan)
scan_btn.grid(row=5, column=3, stick='we', pady=3)

control_panel.grid_columnconfigure(0, minsize=120)
control_panel.grid_columnconfigure(1, minsize=250)
control_panel.grid_columnconfigure(2, minsize=80)
control_panel.grid_columnconfigure(3, minsize=185)


main_window.mainloop()

# В JavaScript это было-бы так
# const foo() { тут код функции}
# const interval1 = setInterval(60000,foo) и foo вызывалась бы каждую минуту
# независимо от выполнения остального кода
# по определенному событию можно эти вызовы прекратить вызвав clearInterval(interval1)
# Что-то подобное желательно на Питоне исполнить.
