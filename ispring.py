import os
import random

import openpyxl
from Question import Question
from TICKET.ticket import Ticket
from config import template_file_for_ispring, output_dir


def get_random_index_list_quest(list_quest, max_group):
    out = []
    for group in range(0, max_group):
        l = []
        for i, v in enumerate(list_quest):
            v1 = v - 1
            if v1 < len(out) or len(out) == 0:
                l.append(random.randint(0, v1))
            else:
                temp_l = []
                for o in out:
                    temp_l.append(o[i])
                n = 0
                while True:
                    n = random.randint(0, v1)
                    if n not in temp_l:
                        break
                l.append(n)
        out.append(l.copy())
    return out


def create_category_file(questions, questions_by_category, exam_name, num, count_questions_in_ticket=30):
    os.makedirs(f'{output_dir}/{exam_name}/{num}', exist_ok=True)

    info_category_file = f'{output_dir}/{exam_name}/{num}/info_ticket_import.txt'
    with open(info_category_file, 'w', encoding='utf-8') as f:
        count_all_sum = 0

        categories = sorted(questions_by_category.keys())

        for category in categories:
            list_question = questions_by_category.get(category)
            count_proc_cat = round(len(list_question) / len(questions) * count_questions_in_ticket)
            if len(list_question) == 1:
                count_proc_cat = 1
            proc = len(list_question) / len(questions) * count_questions_in_ticket
            if proc > len(list_question):
                count_proc_cat = len(list_question)
            count_all_sum += count_proc_cat
            f.write(f'{category}\t\t{count_proc_cat}/{len(list_question)}'
                    f'\n')
        if count_all_sum != count_questions_in_ticket:
            f.write(f'\n{count_all_sum}\tВсего вопросов:{len(questions)}\t')
        else:
            f.write(f'\n{count_all_sum}')


def create_excel_file_for_import(questions: [Question], exam_name='', num=0):
    ticket = Ticket(questions)
    questions_by_category = ticket.questions_by_category
    create_category_file(ticket.all_questions, ticket.questions_by_category, exam_name, num)

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
            values_to_write = ['MC', q.text_question, q.image, '', '',
                               f'*{q.answer_a}', q.answer_b, q.answer_c, q.answer_d,
                               '', '', '', '', '', '', '', '', 1]

            # Write the numbers to the worksheet
            for i, v in enumerate(values_to_write):
                worksheet.cell(row=row + 1, column=i + 1, value=str(v))

        # Save the workbook to a file
        os.makedirs(os.path.join(output_dir, exam_name, str(num)), exist_ok=True)
        workbook.save(f'{output_dir}/{exam_name}/{num}/{category}.xlsx')


def create_tickets(questions: [Question]):
    tickets = []
    ticket = Ticket(questions)
    max_box = ticket.get_max_box()
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
