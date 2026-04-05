# The gateway routes the request, the manager assigns the task
god_llm = ChatOpenAI(base_url="http://localhost:4005/v1", model="big-jay-router", api_key="sk-1234")

crew = Crew(
    agents=[specialist_1, specialist_2],
    tasks=[massive_data_task],
    process=Process.hierarchical,
    manager_llm=god_llm
)