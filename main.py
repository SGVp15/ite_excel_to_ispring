import os
import re

from Excel.excel_reader import get_all_questions_from_excel_file
from Question import Question
from config import INPUT_DIR
from ispring import create_excel_file_for_import, create_tickets


def check_images_in_folder(questions: [Question]):
    questions_with_images = [q for q in questions if q.image != '']
    for q in questions_with_images:
        file = q.image
        if not os.path.exists(str(file)):
            raise FileNotFoundError(file)


def get_all_excel_files(dir, pattertn):
    files_xlsx = []
    for root, dirs, files in os.walk(INPUT_DIR):
        for name in files:
            if name.endswith(pattertn):
                files_xlsx.append(os.path.join(root, name))
    return files_xlsx


if __name__ == '__main__':
    exams_name_path = {}

    files_xlsx = get_all_excel_files(INPUT_DIR, '.xlsx')

    for file in files_xlsx:
        exam_name = re.sub(r'.xlsx$', '', file)
        exams_name_path[exam_name] = file

    for exam_name, file in exams_name_path.items():
        print(exam_name)
        questions: [Question] = get_all_questions_from_excel_file(file)
        folder = os.path.dirname(file)
        check_images_in_folder(questions)

        questions_in_ticket = create_tickets(questions)
        for i, questions_t in enumerate(questions_in_ticket):
            create_excel_file_for_import(
                questions=questions_t, exam_name=exam_name, num_box=i,
                max_questions_in_ticket=30
            )
