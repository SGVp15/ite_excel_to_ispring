import os
import re

from Excel.excel_reader import get_all_questions_from_excel_file
from Question import Question
from config import INPUT_DIR
from ispring import create_excel_file_for_ispring, create_tickets
from utils.utils import get_all_files_from_pattern


def check_images_in_folder(questions: [Question]):
    questions_with_images = [q for q in questions if q.image != '']
    for q in questions_with_images:
        file = q.image
        if not os.path.exists(str(file)):
            raise FileNotFoundError(f'[{file}]')


def main():
    exams_name_path = {}

    for file in get_all_files_from_pattern(INPUT_DIR, '.xlsx'):
        exam_name = re.sub(r'.xlsx$', '', os.path.basename(file))
        exams_name_path[exam_name] = file

    for exam_name, file in exams_name_path.items():
        print(f'{exam_name}:', end='')
        questions: [Question] = get_all_questions_from_excel_file(file)
        check_images_in_folder(questions)

        questions_in_ticket = create_tickets(questions)
        for i, questions_t in enumerate(questions_in_ticket):
            create_excel_file_for_ispring(
                questions=questions_t, exam_name=exam_name, num_box=i,
                max_questions_in_ticket=30
            )

        print('OK')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Stop')
