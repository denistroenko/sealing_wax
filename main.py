"""
Sealing Wax - software for regulag mail sending.
"""

from baseapplib import get_script_dir, EmailSender
from config import Config


# Global
config = Config()
config_list = Config()
sender = EmailSender()


def load_config():
    """
    Функция загрузки конфигурации и списка получателей.
    Вызывает у глобальных объектов config и config_list методы .read_file()
    """

    # Получить путь к текущему скрипту
    script_dir = get_script_dir()
    # Получить полные пути к файлам с конфигурацией
    config_file_name = 'config/default_config'
    config_list_file_name = 'config/default_list'

    # Прочитать файлы и загрузить концигурацию
    config.read_file(f'{script_dir}{config_file_name}')
    config_list.read_file(f'{script_dir}{config_list_file_name}')

def configure_email_sender():
    pass
    #smtp_hostname =
    #sender.configure(smtp_hostname = '',
    #                 login = '',
    #                 password = '',
    #                 from_address = '',
    #                 use_ssl = '',
    #                 port = ''
    #                 )


def send_to_all():
    """
    Высылает всем получателям необходимые файлы в качестве вложений.
    Список получателей и имен файлов должен быть в config_list,
    в секции [main]
    """
    # Получить список отправителей и файлов
    settings = config_list.get_section_dict('main')

    # Пройти по каждому получателю и отправить необходимый файл
    for setting in settings:
        print(setting, 'Отправить %s' % settings[setting])


def main():
    load_config()
    configure_email_sender()
    send_to_all()


if __name__ == '__main__':
    main()
