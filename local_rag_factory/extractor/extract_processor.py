import os
from extractor.pdf_extractor import PdfExtractor
from extractor.excel_extractor import ExcelExtractor
from extractor.word_extractor import WordExtractor

class ExtractProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def extract(self):
        file_extension = os.path.splitext(self.file_path)[1].lower()
        if file_extension == ".pdf":
            extractor = PdfExtractor()
        elif file_extension in {".xlsx", ".xls"}:
            extractor = ExcelExtractor()
        elif file_extension == ".docx":
            extractor = WordExtractor()
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

        return extractor.extract(self.file_path)
