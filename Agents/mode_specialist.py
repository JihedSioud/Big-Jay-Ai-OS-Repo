# The Coder agent is explicitly wired to DeepSeek
coder_llm = ChatOpenAI(base_url="http://localhost:4005/v1", model="ollama/deepseek-coder", api_key="sk-1234")