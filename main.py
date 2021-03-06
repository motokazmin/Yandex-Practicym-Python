import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    """  get_today_stats   
    1. Не давайте переменной имя, совпадающей с именем существующего типа(в данном случаеRecord).
    Это может приводит непонятным ошибкам или крашу во время выполнения. Простой пример, вы решили
    внутри цикла создать объект типа Record - вы получите ошибку во время выполнения TypeError.
    2. Цикл можно заменить более эффективной и более читабельной конструкцией:
    sum([rec.amount for rec in self.records if rec.date == dt.datetime.now().date()])
    """

    def get_today_stats(self):
        return sum([rec.amount for rec in self.records if rec.date == dt.datetime.now().date()])

    """
    Здесь также можно сделать более отпимальный подсчет, заменив цикл на более быструю sum.
    Цикл for выполняется как интерпретируемый байт-код, тогда как Python. sum() полностью
    выполняется в коде C. Кроме того, код C гарантирует, что не будет создавать новые
    объекты Python, если вместо этого он может сохранить сумму в типах C
    """

    def get_week_stats(self):
        today = dt.datetime.now().date()
        return sum([rec.amount for rec in self.records if 7 > (today - rec.date).days >= 0])


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return ('Хватит есть!')

    """
    Вообще конструкция if ... else плохо читабельна, можно исправить это, используя питоновский
    тип словарь. Ключом будет тип валюты, значением - кортеж из двух величин - RATE и тип валюты.
    К элементам словаря можно обращаться так: d[currency], но лучше делать это
    с помощью метода d.get(currency) - тогда не возникнет исключения выполнения при передаче функции
    не обрабатываемой валюты - китайского юаня, египетского фунта и т.д. :)
    """
class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        cash_remained = self.limit - self.get_today_stats()

        d = {'usd': (USD_RATE, 'USD'), 'eur': (EURO_RATE, 'Euro'), 'rub': (1.0, 'руб')}

        rate = d.get(currency)
        if rate is None:
            return f'Неизвестная валюта {currency}'

        cash_remained /= rate[0]
        currency_type = d.get(currency)[1]

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

    def get_week_stats(self):
        super().get_week_stats()
