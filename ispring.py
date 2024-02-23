import os

import openpyxl

from Question import Question
from config import template_ispring


def get_all_category_from_questions(questions: list[Question]) -> list[str]:
    categories = []
    for q in questions:
        if q.category not in categories:
            categories.append(q.category)
    return sorted(categories)


def create_category_file(questions):
    categories = get_all_category_from_questions(questions)

    os.makedirs(f'./Category/{questions[0].exam}', exist_ok=True)

    category_file = f'./Category/{questions[0].exam}/category.txt'
    with open(category_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(categories))


def create_dict_category_questions(questions: [Question]) -> dict:
    questions_by_category = {}
    categories = get_all_category_from_questions(questions)
    for category in categories:
        questions_in_category = []
        for question in questions:
            if question.category == category:
                questions_in_category.append(question)
                # TODO replace to def
                # if q.box_question not in box_questions.keys() or q.box_question is None:
                #     box_questions[q.box_question] = [q]
                # else:
                #     box_questions[q.box_question].append(q)
        # questions_by_category[category] = box_questions.copy()
        questions_by_category[category] = questions_in_category.copy()
    return questions_by_category


def create_excel_file_for_ispring(questions: [Question]):
    create_category_file(questions)
    questions_by_category = create_dict_category_questions(questions)
    # for category, list_question in questions_by_category.items():
    #     print(f'{category}\t\t{len(list_question)}')

    head = read_template()
    for category, list_question in questions_by_category.items():
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        for i, v in enumerate(head):
            worksheet.cell(row=1, column=i + 1, value=str(v))

        row = 0
        # Create a list of values to write to the Excel file
        for q in list_question:
            row += 1
            values_to_write = ['MC', q.text_question, q.image, '', '',
                               f'*{q.answer_a}', q.answer_b, q.answer_c, q.answer_d,
                               '', '', '', '', '', '', '', '', 1]

            # Write the numbers to the worksheet
            for i, v in enumerate(values_to_write):
                worksheet.cell(row=row + 1, column=i + 1, value=str(v))

        # Save the workbook to a file
        os.makedirs(os.path.join(os.getcwd(), 'Category', questions[0].exam), exist_ok=True)
        workbook.save(f'./Category/{questions[0].exam}/{category}.xlsx')

    # max_group = 0
    # for category, list_quest in questions_by_category.items():
    #     for k, v in list_quest.items():
    #         max_group = max(max_group, len(v))
    #
    # for category, list_quest in questions_by_category.items():
    #     list_len_group = [len(i) for i in list_quest.values()]
    #     # index_list_quest = get_random_index_list_quest(list_len_group, max_group)
    #     for group_number in range(max_group):
    #         l_quest = []
    #         l_questions = [v for v in list_quest.values()]
    #         for i, v in enumerate(index_list_quest[group_number]):
    #             l_quest.append(l_questions[i][v])


def read_template(file=template_ispring):
    if os.path.isfile(file):
        workbook = openpyxl.load_workbook(file)
        page_name = workbook.sheetnames
        worksheet = workbook[page_name[0]]
        for row in worksheet.iter_rows(values_only=True):
            return row
