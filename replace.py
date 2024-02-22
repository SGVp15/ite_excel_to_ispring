def replace_docx_text(document, old_text, new_text):
    old_text = '{' + old_text + '}'
    section = document.sections[0]
    header = section.header
    footer = section.footer
    for doc_obj in (document, header, footer):
        docx_replace_regex(doc_obj, old_text, new_text)


def docx_replace_regex(doc_obj, old_text: str, new_text: str):
    # Замена в параграфах
    for paragraph in doc_obj.paragraphs:
        if old_text not in paragraph.text:
            continue
        runs = paragraph.runs
        if len(runs) == 0:
            continue
        if len(runs) > 1:
            text = ''
            for run in runs:
                text += run.text
            runs[0].text = text
            for i in range(1, len(runs)):
                runs[i].text = ''
        runs[0].text = runs[0].text.replace(old_text, new_text)

    # Замена в таблицах
    for table in doc_obj.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_regex(cell, old_text, new_text)
