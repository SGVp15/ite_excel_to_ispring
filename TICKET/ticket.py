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

    def get_max_len_box(self):
        for k, v in self.questions_by_box.items():
            if len(v) > self.max_len_box:
                self.max_len_box = len(v)
        return self.max_len_box

    def create_ticket(self, num):
        questions = []
        questions.extend(self.questions_without_box)

        for k, v in self.questions_by_box.items():
            len_box = num % len(v)
            questions.append(v[len_box])

        return questions
