import os
import re

from Excel.excel_reader import get_all_questions_from_excel_file
from config import input_dir
from ispring import create_excel_file_for_import, create_tickets

if __name__ == '__main__':
    exams_name_path = {}
    files_xlsx = [x for x in os.listdir(input_dir) if x.endswith('xlsx')]
    for file in files_xlsx:
        exam_name = re.sub(r'.xlsx$', '', file)
        exams_name_path[exam_name] = os.path.join(str(input_dir), str(file))

    for exam_name, file in exams_name_path.items():
        print(exam_name)
        questions = get_all_questions_from_excel_file(file)

        questions_in_ticket = create_tickets(questions)
        for i, questions_t in enumerate(questions_in_ticket):
            create_excel_file_for_import(
                questions=questions_t, exam_name=exam_name, num_box=i,
                max_questions_in_ticket=30
            )
