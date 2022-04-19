import logging
from baseapplib import get_script_dir, EmailSender, configure_logger
from config import Config


# Global
config = Config()       # объект основной конфигурации
config_list = Config()  # объект конфигурации списка рассылки
sender = EmailSender()  # объект отправителя email
logger = logging.getLogger(__name__)  # объект логгера
script_dir = get_script_dir()         # путь к этому файлу .py


def load_config_defaults():
    config.set('default', 'template', f'{script_dir}templates/default')


def load_config():
    """
    Функция загрузки конфигурации и списка получателей.
    Вызывает у глобальных объектов config и config_list методы .read_file()
    """

    # Определить полные пути к файлам конфигурации
    config_file_name = f'{script_dir}config/default_config'
    config_list_file_name = f'{script_dir}config/default_list'

    try:
        # Прочитать файлы и загрузить конфигурацию
        logger.debug(f'Загрузка файла основной конфигурации '
                     f'{config_file_name} ...')
        config.read_file(config_file_name, except_if_error=True)
        logger.debug(f'Загрузка файла конфигурации списка отправителей'
                     f' {config_list_file_name}... ')
        config_list.read_file(config_list_file_name, except_if_error=True)
    except Exception:
        logger.debug(Exception, exc_info = True)
        logger.error('Возникла ошибка. Завершение работы.')
        exit()


def configure_email_sender():
    """
    Функция конфигурирует глобальный объект email-sendera (sender).
    """

    logger.debug('''Конфигурирование email-sender'а ...''')

    try:
        # Получить имя сервера (имя хоста)
        smtp_hostname = config.smtp.server
        # Получить логин
        login = config.smtp.user
        # Получить пароль
        password = config.smtp.password

        # Получить адрес отправителя (если указан)
        from_address = login
        if config.smtp.address:
            from_address = config.smtp.address

        # Получить: использовать SSL-сертификат (если указано)
        use_ssl = False
        if config.smtp.ssl.lower() == 'yes':
            use_ssl = True

        # Получить smtp-порт, если указан
        port = 25
        if config.smtp.port:
            port = config.smtp.port

        # Вызвать метод конфигурации у глобального объекта sender
        sender.configure(smtp_hostname=smtp_hostname,
                         login=login,
                         password=password,
                         from_address=from_address,
                         use_ssl=use_ssl,
                         port=port,
                         )
    except Exception:
        logger.debug(Exception, exc_info = True)
        logger.error('Возникла ошибка. Завершение работы.')
        exit()


def send_to_all():
    """
    Высылает всем получателям необходимые файлы в качестве вложений.
    Список получателей и имен файлов должен быть в config_list,
    в секции [main]
    """
    try:
        # Получить тему сообщения
        subject = 'Sealing Wax message'
        if config.smtp.subject:
            subject = config.smtp.subject

        if config.smtp.message:
            subject = config.smtp.message

        # Получить словарь строк. Ключи - email-адреса, значения - имена файлов
        lines :dict = config_list.get_section_dict('main')
    except Exception:
        logger.debug(Exception, exc_info = True)
        logger.error('Возникла ошибка. Завершение работы.')
        exit()

    # Пройти по каждому получателю и отправить необходимый файл
    for address in lines:
        logger.info(f'Sending to {address} file {lines[address]}...')
        try:
            # Получить текст сообщения
            with open(config.default.template, 'r') as template_file:
                message = template_file.read()

            file_name = lines[address].split('/')[-1]
            message = message.format(name=address,
                                    file_name=file_name,
                                    )
            # Инициалицация пустого списка
            attachment_files = []
            # Присоединить к списку отправителей текуцего отправителя
            attachment_files.append(f'{script_dir}{lines[address]}')

            logger.debug(f'attachment files: {attachment_files}')

            # Отправить email
            sender.send_email(to_address=address,
                              subject=subject,
                              message=message,
                              attachment_files=attachment_files,
                              )
        except Exception:
            logger.debug(Exception, exc_info = True)
            logger.error('Возникла ошибка.')


def main():
    configure_logger(logger=logger,
                     screen_logging=True,
                     start_msg='Start "Sealing Wax"!')
    load_config_defaults()
    load_config()
    configure_email_sender()
    send_to_all()
