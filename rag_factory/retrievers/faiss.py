import os
import datetime
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from extractor.extract_processor import ExtractProcessor
load_dotenv()
# 从环境变量中获取 API Key
DASHSCOPE_API_KEY = os.environ.get('QWEN_API_KEY')
embeddings = DashScopeEmbeddings(model="text-embedding-v1", dashscope_api_key=DASHSCOPE_API_KEY)

class FaissRetriever:
    def __init__(self):
        self.index_path = 'data/faiss_index'
        self.metadata_path = 'data/faiss_metadata.json'
        
    def _load_existing_metadata(self):
        """加载已存在文档的元数据"""
        if os.path.exists(self.metadata_path):
            import json
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"files": {}, "content_hashes": {}}
        
    def _save_metadata(self, metadata):
        """保存元数据"""
        import json
        os.makedirs('data', exist_ok=True)
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
            
    def _get_content_hash(self, content):
        """生成内容哈希值"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()
        
    def is_file_processed(self, file_path):
        """判断文件是否已处理过"""
        metadata = self._load_existing_metadata()
        return file_path in metadata["files"]
        
    def add_documents(self, file_path):
        """向FAISS添加新文档"""
        # 检查文件是否已处理
        if self.is_file_processed(file_path):
            print(f"文件 {file_path} 已处理过，跳过")
            return False
            
        # 提取文档内容
        documents = ExtractProcessor(file_path).extract()
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ".", " ", ""],
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(documents)
        
        # 加载现有知识库或创建新的
        if os.path.exists(self.index_path):
            knowledgeBase = FAISS.load_local(self.index_path, embeddings, allow_dangerous_deserialization=True)
            # 添加新文档
            knowledgeBase.add_texts(chunks)
        else:
            knowledgeBase = FAISS.from_texts(chunks, embeddings)
            os.makedirs('data', exist_ok=True)
            
        # 保存更新后的知识库
        knowledgeBase.save_local(self.index_path)
        
        # 更新元数据
        metadata = self._load_existing_metadata()
        metadata["files"][file_path] = {
            "processed_at": str(datetime.datetime.now()),
            "chunk_count": len(chunks),
            "content_hash": self._get_content_hash(documents)
        }
        self._save_metadata(metadata)
        
        print(f"成功添加文档 {file_path}，共 {len(chunks)} 个文本块")
        return True
    
    def run(self, query, file_path=None, k=10):
        """运行检索"""
        # 如果提供了文件路径，先尝试添加文档
        if file_path:
            self.add_documents(file_path)
            
        # 加载知识库进行检索
        if not os.path.exists(self.index_path):
            raise ValueError("FAISS索引不存在，请先添加文档")
            
        knowledgeBase = FAISS.load_local(self.index_path, embeddings, allow_dangerous_deserialization=True)
        docs = knowledgeBase.similarity_search(query, k)
        
        return docs
