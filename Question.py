from dataclasses import dataclass


@dataclass
class Question:
    id_question: str
    text_question: str
    answer_a: str
    answer_b: str
    answer_c: str
    answer_d: str
    image: str
    box_question: int
    category: str
    exam: str
