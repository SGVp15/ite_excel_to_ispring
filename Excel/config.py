import os

from config import path_questions

file_xlsx = {
    'ITIL4FC': os.path.join(path_questions, 'ITIL4FC.xlsx'),
    'CobitC': os.path.join(path_questions, 'CobitС.xlsx'),
    'BAFC': os.path.join(path_questions, 'BAFC.xlsx'),
    'BASRMC': os.path.join(path_questions, 'BASRMC.xlsx'),
    'ICSC': os.path.join(path_questions, 'ICSC.xlsx'),
    'RCVC': os.path.join(path_questions, 'RCVC.xlsx'),
    'CPIC': os.path.join(path_questions, 'CPIC.xlsx')
}

map_excel = {
    'Уровень по Блуму': 'C',
    'Раздел курса': 'D',
    'Версия презентация': 'E',
    'Ссылка на презентацию': 'F',
    'Ссылка на источник': 'G',
    'Код вопроса': 'H',
    'Блок вопросов': 'I',
    'Пояснение': 'J',
    'Действующий 1-да, 0-нет': 'K',
    'Версия': 'L',
}
