import os

LOG_FILE = os.path.join(os.getcwd(), 'log.txt')

template_file_for_ispring = './template_ispring.xlsx'

# Папка с вопросами
INPUT_DIR = './input'
os.makedirs(INPUT_DIR, exist_ok=True)

# output_dir = '//192.168.20.100/личные документы/Савушкин/ispring'
OUTPUT_DIR = './output'
os.makedirs(OUTPUT_DIR, exist_ok=True)
