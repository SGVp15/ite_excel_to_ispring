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

        self.max_len_box = 0

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

    # def get_dict_questions_by_category(self) -> dict:
    #     self.questions_by_category = {}
    #     categories = self.get_all_category_from_questions()
    #     for category in categories:
    #         questions_in_category = []
    #         for question in self.questions:
    #             if question.category == category:
    #                 questions_in_category.append(question)
    #         self.questions_by_category[category] = questions_in_category
    #     return self.questions_by_category
    #
    # def get_dict_questions_by_box(self) -> dict:
    #     self.questions_by_box = {}
    #     boxes = self.get_all_box_from_questions()
    #     for box in boxes:
    #         questions_in_box = []
    #         for question in self.questions_with_box:
    #             if question.box_question == box:
    #                 questions_in_box.append(question)
    #         self.questions_by_box[box] = questions_in_box
    #     return self.questions_by_box
    #
    # def get_all_category_from_questions(self) -> list[str]:
    #
    #     return sorted(categories)
    #
    # def get_all_box_from_questions(self) -> list[str]:
    #     boxes = []
    #     for q in self.questions_with_box:
    #         if q.box_question not in boxes:
    #             boxes.append(q.box_question)
    #     return sorted(boxes)

    def get_max_box(self):
        for k, v in self.questions_by_box.items():
            if self.max_len_box < len(v):
                self.max_len_box = len(v)
        return self.max_len_box

    def create_ticket(self, num):
        questions = []
        questions.extend(self.questions_without_box)

        for k, v in self.questions_by_box.items():
            len_box = num % len(v)
            questions.append(v[len_box])

        return questions
