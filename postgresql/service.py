import psycopg2
from psycopg2 import Error

from settings import db_config


class CredentialsError(Exception):
    pass


class ConnectError(Exception):
    pass


class SQLError(Exception):
    pass


class ConnectDB:
    """Класс выполняет подключение и закрые запроса в БД.
     Конструкция запроса: with ConnectDB(config_db) as cursor:
                              Запрос."""
    def __init__(self, config_db=db_config) -> None:
        self.config = config_db

    def __enter__(self) -> 'cursor':
        """Выполняет подключение к БД"""
        try:
            self.connection = psycopg2.connect(**self.config)  # Подключение к существующей базе
            self.cursor = self.connection.cursor()  # Курсор для выполнения операций с базой данных
            return self.cursor
        except (Exception, Error) as error:
            print("Ошибка при подключение к существующей БД", error)
        except psycopg2.InterfaceError as err:
            raise ConnectError(err)
        except psycopg2.OperationalError as err:
            raise CredentialsError(err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрывает работу с БД"""
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_type is psycopg2.ProgrammingError:
            raise SQLError(exc_val)
        elif exc_type:
            raise exc_type(exc_val)


def use_database(query: 'sql_query'):
    """Функция отправления запроса в БД. СОдержит в себе подключение к БД."""
    with ConnectDB() as cursor:
        cursor.execute(query)


def select_query(query) -> list:
    """Возвращает данные в виде списка от SELECT запроса в БД"""
    storage_chapter = []
    with ConnectDB(db_config) as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            storage_chapter.append(row[0])
    return storage_chapter
