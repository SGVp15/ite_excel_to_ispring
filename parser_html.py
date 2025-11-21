import os
import re
from itertools import count
from multiprocessing.connection import answer_challenge

from bs4 import BeautifulSoup
import json

from Excel.excel_reader import get_all_questions_from_excel_file
from Question import Question
from config import INPUT_DIR
from utils.utils import get_all_files_from_pattern


def parse_quiz_review(html_content: str) -> dict:
    """
    Извлекает информацию о тесте, вопросы, ответы пользователя, правильные ответы
    и полный список всех вариантов ответа, ограничивая поиск блоком role="main".
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    results = {'test_info': {}, 'questions': []}

    # название теста из заголовка
    if 'название_теста' not in results['test_info']:
        test_title_tag = soup.find('h1', class_="h2 mb-0")
        if test_title_tag:
            results['test_info']['test_name'] = test_title_tag.text

    # --- 1. Ограничение поиска блоком div role="main" ---
    main_content = soup.find('div', role='main')
    if not main_content:
        results['error'] = 'Ошибка: Основной блок контента (div role="main") не найден.'
        return results

    # --- 2. Общая информация о тесте (generaltable quizreviewsummary) ---
    summary_table = main_content.find('table', class_='generaltable generalbox quizreviewsummary mb-0')

    if summary_table:
        for i, row in enumerate(summary_table.find_all('tr')):
            header = row.find('th')
            data = row.find('td')

            if header and data:
                header_text = header.text.strip()
                data_text = data.text.strip()
                if i == 0:
                    results['test_info']['user'] = data_text
                    continue
                results['test_info'][header_text] = data_text

    # Очистка и нормализация текста
    for key, value in list(results['test_info'].items()):
        results['test_info'][key] = re.sub(r'\s+', ' ', value).strip()

    # --- 3. Вопросы, ответы и все варианты ---
    # Ищем все блоки вопросов внутри main_content
    question_blocks = main_content.find_all('div', class_=re.compile(r'^que '))

    for q_block in question_blocks:
        question_data = {}

        # Номер вопроса и статус
        q_no_tag = q_block.find('span', class_='qno')
        question_data['number'] = q_no_tag.text.strip() if q_no_tag else 'N/A'
        q_state_tag = q_block.find('div', class_='state')
        question_data['status'] = q_state_tag.text.strip() if q_state_tag else 'N/A'

        # !!! Извлечение Баллов (Новое поле) !!!
        grade_tag = q_block.find('div', class_='grade')
        question_data['points'] = grade_tag.text.strip() if grade_tag else 'Баллы не найдены'

        # !!! Извлечение Текста вопроса (div class="qtext") !!!
        q_text_tag = q_block.find('div', class_='qtext')
        # Извлекаем текст из дочернего элемента div.clearfix, если он есть
        question_data['question_text'] = re.sub(r'\s+', ' ',
                                                q_text_tag.text.strip()) if q_text_tag else 'Текст вопроса не найден'

        # --- Извлечение всех вариантов ответа (data-region="answer-label") ---
        all_options = []
        answer_container = q_block.find('div', class_='answer')

        if answer_container:
            # Проходим по всем блокам вариантов (r0, r1, r2...)
            for option_div in answer_container.find_all('div', recursive=False):
                if not re.match(r'r\d+', ' '.join(option_div.get('class', []))):
                    continue

                # Ищем контейнер текста ответа (по data-region="answer-label")
                label_div = option_div.find('div', attrs={'data-region': 'answer-label'})
                option_text_tag = label_div.find('div', class_='flex-fill') if label_div else None
                option_text = option_text_tag.text.strip() if option_text_tag else 'Текст варианта не найден'

                # Проверка, был ли вариант выбран пользователем (по checked атрибуту или иконке)
                is_selected = option_div.find('input', checked=True) is not None

                # Проверка, является ли вариант правильным (по классу 'correct')
                is_correct_option = 'correct' in option_div.get('class', [])

                all_options.append(
                    re.sub(r'\s+', ' ', option_text).strip()
                    # 'выбран_пользователем': is_selected,
                    # 'является_правильным': is_correct_option
                )

        question_data['answers'] = all_options
        results['questions'].append(question_data)
    return results


# --- Пример использования скрипта ---
def main():
    try:
        with open('2.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        parsed_data = parse_quiz_review(html_content)

        # Выводим результат в консоль в формате JSON
        a = json.dumps(parsed_data, indent=4, ensure_ascii=False)
        # print(a)
        python_object = json.loads(a)
        # print(python_object)
        return python_object
    except FileNotFoundError:
        print("Ошибка: Файл '1.html' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")


if __name__ == '__main__':
    exams_name_path = {}
    for file in get_all_files_from_pattern(INPUT_DIR, '.xlsx'):
        exam_name = re.sub(r'.xlsx$', '', os.path.basename(file))
        exams_name_path[exam_name] = file

    all_questions = []
    for exam_name, file in exams_name_path.items():
        # print(f'{exam_name}:', end='')
        all_questions.extend(get_all_questions_from_excel_file(file))
    q_my = main()['questions']
    quests = []
    for i,q in enumerate(q_my):
        c = Question(
            text_question=q.get('question_text'),
            ans_a=q.get('answers')[0],
            ans_b=q.get('answers')[1],
            ans_c=q.get('answers')[2],
            ans_d=q.get('answers')[3])

        c.status = q.get('status')
        print(q.get('number'), c.status , q.get('status'))
        quests.append(c)

    # category: dict
    all_questions = [q for q in all_questions if q in quests]
    not_questions = [q for q in all_questions if q not in quests]

    answer_category = {}
    all_category = {}
    for q in all_questions:
        answer_category[q.category] = 0
        all_category[q.category] = 0

    for i, q in enumerate(quests):
        q: Question
        for q_all in all_questions:
            q_all: Question
            if q == q_all:
                all_category[q_all.category] += 1
                if q.status == 'Верно':
                    print(q_all.category,q.status)
                    answer_category[q_all.category] += 1
                break
    for k in sorted(all_category.keys()):
        print(f'{k}\t{answer_category[k]}\t{all_category[k]}')
