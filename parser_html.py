import re
from bs4 import BeautifulSoup
import json


def parse_quiz_review(html_content: str) -> dict:
    """
    Извлекает информацию о тесте, вопросы, ответы пользователя, правильные ответы
    и полный список всех вариантов ответа, ограничивая поиск блоком role="main".
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    results = {'test_info': {}, 'вопросы': []}

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

    # название теста из заголовка
    if 'название_теста' not in results['test_info']:
        test_title_tag = soup.find('h1', class_="h2 mb-0")
        if test_title_tag:
            results['test_info']['test_name'] = test_title_tag.text

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
        question_data['номер'] = q_no_tag.text.strip() if q_no_tag else 'N/A'
        q_state_tag = q_block.find('div', class_='state')
        question_data['статус'] = q_state_tag.text.strip() if q_state_tag else 'N/A'

        # !!! Извлечение Баллов (Новое поле) !!!
        grade_tag = q_block.find('div', class_='grade')
        question_data['баллы'] = grade_tag.text.strip() if grade_tag else 'Баллы не найдены'

        # !!! Извлечение Текста вопроса (div class="qtext") !!!
        q_text_tag = q_block.find('div', class_='qtext')
        # Извлекаем текст из дочернего элемента div.clearfix, если он есть
        question_data['вопрос'] = re.sub(r'\s+', ' ',
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

        question_data['все_варианты_ответа'] = all_options
        results['вопросы'].append(question_data)
    return results


# --- Пример использования скрипта ---
try:
    with open('1.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    parsed_data = parse_quiz_review(html_content)

    # Выводим результат в консоль в формате JSON
    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))

except FileNotFoundError:
    print("Ошибка: Файл '1.html' не найден.")
except Exception as e:
    print(f"Произошла ошибка при парсинге: {e}")
