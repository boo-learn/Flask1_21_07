import sqlite3

select_quotes = "SELECT * from quotes"
# Подключение в БД
connection = sqlite3.connect("test.db")
# Создаем cursor, он позволяет делать SQL-запросы
cursor = connection.cursor()
# Выполняем запрос:
cursor.execute(select_quotes)

# Извлекаем результаты запроса
quotes = cursor.fetchall()
print(f"{quotes=}")

# Закрыть курсор:
cursor.close()
# Закрыть соединение:
connection.close()
