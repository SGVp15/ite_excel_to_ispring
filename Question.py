class Question:
    def __init__(self):
        self.id_question: str = ''
        self.text_question: str = ''
        self.answer_a: str = ''
        self.answer_b: str = ''
        self.answer_c: str = ''
        self.answer_d: str = ''
        self.image: str = ''
        self.box_question: int
        self.category: str = ''
        self.exam: str = ''

    def __str__(self):
        return (f'{self.text_question}\t'
                f'{self.answer_a}\t'''
                f'{self.answer_b}\t'''
                f'{self.answer_c}\t'''
                f'{self.answer_d}\t'''
                f'{self.image}\t')
