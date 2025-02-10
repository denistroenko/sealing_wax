__version__ = '0.0.17'


import random
import smtplib
import os
from os.path import basename
import inspect
import sys
import logging
import logging.handlers
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate


def get_script_dir(follow_symlinks=True):
    """
    Возвращает путь к скрипту __main__ (папку)
    """
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return '{}/'.format(os.path.dirname(path))


def configure_logger(
        logger: object,
        screen_logging: bool = False,
        info_file_name: str = '%sinfo.log' % get_script_dir(),
        debug_file_name: str = '%sdebug.log' % get_script_dir(),
        error_file_name: str = '%serror.log' % get_script_dir(),
        date_format: str = '%Y-%m-%d %H:%M:%S',
        message_format: str = '%(asctime)s [%(name)s] %(levelname)s %(message)s',
        start_msg: str = ''
        ):

    """
    Стандартная конфигурация логгера. Передаваемый объект логгера должен быть
    создан на глобальном уровне модуля, в который импортируется эта функция.

    logger - Объект логгера
    screen_logging (False) - включить хендлер экрана
    debug_file_name, error_file_name - имена файлов для
    файловых хендлеров (если пустая строка - файловые хендлеры не создаются).
    start_msg - строка, записываемая в лог при старте
    """

    # set level
    logger.setLevel(logging.DEBUG)

    # create and configure formatters
    # standard formats
    file_formatter = logging.Formatter(fmt=message_format,
                                       datefmt=date_format,
                                       )
    if screen_logging:
        screen_formatter = logging.Formatter(fmt='%(message)s')
        screen_handler = logging.StreamHandler()
        screen_handler.setLevel(logging.INFO)
        screen_handler.setFormatter(screen_formatter)
        logger.addHandler(screen_handler)

    if info_file_name:
        file_info_handler = logging.handlers.RotatingFileHandler(
                filename=info_file_name, maxBytes=10485760, backupCount=5)
        file_info_handler.setLevel(logging.INFO)
        file_info_handler.setFormatter(file_formatter)
        logger.addHandler(file_info_handler)

    if debug_file_name:
        file_debug_handler = logging.handlers.RotatingFileHandler(
                filename=debug_file_name, maxBytes=10485760, backupCount=5)
        file_debug_handler.setLevel(logging.DEBUG)
        file_debug_handler.setFormatter(file_formatter)
        logger.addHandler(file_debug_handler)

    if error_file_name:
        file_error_handler = logging.handlers.RotatingFileHandler(
                filename=error_file_name, maxBytes=10485760, backupCount=5)
        file_error_handler.setLevel(logging.ERROR)
        file_error_handler.setFormatter(file_formatter)
        logger.addHandler(file_error_handler)

    if start_msg:
        logger.debug(start_msg)


# need edit for pep8!!!!!!!!!!!!!!!!!!!!!!!!
def human_space(bytes: int) -> str:
    if bytes >= 1024 ** 3:
        result = str('{}G'.format(round(bytes/1024**3, 1)))
    elif bytes >= 1024 ** 2:
        result = str('{}M'.format(round(bytes/1024**2, 1)))
    elif bytes >= 1024:
        result = str('{}K'.format(round(bytes/1024, 1)))
    else:
        result = str('{}b'.format(bytes))
    return result


# need edit for pep8!!!!!!!!!!!!!!!!!!!!!!!!
class PasswordGenerator:

    def __init__(self):
        self.use_special_symbols = False
        self.password_len = 12
        self.curent_password = ""
        self.get_new_password()

    def get_new_password(self):
        # Даем списки, из которых будет генерироваться пароль
        list_of_chars = list("qwertyuiopasdfghjklzxcvbnm")
        list_of_CHARS = list("QWERTYUIOPASDFGHJKLZXCVBNM")
        list_of_numbers = list("1234567890")
        list_of_symbols = list("""~!@#$%^&*()[]{};:"'<>,.""")

        if self.use_special_symbols:
            # Распределяем доли пароля как четверть от его длины
            # на каждый список (букв, БУКВ, цифр и символов)
            count_of_chars = int(self.password_len / 4)
            count_of_CHARS = int(self.password_len / 4)
            count_of_numbers = int(self.password_len / 4)
            count_of_symbols = self.password_len - \
                (count_of_chars + count_of_CHARS + count_of_numbers)
        else:
            count_of_CHARS = int(self.password_len / 3)
            count_of_numbers = int(self.password_len / 3)
            count_of_chars = \
                self.password_len - (count_of_CHARS + count_of_numbers)
            count_of_symbols = 0

        # Если нужная доля пароля превышает кол-во элементов списка этой доли,
        # то умножим список на ......
        if len(list_of_numbers) < count_of_numbers:
            list_of_numbers *= \
                int(count_of_numbers / len(list_of_numbers) + 1)
        if len(list_of_CHARS) < count_of_CHARS:
            list_of_CHARS *= \
                int((count_of_CHARS / len(list_of_CHARS)) + 1)
        if len(list_of_numbers) < count_of_numbers:
            list_of_numbers *= \
                int((count_of_numbers / len(list_of_numbers)) + 1)
        if len(list_of_symbols) < count_of_symbols:
            list_of_symbols *= \
                int((count_of_symbols / len(list_of_symbols)) + 1)

        # Перетасовываем элементы списка
        random.shuffle(list_of_chars)
        random.shuffle(list_of_CHARS)
        random.shuffle(list_of_numbers)
        random.shuffle(list_of_symbols)

        # Обрезаем списки
        list_of_chars = list_of_chars[:count_of_chars]
        list_of_CHARS = list_of_CHARS[:count_of_CHARS]
        list_of_numbers = list_of_numbers[:count_of_numbers]
        if self.use_special_symbols:
            list_of_symbols = list_of_symbols[:count_of_symbols]

        # Соединяем списки
        main_list = list_of_chars + list_of_CHARS + list_of_numbers
        if self.use_special_symbols:
            main_list += list_of_symbols

        # Перетасовываем элементы списка
        random.shuffle(main_list)

        # Возвращаем значение (строку)
        # Превращаем список в строку ("" - разделитель)
        self.curent_password = "".join(main_list)
        return self.curent_password


# need edit for pep8!!!!!!!!!!!!!!!!!!!!!!!!
class EmailSender:
    def __init__(self):
        self.__host = ''
        self.__login = ''
        self.__password = ''
        self.__from = ''
        self.__use_ssl = None
        self.__port = 0

    def configure(self,
                  smtp_hostname: str,
                  login: str,
                  password: str,
                  from_address: str,
                  use_ssl: bool = True,
                  port: int = 465,
                  ):
        self.__host = smtp_hostname
        self.__login = login
        self.__password = password
        self.__from = from_address
        self.__use_ssl = use_ssl
        self.__port = port

    def send_email(self, to_address: str, subject: str, message: str,
                   use_html_format: bool = False, attachment_files: tuple = ()):
        # Message object
        msg = MIMEMultipart()

        # Set message properties
        msg['Subject'] = subject
        msg['From'] = self.__from
        msg['To'] = to_address
        msg['Date'] = formatdate(localtime=True)

        # Attach text to message
        if use_html_format:
            msg.attach(MIMEText(message, "html", "utf-8"))
        else:
            msg.attach(MIMEText(message, "plain", "utf-8"))

        # Attach files
        for attachment_file in attachment_files:
            with open(attachment_file, "rb") as attachment:
                 part = MIMEApplication(attachment.read(),
                                        Name=basename(attachment_file))
                 part['Content-Disposition'] = (
                        'attachment; filename="%s"' % basename(attachment_file))
                 msg.attach(part)

        # Server choice
        if self.__use_ssl:
            server = smtplib.SMTP_SSL(self.__host, self.__port)
        else:
            server = smtplib.SMTP(self.__host)

        server.login(self.__login, self.__password)
        server.sendmail(self.__from, to_address, msg.as_string())
        server.quit()


# need edit for pep8!!!!!!!!!!!!!!!!!!!!!!!!
class HtmlLetter:

    def __init__(self, background_color: str = '#fff',
                 color: str = '#333', font_size: int = 14):

        self.__background_color = background_color
        self.__color = color
        self.__font_size = font_size
        self.__html_letter = '<html>\n\t<body style="' + \
            'background-color: {}; ' + \
            'color: {}; ' + \
            'font-size: {}px; ' + \
            '">\n{}\n' + '\t</body>\n</html>'
        self.__body = ''

    def get_letter(self):

        html_letter = \
            self.__html_letter.format(self.__background_color,
                                      self.__color,
                                      str(self.__font_size),
                                      self.__body)
        return html_letter

    def append(self,
            text: str = '',
            tag_type: str = 'div',
            weight: int = 0,
            color: str = '',
            font_size: int = 0,
            border: bool = False,
            width: str = '100%'):

        text_block = '\t\t'
        text_block += '<' + tag_type + ' style="'
        if weight > 0:
            text_block += 'font-weight: ' + str(weight) + '; '
        if color != '':
            text_block += 'color: ' + color + '; '
        if font_size > 0:
            text_block += 'font-size: ' + str(font_size) + 'px; '
        if border:
            text_block += 'border: 1px solid ' + color + '; '
        text_block += 'width: ' + width + '; '
        text_block += '">'
        if text != '':
            text_block += text
        else:
            text_block += '<br>'
        text_block += '</' + tag_type + '>\n'

        self.__body += text_block

    def reset(self):

        self.__body = ''

