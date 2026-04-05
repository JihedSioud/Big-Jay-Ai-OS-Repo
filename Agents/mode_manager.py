# The system decides who works, but uses Llama3 as the CEO brain
manager_llm = ChatOpenAI(base_url="http://localhost:4005/v1", model="ollama/llama3", api_key="sk-1234")

crew = Crew(
    agents=[researcher, analyst],
    tasks=[task1, task2],
    process=Process.hierarchical, # This turns on the Manager!
    manager_llm=manager_llm
)