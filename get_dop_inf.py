from typing import NamedTuple

# for verification GP and m_e
m_e_spisok = ['ВС', 'ВТК', 'ВПР', 'ВСТР', 'ЕФР', 'ЗУГ', 'КИН', 'КУЗ', 'КУДР',
              'МБ', 'МАМ', 'МАЙ', 'МОСК', 'ОМБ', 'ПЕТ', 'ПРД', 'ПРОп', 'ПРОл',
              'ЭРГ', 'ПРЗ', 'САЛ', 'СОЛ', 'СОР', 'СБ', 'СУГ', 'УГ', 'УБ', 'ФН',
              'ЮБ', 'ЮТЕПЛ', 'ЮС']
GP_spisok = [200, 225, 250, 270, 320, 400]

# for connection with BD
host = "127.0.0.1"
user = "postgres"
password = "122333"
db_name = "dvizhenie_BU"
port = "5432"


# coeff for rating
class Coeff(NamedTuple):
    GP: float
    first_stage: float
    second_stage: float
    RUO_rating: float
    m_e_rating: float


Rating = Coeff(GP=2.5, first_stage=2, second_stage=1.3, RUO_rating=1.5, m_e_rating=2.7)

if Rating.GP + Rating.first_stage + Rating.second_stage + Rating.RUO_rating + Rating.m_e_rating != 10:
    print("Сумма рейтинга не равна 10")