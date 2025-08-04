import os
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI


class Model:
    def __init__(self):
        self.store = {}
        self.llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.3, max_tokens=100, api_key=os.getenv('GEMINI_KEY'))
        
    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            history = InMemoryChatMessageHistory()
            history.add_message(SystemMessage(content="You are a helpful assistant. Only answer in brief (within 100 words)."),)
            self.store[session_id] = history
        return self.store[session_id]
    
    def getChain(self):
        chain = RunnableWithMessageHistory(self.llm, self.get_session_history)
        return chain

