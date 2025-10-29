class Question:
    def __init__(self):
        self.id_question: str = ''
        self.text_question: str = ''
        self.ans_a: str = ''
        self.ans_b: str = ''
        self.ans_c: str = ''
        self.ans_d: str = ''
        self.image: str = ''
        self.box_question: int
        self.category: str = ''
        self.exam: str = ''

    def __str__(self):
        return (f'{self.text_question}\t'
                f'{self.ans_a}\t'''
                f'{self.ans_b}\t'''
                f'{self.ans_c}\t'''
                f'{self.ans_d}\t'''
                f'{self.image}\t')
