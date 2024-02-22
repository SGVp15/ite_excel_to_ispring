import json
import os
import random

from Excel.excel_reader import get_all_questions_from_excel_file
from config import dir_out
from ispring import create_excel_file_for_ispring
from Question import Question


def create_folders(name):
    os.makedirs(f'{dir_out}/{name}/json', exist_ok=True)


def get_num_question_category_version(s) -> (int, int, int):
    s = s.split('.')
    try:
        num_question = int(s[1])
        category = int(s[2])
        version = int(s[3])
        return num_question, category, version
    except (IndexError, ValueError):
        return 0, 0, 0


def create_new_ticket(questions: [Question]) -> [Question]:
    ticket = []
    box_question = []
    while len(ticket) < 30 and len(questions) > 0:
        max_len = max(0, len(questions) - 1)
        n = random.randint(0, max_len)
        question = questions[n]
        if question.box_question == 'None' or question.box_question not in box_question:
            box_question.append(question.box_question)
            ticket.append(question)
        del questions[n]
    return ticket


def set_to_json(obj, file_name):
    with open(f'{file_name}.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(obj))


def get_from_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        obj = json.loads(f.read())
    return obj


if __name__ == '__main__':
    exams = []
    exams.extend(['ITIL4FC', 'RCVC', 'CPIC', 'ICSC', 'Cobit2019C',
                  'BAFC', 'BASRMC'])

    for exam in exams:
        print(f'\n{exam}[  create_new_tickets  ]')
        create_excel_file_for_ispring(get_all_questions_from_excel_file(exam))
