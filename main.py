import os

from Excel.excel_reader import get_all_questions_from_excel_file
from config import input_dir
from ispring import create_excel_file_for_import, create_tickets

if __name__ == '__main__':
    exams = {}
    files_xlsx = [x for x in os.listdir(input_dir) if x.endswith('xlsx')]
    for file in files_xlsx:
        exams[file[:-5]] = os.path.join(input_dir, file)

    for exam_name, file in exams.items():
        print(exam_name)
        questions = get_all_questions_from_excel_file(file)

        questions_in_ticket = create_tickets(questions)
        for i, questions_t in enumerate(questions_in_ticket):
            create_excel_file_for_import(questions_t, exam_name, i)
