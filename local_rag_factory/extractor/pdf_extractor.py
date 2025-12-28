from pypdfium2._helpers.page import PdfPage


import pypdfium2

class PdfExtractor():
    def __init__(self):
        pass

    def extract(self, file_path):
        text = ""
        pdf_reader = pypdfium2.PdfDocument(file_path, autoclose=True)
        try:
            for page_number, page in enumerate[PdfPage](pdf_reader):
                text_page = page.get_textpage()
                content = text_page.get_text_range()
                if content:
                    text += content
                text_page.close()
                page.close()
            return text
        finally:
            pdf_reader.close()
