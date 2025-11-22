import glob
import os
import re
import shutil

from Excel.excel_reader import get_all_questions_from_excel_file
from Question import Question
from TICKET.ticket import create_gift
from config import INPUT_DIR, OUTPUT_DIR, TXT_FILE_CATEGORY, OUTPUT_DIR_GIFT
from ispring import create_excel_file_for_ispring, create_tickets, create_txt_file_category
from utils.utils import get_all_files_from_pattern


def check_images_in_folder(questions: [Question]):
    questions_with_images = [q for q in questions if q.image != '']
    for q in questions_with_images:
        file = q.image
        if not os.path.exists(str(file)):
            raise FileNotFoundError(f'[{file}]')


def copy_images_to_folder_exam(ticket, dir):
    for q in ticket.all_questions:
        if q.image not in ('', None):
            shutil.copyfile(q.image, os.path.join(dir, os.path.basename(q.image)))


def main():
    exams_name_path = {}

    for file in get_all_files_from_pattern(INPUT_DIR, '.xlsx'):
        exam_name = re.sub(r'.xlsx$', '', os.path.basename(file))
        exams_name_path[exam_name] = file

    for exam_name, file in exams_name_path.items():
        print(f'{exam_name}:', end='')
        questions: [Question] = get_all_questions_from_excel_file(file)
        check_images_in_folder(questions)

        for i, ticket in enumerate(create_tickets(questions)):
            dir = os.path.join(str(OUTPUT_DIR), str(exam_name), str(i))
            os.makedirs(dir, exist_ok=True)

            create_excel_file_for_ispring(ticket=ticket, exam_name=exam_name, path_out=dir, num_box=i)
            create_gift(ticket=ticket, exam_name=exam_name, path_out=OUTPUT_DIR_GIFT, num_box=i)
            create_txt_file_category(ticket, file_path=os.path.join(dir, TXT_FILE_CATEGORY), max_questions_in_ticket=30)
            copy_images_to_folder_exam(ticket, dir)
        print('OK')
    merge_gift_files_clean(OUTPUT_DIR_GIFT, './out/all_gift.txt')


def merge_gift_files_clean(source_dir, output_file):
    output_path = output_file
    search_path = os.path.join(source_dir, '*.txt')
    gift_files = glob.glob(search_path)

    if not gift_files:
        print(f"❌ В папке '{source_dir}' не найдено файлов с расширением .gift.")
        return

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for filename in gift_files:
                with open(filename, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n')

        print(f"\n✅ Все файлы успешно объединены в: **{output_path}**")
    except IOError as e:
        print(f"\n❌ Произошла ошибка при работе с файлами: {e}")
    except Exception as e:
        print(f"\n❌ Произошла непредвиденная ошибка: {e}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Stop')
