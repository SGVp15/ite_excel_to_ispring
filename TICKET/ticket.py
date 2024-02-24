from Question import Question


class Ticket:
    def __init__(self, questions):
        self.all_questions = questions
        self.questions: list(Question) = []
        self.box_question: list = []
        self.questions_by_category = {}

        for question in questions:
            if question.box_question is None:
                self.questions.append(question)
            if question.box_question not in self.box_question:
                self.questions.append(question)
                self.box_question.append(question.box_question)

    def get_dict_questions_by_category(self) -> dict:
        self.questions_by_category = {}
        categories = self.get_all_category_from_questions()
        for category in categories:
            questions_in_category = []
            for question in self.questions:
                if question.category == category:
                    questions_in_category.append(question)
            self.questions_by_category[category] = questions_in_category
        return self.questions_by_category

    def get_all_category_from_questions(self) -> list[str]:
        categories = []
        for q in self.questions:
            if q.category not in categories:
                categories.append(q.category)
        return sorted(categories)
