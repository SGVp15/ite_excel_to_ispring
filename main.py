import os
import re

from Excel.excel_reader import get_all_questions_from_excel_file
from Question import Question
from config import INPUT_DIR
from ispring import create_excel_file_for_ispring, create_tickets


def check_images_in_folder(questions: [Question]):
    questions_with_images = [q for q in questions if q.image != '']
    for q in questions_with_images:
        file = q.image
        if not os.path.exists(str(file)):
            raise FileNotFoundError(file)


def get_all_excel_files(folder_input: str, pattern: str):
    file_list = []
    for root, dirs, files in os.walk(folder_input):
        for name in files:
            if name.endswith(pattern):
                file_list.append(os.path.join(root, name))
    return file_list


if __name__ == '__main__':
    exams_name_path = {}

    files_xlsx: [None | str] = get_all_excel_files(INPUT_DIR, '.xlsx')

    for file in files_xlsx:
        exam_name = re.sub(r'.xlsx$', '', os.path.basename(file))
        exams_name_path[exam_name] = file

    for exam_name, file in exams_name_path.items():
        print(f'{exam_name}:', end='')
        questions: [Question] = get_all_questions_from_excel_file(file)
        folder = os.path.dirname(file)
        check_images_in_folder(questions)

        questions_in_ticket = create_tickets(questions)
        for i, questions_t in enumerate(questions_in_ticket):
            create_excel_file_for_ispring(
                questions=questions_t, exam_name=exam_name, num_box=i,
                max_questions_in_ticket=30
            )

        print('OK')
