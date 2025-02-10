import logging
from baseapplib import configure_logger, get_script_dir


logger = logging.getLogger(__name__)
configure_logger(logger,
                 debug_file_name='{}log/value_debug.log'.format(get_script_dir()),
                 error_file_name='{}log/value_error.log'.format(get_script_dir()),
                 )


class int_value:
    """
    Дескриптор данных (данные числового типа). Вызывает исключение при неверном
    формате данных при присваивании.
    """

    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        if isinstance(value, int):
            instance.__dict__[self.__name] = value
            logger.debug('%s = %s' % (self.__name, value))
        else:
            logger.critical('%s = %s' % (self.__name, value))
            raise ValueError('Неверный тип данных (верный - int).')


class str_value:
    """
    Дескриптор данных (данные строкового типа). Вызывает исключение при неверном
    формате данных при присваивании.
    """

    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        if isinstance(value, str):
            instance.__dict__[self.__name] = value
            logger.debug('%s = %s' % (self.__name, value))
        else:
            logger.critical('%s = %s' % (self.__name, value))
            raise ValueError('Неверный тип данных (верный - str).')


class list_value:
    """
    Дескриптор данных (данные типа список). Вызывает исключение при неверном
    формате данных при присваивании.
    """

    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        if isinstance(value, list):
            instance.__dict__[self.__name] = value
            logger.debug('%s = %s' % (self.__name, value))
        else:
            logger.critical('%s = %s' % (self.__name, value))
            raise ValueError('Неверный тип данных (верный - list).')


class dict_value:
    """
    Дескриптор данных (данные типа словарь). Вызывает исключение при неверном
    формате данных при присваивании.
    """

    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        if isinstance(value, dict):
            instance.__dict__[self.__name] = value
            logger.debug('%s = %s' % (self.__name, value))
        else:
            logger.critical('%s = %s' % (self.__name, value))
            raise ValueError('Неверный тип данных (верный - dict).')


class bool_value:
    """
    Дескриптор данных (данные типа булево). Вызывает исключение при неверном
    формате данных при присваивании.
    """

    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        if isinstance(value, bool):
            instance.__dict__[self.__name] = value
            logger.debug('%s = %s' % (self.__name, value))
        else:
            logger.critical('%s = %s' % (self.__name, value))
            raise ValueError('Неверный тип данных (верный - bool).')
