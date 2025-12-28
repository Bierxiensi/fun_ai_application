from IntentAgent import IntentAgent

if __name__ == "__main__":
    agent = IntentAgent()
    user_input = "客户经理被投诉了，投诉一次扣多少分"
    file_path = 'data/浦发上海浦东发展银行西安分行个金客户经理考核办法.pdf'
    # user_input = "迪士尼有几个园区"
    # file_path = 'data/迪士尼乐园 _园区地图、各主题区域介绍.docx'
    # user_input = "迪士尼各个园区有什么项目？"
    # file_path = 'data/迪士尼乐园项目.xlsx'
    result = agent.run(user_input, file_path) 
    print(result)
