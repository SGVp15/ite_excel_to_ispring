import os
import re

from Question import Question


class Ticket:
    def __init__(self, questions: [Question]):
        self.all_questions = questions
        self.questions = []
        self.box_question: list = []
        self.questions_with_box: list = []
        self.questions_without_box: list = []

        self.questions_by_category = {}
        self.questions_by_box = {}

        self.max_len_box = 1

        for question in self.all_questions:
            if question.category not in self.questions_by_category.keys():
                self.questions_by_category[question.category] = [question]
            else:
                self.questions_by_category[question.category].append(question)

            if question.box_question is not None:
                if question.box_question not in self.questions_by_box.keys():
                    self.questions_by_box[question.box_question] = [question]
                else:
                    self.questions_by_box[question.box_question].append(question)

            if question.box_question is None:
                self.questions_without_box.append(question)
            else:
                self.questions_with_box.append(question)

    def get_max_len_box(self):
        for k, v in self.questions_by_box.items():
            if len(v) > self.max_len_box:
                self.max_len_box = len(v)
        return self.max_len_box

    def create_unique_ticket(self, num):
        questions = []
        questions.extend(self.questions_without_box)

        for _, v in self.questions_by_box.items():
            len_box = num % len(v)
            questions.append(v[len_box])

        return Ticket(questions)


def create_gift(ticket: Ticket, exam_name: str, path_out: str, num_box: int) -> object:
    with open(file=f'{path_out}/gift.txt', mode='w', encoding='utf-8') as f:
        s = ''
        for i, q in enumerate(ticket.all_questions):
            q: Question
            s += f'$CATEGORY: $module$/top/{exam_name}_{num_box}/{q.category}\n\n'
            s += (f"::Вопрос{i + 1}::{q.text_question}{{\n"
                  f"\t={q.ans_a}\n"
                  f"\t~{q.ans_b}\n"
                  f"\t~{q.ans_c}\n"
                  f"\t~{q.ans_d}\n"
                  f"}}\n\n"
                  )
        f.write(s)
