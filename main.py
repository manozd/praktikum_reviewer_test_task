# В коде используется только класс datetime.datetime, поэтому можно не таскать с собой весь модуль datetime.
# Можно написать:
# from datetime import datetime
# или
# from datetime import datetime as dt
# Так мы сэкономим немного памяти и выражение с этой библиотекой станет чуть короче, что лучше для восприятия.
# В целом, импортируем только то, что используем.
import datetime as dt

# Желательно для каждого класса писать маленький комментарий о том, что он делает.
# Сам комментарий должен быть в тройных кавычках: """комментарий""". Это стандарт PEP 257
# Называется Docstring.
# Ссылка: https://peps.python.org/pep-0257/
# Другим пользователям кода будет легче в нем разобраться.
# Например, они смогут посмотреть этот комментарий с помощью аттрибута __doc__.

class Record:
    # После каждой переменной внутри скобок желательно писать тип данных, который ожидатся. 
    # Например: def __init__(self, amount: int, comment: str, date: str = ''). 
    # Для этого можно также использовать встроенную библиотеку typing.
    # Ссылка: https://docs.python.org/3/library/typing.html
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Лучше написать без отрицания not.
        # Без not в данном случае текст кода будет пониматься легче.
        
        # Кроме того, в коде неудачный перенос на новую строку после if
        # Следовало бы написать так:
        # self.date = (
        #     dt.datetime.now().date()
        #     if not date
        #     else dt.datetime.strptime(date, '%d.%m.%Y').date()
        # )
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        
        # Желательно поменять местами объявление self.date и self.comment и сделать порядок таким же,
        # как и внутри скобок выше __init__(...).
        # Так читается лучше и выглядит красивее.
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # Тут стоит уточнить в объявлении функции, что record это объект класса Record
    # def add_record(self, record: Record):
    # Стоит еще написать проверку (напирмер assert), что record это объект класса Record. 
    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # Объект Record нужно писать с маленькой буквы, так это не сам класс,
        # а объект класса Record.
        
        # Чем меньше вложенных конструкций for, if и т.д. тем лучше.
        # Предлагаю попытаться переписать  функцию с использованием list comprehensions
        # Ссылка: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        # Может получится переписать функцию в 2 или даже в 1 простую и понятную строку!
        # Пример: range_sum = sum([i for i in range(10)]).
        # Это работает и для кортежей...
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Здесь стоит написать так:
                # today_stats += Record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # Здесь можно попытаться переписать функцию с использованием list comprehensions аналогично предыдущему варианту.
        # Это не критично, но лучше пользоваться возможностями, которые предлагает python.
        # Стоит еще иметь в виду, что list comprehensions это не всегда хорошо,
        # В каждом отдельном случае нужно думать, стоит ли его использовать.
        # Наша главная задача написать максимально простой и понятный код, который дает правильный результат!
        for record in self.records:
            # Условие ниже будет правильнее переписать вот так:
            # if 0 <= (today - record.date).days < 7:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Скобки лишние, лучше убрать.
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Лучше не конвертировать их во float. Лишняя опреация, ничего не дает.
    # Деление работает и с типом int
    # Например: 10 / 10 = 1.0
    # Если очень хочется именно float, то можно написать 60.0 и 70.0
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    
    # USD_RATE=USD_RATE и EURO_RATE=EURO_RATE объявлять не нужно, это уже глобальные переменные класса, функция их видит.
    # Получится ли взять просто USD_RATE и EURO_RATE внутри функции?
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        
        # Это лишняя строка. currency_type будет присвоено другое значение чуть ниже.
        # Если, конечно, currency это usd, eur или rub
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        
        # Возможно стоило бы создать объекты dict в начале файла или внутри тела класса, которые имеют, например, такую структуру
        # CURRENCY_RATE_DICT = {"usd": 60, "Euro": 70, "руб": 1}
        # CURRENCY_TYPE_DICT = {"usd": "USD", "eur": "Euro", "rub": "руб"}
        # Во-первых, это удобнее. Если появится новая валюта, то будет достаточно вписать ее в эти словари и не дописывать код функции.
        # Главное, чтобы значение CURRENCY_RATE_DICT не было 0. Может стоит дописать проверку, чтобы такого не допускалось.
        # Во-вторых, сложное условие if ниже будет переписано в 2 строки
        # cash_remained /= CURRENCY_RATE_DICT[currency]
        # currency_type = CURRENCY_TYPE_DICT[currency]
        # Этот комментарий необязательный так как в условии задания сказанно объявить именно константы USD_RATE и EURO_RATE,
        # Но всегда стоит продумывать структуру кода заранее, чтобы в будущем было легче его использовать, читать и изменять.
        # Стоит еще написать проверку, что currency, которое пришло на вход это usd, eur или rub.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    
    # Эта функция не работает, при вызове мы получим None.
    # Хороший вопрос на подумать: что нужно сделать с функцией, чтобы она заработала? 
    # В целом, super() нужно использовать, когда мы хотим как-то дополнить метод родительского класса
    # В нашем случае мы ничего не дополняем и следующие 2 строчки можно просто убрать.
    # Дополнительно можно почитать тут: https://docs-python.ru/tutorial/vstroennye-funktsii-interpretatora-python/funktsija-super/
    def get_week_stats(self):
        super().get_week_stats()
