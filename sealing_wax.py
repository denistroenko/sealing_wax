import logging
from baseapplib import get_script_dir, EmailSender, configure_logger
from config import Config


# Global
config = Config()       # объект основной конфигурации
config_list = Config()  # объект конфигурации списка рассылки
sender = EmailSender()  # объект отправителя email
logger = logging.getLogger(__name__)  # объект логгера


def load_config():
    """
    Функция загрузки конфигурации и списка получателей.
    Вызывает у глобальных объектов config и config_list методы .read_file()
    """
    # Получить путь к текущему скрипту
    script_dir = get_script_dir()

    # Определить полные пути к файлам конфигурации
    config_file_name = f'{script_dir}config/default_config'
    config_list_file_name = f'{script_dir}config/default_list'

    try:
        # Прочитать файлы и загрузить концигурацию
        logger.debug(f'Загрузка файла основной конфигурации '
                     f'{config_file_name} ...')
        config.read_file(config_file_name, except_if_error=True)
        logger.debug(f'Загрузка файла конфигурации списка отправителей'
                     f' {config_file_name}... ')
        config_list.read_file(config_list_file_name, except_if_error=True)
    except Exception:
        logger.debug(Exception, exc_info = True)
        logger.error('Возникла ошибка. Завершение работы.')
        exit()


def configure_email_sender():
    logger.debug('''Конфигурирование email-sender'а ...''')

    try:
        smtp_hostname = config.smtp.server
        login = config.smtp.user
        password = config.smtp.password

        from_address = login
        if config.smtp.address:
            from_address = config.smtp.address

        use_ssl = False
        if config.smtp.ssl.lower() == 'yes':
            use_ssl = True

        port = 465
        if config.smtp.port:
            port = config.smtp.port

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

        # Получить текст сообщения
        message = 'Sealing Wax message'
        if config.smtp.message:
            subject = config.smtp.message

        # Получить список отправителей и файлов
        settings = config_list.get_section_dict('main')
    except Exception:
        logger.debug(Exception, exc_info = True)
        logger.error('Возникла ошибка. Завершение работы.')
        exit()

    # Пройти по каждому получателю и отправить необходимый файл
    for setting in settings:
        logger.info(f'Sending to {setting}...')
        try:
            sender.send_email(setting, subject, message)
        except Exception:
            logger.debug(Exception, exc_info = True)
            logger.error('Возникла ошибка. Завершение работы.')


def main():
    configure_logger(logger, screen_logging=True)
    logger.debug('### ### ### ## ## # Start program... # ## ## ### ### ###')
    load_config()
    configure_email_sender()
    send_to_all()
