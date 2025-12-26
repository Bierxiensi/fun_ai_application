from models.qwenLLM import QwenLLM

class IntentAgent:
    def __init__(self):
        self.llm = QwenLLM()

    def run(self, user_input: str, file_path: str) -> dict:
        instruction = """你是一个意图识别 Agent。
            你的任务：
            根据用户输入，判断用户当前最主要的系统意图。

            你只能从以下意图中选择一个：
            - rag_query：用户在询问某个具体知识点、概念或技术细节，并且需要根据本地资料回答问题。
            - unknown：无法判断或信息不足

            请输出 JSON，格式如下：
            {
                "query_type": "意图类型",
                "intent": "...",
                "confidence": "置信度(0-1)"
                "reason": "一句话解释"
            }
            不要输出任何多余文本。
        """
        response = self.llm.judge_intent(user_input, instruction)
        print(response)
        if(response["query_type"] == "unknown"):
            return self.llm.run(user_input)
        elif(response["query_type"] == "rag_query"):
            return self.llm.query_rag(user_input, file_path)
        else:
            return response
