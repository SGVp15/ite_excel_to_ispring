import os

LOG_FILE = os.path.join(os.getcwd(), 'log.txt')

template_file_for_ispring = './template_ispring.xlsx'

# Папка с вопросами
input_dir = './input'
os.makedirs(input_dir, exist_ok=True)

# output_dir = '//192.168.20.100/личные документы/Савушкин/ispring'
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)
