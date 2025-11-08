import os

LOG_FILE = os.path.join(os.getcwd(), 'log.txt')

template_file_for_ispring = './template_ispring.xlsx'

# Папка с вопросами
INPUT_DIR = './input'

OUTPUT_DIR = './out'
OUTPUT_DIR_GIFT = './out/gift'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR_GIFT, exist_ok=True)
os.makedirs(INPUT_DIR, exist_ok=True)

TXT_FILE_CATEGORY = 'info_ticket_import.txt'
