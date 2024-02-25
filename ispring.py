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


def create_category_file(questions, questions_by_category, count_questions_in_ticket=30):
    os.makedirs(f'{output_dir}/{questions[0].exam}', exist_ok=True)

    info_category_file = f'{output_dir}/{questions[0].exam}/info_ticket_import.txt'
    with open(info_category_file, 'w', encoding='utf-8') as f:
        count_all_sum = 0
        for category, list_question in questions_by_category.items():
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


def create_excel_file_for_import(questions: [Question]):
    ticket = Ticket(questions)
    questions_by_category = ticket.get_dict_questions_by_category()
    create_category_file(ticket.questions, questions_by_category)

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
        os.makedirs(os.path.join(output_dir, questions[0].exam), exist_ok=True)
        workbook.save(f'{output_dir}/{questions[0].exam}/{category}.xlsx')


# def create_excel_file_for_ispring(questions: [Question]):
#     questions_by_category = create_dict_category_questions(questions)
#     create_category_file(questions, questions_by_category)
#
#     categories = []
#     for q in questions:
#         if q.category not in categories:
#             categories.append(q.category)
#     os.makedirs(f'./{output_dir}/{questions[0].exam}', exist_ok=True)
#     category_file = f'./{output_dir}/{questions[0].exam}/category.txt'
#     with open(category_file, 'w', encoding='utf-8') as f:
#         for category in categories:
#             f.write(category + '\n')
#
#     questions_by_category = {}
#     for category in categories:
#         box_questions = {}
#         for q in questions:
#             if q.category == category:
#                 if q.box_question not in box_questions.keys():
#                     box_questions[q.box_question] = [q]
#                 else:
#                     box_questions[q.box_question].append(q)
#         questions_by_category[category] = box_questions.copy()
#
#     # for category, dict_box_quest in questions_by_category.items():
#     #     print(f'{category}\t\t{len(dict_box_quest)}')
#
#     head = read_template()
#
#     max_group = 0
#     for category, dict_box_quest in questions_by_category.items():
#         for k, v in dict_box_quest.items():
#             max_group = max(max_group, len(v))
#
#     for category, dict_box_quest in questions_by_category.items():
#         list_len_group = [len(i) for i in dict_box_quest.values()]
#         index_list_quest = get_random_index_list_quest(list_len_group, max_group)
#         for group_number in range(max_group):
#             l_quest = []
#             l_questions = [v for v in dict_box_quest.values()]
#             for i, v in enumerate(index_list_quest[group_number]):
#                 l_quest.append(l_questions[i][v])
#
#             workbook = openpyxl.Workbook()
#             worksheet = workbook.active
#             j = 0
#             for i, v in enumerate(head):
#                 worksheet.cell(row=1, column=i + 1, value=str(v))
#
#             # Create a list of values to write to the Excel file
#             for q in l_quest:
#                 j += 1
#                 values_to_write = ['MC', q.text_question, '', '', '',
#                                    f'*{q.answer_a}', q.answer_b, q.answer_c, q.answer_d,
#                                    '', '', '', '', '', '', '', '', 1]
#
#                 # Write the numbers to the worksheet
#                 for i, v in enumerate(values_to_write):
#                     worksheet.cell(row=j + 1, column=i + 1, value=str(v))
#
#             # Save the workbook to a file
#             os.makedirs(name=f'./{output_dir}/{questions[0].exam}/{group_number}', exist_ok=True)
#             workbook.save(f'./{output_dir}/{questions[0].exam}/{group_number}/{category}.xlsx')


def read_template(file=template_file_for_ispring):
    if os.path.isfile(file):
        workbook = openpyxl.load_workbook(file)
        page_name = workbook.sheetnames
        worksheet = workbook[page_name[0]]
        for row in worksheet.iter_rows(values_only=True):
            return row
