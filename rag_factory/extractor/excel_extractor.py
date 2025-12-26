import pandas as pd

class ExcelExtractor():
    def extract(self, file_path: str):
        """解析Excel文件，提取全部文本"""
        print(file_path)
        
        # 使用pandas读取Excel文件
        try:
            # 读取所有sheet
            excel_file = pd.ExcelFile(file_path)
            all_text = []
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # 将DataFrame转换为文本
                sheet_text = []
                
                # 添加表头
                if not df.empty:
                    headers = df.columns.tolist()
                    sheet_text.append(" | ".join(str(h) for h in headers))
                    
                    # 添加数据行
                    for index, row in df.iterrows():
                        row_text = " | ".join(str(cell) for cell in row)
                        sheet_text.append(row_text)
                
                if sheet_text:
                    all_text.append(f"Sheet: {sheet_name}\n" + "\n".join(sheet_text))
            
            return "\n\n".join(all_text)
            
        except Exception as e:
            print(f"Excel文件解析错误: {e}")
            return ""
