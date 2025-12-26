import os
import json
import dashscope
from tracemalloc import stop
from dotenv import load_dotenv
from retrievers.faiss import FaissRetriever

load_dotenv()
# 从环境变量中获取 API Key
dashscope.api_key = os.environ.get('QWEN_API_KEY')

def get_completion(prompt, model="qwen-turbo-latest"):
    messages = [{"role": "user", "content": prompt}]
    response = dashscope.Generation.call(
        model=model,
        messages=messages,
        result_format='message',
        temperature=0,
    )
    return response.output.choices[0].message.content

class QwenLLM:
    def __init__(self):
        self.faiss_retriever = FaissRetriever()

    def judge_intent(self, query, instruction):
        """自动识别Query类型"""
        prompt = f"""
            ### 指令 ###
            {instruction}

            ### 原始查询 ###
            {query}

            ### 分析结果 ###
        """
        
        response = get_completion(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "query_type": "未知类型",
                "intent": "unknown",
                "confidence": 0.5,
                "reason": "无法解析JSON格式"
            }
    
    def query_rag(self, query, file_path):
        context = self.faiss_retriever.run(query, file_path, k=10)

        instruction = """
            根据上下文回答原始查询，如果上下文没有相关信息，
            则回答'我没有找到相关信息，我可以帮你建立一个新的知识库'
            不要从网上搜索或者自己生成。
        """
        
        """根据查询生成知识"""
        prompt = f"""
            ### 指令 ###
            {instruction}

            ### 原始查询 ###
            {query}

            ### 上下文 ###
            {context}
            
            ### 分析结果 ###
        """
        
        response = get_completion(prompt)
        return response

    def run(user_input):
        response = get_completion(user_input)
        return response