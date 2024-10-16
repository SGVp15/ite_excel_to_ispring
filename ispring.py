import os
import shutil
from copy import deepcopy

import openpyxl

from Question import Question
from TICKET.ticket import Ticket
from config import template_file_for_ispring, OUTPUT_DIR
from list_utils import compress


def create_txt_file_category(questions, questions_by_category, exam_name, num, max_questions_in_ticket=30):
    os.makedirs(os.path.join(str(OUTPUT_DIR), str(exam_name), str(num)), exist_ok=True)

    info_category_file = os.path.join(str(OUTPUT_DIR), str(exam_name), str(num), 'info_ticket_import.txt')
    with open(info_category_file, 'w', encoding='utf-8') as f:
        count_all_sum = 0
        categories = sorted(questions_by_category.keys())

        list_max = [len(questions_by_category.get(category)) for category in categories]
        list_a = deepcopy(list_max)
        list_a, list_max = compress(list_a, list_max, max_questions_in_ticket)
        # for i, category in enumerate(categories):
        #     list_question = questions_by_category.get(category)
        #     count_proc_cat = round(len(list_question) / len(questions) * max_questions_in_ticket)
        #     if len(list_question) == 1:
        #         count_proc_cat = 1
        #     proc = len(list_question) / len(questions) * max_questions_in_ticket
        #     if proc > len(list_question):
        #         count_proc_cat = len(list_question)
        #     count_all_sum += count_proc_cat

        list_a, list_max = compress(list_a, list_max, max_questions_in_ticket)
        for i, category in enumerate(categories):
            f.write(f'{category}\t{list_a[i]}\t{list_max[i]}\n')
            print(f'\t{list_a[i]}\t{list_max[i]}\t{list_a[i] / list_max[i]}')
        if sum(list_max) < max_questions_in_ticket:
            f.write(f'\n{count_all_sum} Всего вопросов: {len(questions)}')
        else:
            f.write(f'\n{len(questions)}')
    print('\n')


def create_excel_file_for_ispring(questions: [Question], exam_name: str, num_box=0, max_questions_in_ticket=30):
    ticket = Ticket(questions)
    questions_by_category = ticket.questions_by_category
    create_txt_file_category(ticket.all_questions, ticket.questions_by_category, exam_name, num_box,
                             max_questions_in_ticket=max_questions_in_ticket)

    head = read_template()
    for category, question_list in questions_by_category.items():
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        for i, v in enumerate(head):
            worksheet.cell(row=1, column=i + 1, value=str(v))

        row = 0
        # Create a list of values to write to the Excel file
        for q in question_list:
            row += 1
            values_to_write = ['MC', q.text_question, os.path.basename(q.image), '', '',
                               f'*{q.answer_a}', q.answer_b, q.answer_c, q.answer_d,
                               '', '', '', '', '', '', '', '', 1]

            # Write the numbers to the worksheet
            for i, v in enumerate(values_to_write):
                worksheet.cell(row=row + 1, column=i + 1, value=str(v))

        # Save the workbook to a file
        dir = os.path.join(str(OUTPUT_DIR), str(exam_name), str(num_box))
        os.makedirs(dir, exist_ok=True)
        workbook.save(f'{dir}/{category[:2]}.xlsx')
    for q in questions:
        if q.image != '':
            shutil.copyfile(q.image, os.path.join(dir, os.path.basename(q.image)))


def create_tickets(questions: [Question]):
    tickets = []
    ticket = Ticket(questions)
    max_box = ticket.get_max_len_box()
    for i in range(max_box):
        tickets.append(ticket.create_ticket(i))
    return tickets


def read_template(file=template_file_for_ispring):
    if os.path.isfile(file):
        workbook = openpyxl.load_workbook(file)
        page_name = workbook.sheetnames
        worksheet = workbook[page_name[0]]
        for row in worksheet.iter_rows(values_only=True):
            return row
