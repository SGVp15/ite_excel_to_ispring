import os
import re
import shutil

from Excel.excel_reader import get_all_questions_from_excel_file
from Question import Question
from TICKET.ticket import create_gift
from config import INPUT_DIR, OUTPUT_DIR, TXT_FILE_CATEGORY
from ispring import create_excel_file_for_ispring, create_tickets, create_txt_file_category
from utils.utils import get_all_files_from_pattern


def check_images_in_folder(questions: [Question]):
    questions_with_images = [q for q in questions if q.image != '']
    for q in questions_with_images:
        file = q.image
        if not os.path.exists(str(file)):
            raise FileNotFoundError(f'[{file}]')


def copy_images_to_folder_exam(ticket, dir):
    for q in ticket.all_questions:
        if q.image not in ('', None):
            shutil.copyfile(q.image, os.path.join(dir, os.path.basename(q.image)))


def main():
    exams_name_path = {}

    for file in get_all_files_from_pattern(INPUT_DIR, '.xlsx'):
        exam_name = re.sub(r'.xlsx$', '', os.path.basename(file))
        exams_name_path[exam_name] = file

    for exam_name, file in exams_name_path.items():
        print(f'{exam_name}:', end='')
        questions: [Question] = get_all_questions_from_excel_file(file)
        check_images_in_folder(questions)

        for i, ticket in enumerate(create_tickets(questions)):
            dir = os.path.join(str(OUTPUT_DIR), str(exam_name), str(i))
            os.makedirs(dir, exist_ok=True)

            create_excel_file_for_ispring(ticket=ticket, exam_name=exam_name, path_out=dir, num_box=i)
            create_gift(ticket=ticket, exam_name=exam_name, path_out=dir, num_box=i)
            create_txt_file_category(ticket, file_path=os.path.join(dir, TXT_FILE_CATEGORY), max_questions_in_ticket=30)
            copy_images_to_folder_exam(ticket, dir)
        print('OK')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Stop')
