import json
import os
import random

from Excel.excel_reader import get_all_questions_from_excel_file
from config import dir_out, input_dir
from ispring import create_excel_file_for_import, create_tickets
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
    exams = {}
    for file in os.listdir(input_dir):
        exams[os.path.basename(os.path.join(os.getcwd(), input_dir, file))[:-5]] = os.path.join(os.getcwd(), input_dir,
                                                                                                file)

    for exam_name, file in exams.items():
        print(exam_name)
        questions = get_all_questions_from_excel_file(file)

        questions_in_ticket = create_tickets(questions)
        for i, questions_t in enumerate(questions_in_ticket):
            create_excel_file_for_import(questions_t, exam_name, i)
