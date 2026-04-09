import os
import json
import uuid
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

class WorkspaceManager:
    """
    Handles the physical directories for isolated projects.
    Ensures zero "context bleed" by maintaining separate workspaces and histories.
    """
    def __init__(self, base_dir: str = "/AI_OS_Projects"):
        self.base_dir = base_dir
        self.project_path = None
        self.workspace_dir = None
        self.vector_db_dir = None
        self.history_file = None

    def mount_project(self, project_name: str):
        """
        Creates or mounts the folder structure for a specific project.
        """
        # We can use a relative or absolute path based on base_dir.
        # Using abspath to ensure consistency.
        self.project_path = os.path.abspath(os.path.join(self.base_dir, project_name))
        self.workspace_dir = os.path.join(self.project_path, "workspace")
        self.vector_db_dir = os.path.join(self.project_path, "vector_db")
        self.history_file = os.path.join(self.project_path, ".history.json")

        os.makedirs(self.workspace_dir, exist_ok=True)
        os.makedirs(self.vector_db_dir, exist_ok=True)

        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def update_memory(self, role: str, content: str):
        """
        Appends a new message to the project's .history.json, keeping only the last 10 messages.
        """
        if not self.history_file:
            raise ValueError("Project not mounted. Call mount_project() first.")
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        history.append({"role": role, "content": content})
        
        # Keep only a rolling window of the last 10 messages
        history = history[-10:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4)

    def get_memory(self) -> list:
        """
        Retrieves the current short-term history.
        """
        if not self.history_file or not os.path.exists(self.history_file):
            return []
        with open(self.history_file, 'r', encoding='utf-8') as f:
            return json.load(f)


class LocalizedRAGEngine:
    """
    Manages the isolated ChromaDB and local embeddings for a single project.
    Embeddings are processed locally using BAAI/bge-m3 or nomic-embed-text-v1.5.
    """
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.embedding_model = SentenceTransformer(model_name)
        self.client = None
        self.collection = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def init(self, project_path: str):
        """
        Initializes a chromadb.PersistentClient pointing strictly to the mounted project's /vector_db/ folder.
        """
        vector_db_dir = os.path.join(project_path, "vector_db")
        self.client = chromadb.PersistentClient(path=vector_db_dir)
        self.collection = self.client.get_or_create_collection(name="project_collection")

    def ingest_file(self, file_path: str):
        """
        Reads a file, splits it, generates local embeddings, and saves them to the active project's Chroma collection.
        """
        if not self.collection:
            raise ValueError("RAGEngine not initialized. Call init() first.")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        chunks = self.text_splitter.split_text(text)
        
        if not chunks:
            return

        embeddings = self.embedding_model.encode(chunks).tolist()
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"source": file_path} for _ in chunks]

        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, top_k: int = 5) -> list:
        """
        Vectorizes the user's query and returns the most relevant chunks from the active project's database.
        """
        if not self.collection:
            raise ValueError("RAGEngine not initialized. Call init() first.")
            
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        if results and results['documents'] and results['documents'][0]:
            return results['documents'][0]
        return []


class AIHubClientMock:
    """
    Mock for the AIHubClient that routes requests through LiteLLM.
    """
    def generate(self, payload: str) -> str:
        # In the real system, this would call LiteLLM with the payload
        return "This is a simulated response based on the localized RAG context and project history."


class OSBridge:
    """
    The Orchestrator pipeline that connects the Workspace, the RAG Engine, and AIHubClient.
    """
    def __init__(self, workspace_manager: WorkspaceManager, rag_engine: LocalizedRAGEngine, ai_hub_client):
        self.workspace = workspace_manager
        self.rag = rag_engine
        self.ai_hub = ai_hub_client

    def handle_prompt(self, user_text: str) -> str:
        """
        Processes a user prompt by constructing a comprehensive context and routing it to the LLM.
        """
        # 1. Retrieve the top 5 relevant chunks from LocalizedRAGEngine.search()
        try:
            rag_chunks = self.rag.search(user_text, top_k=5)
            rag_context = "\n\n".join(rag_chunks)
        except Exception as e:
            rag_context = ""
            print(f"Warning: RAG search failed: {e}")

        # 2. Retrieve the last 10 chat messages from WorkspaceManager.get_memory()
        chat_history = self.workspace.get_memory()
        history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history])

        # 3. Construct a giant combined prompt: [System Instructions] + [RAG Context] + [Chat History] + [User Prompt]
        system_instructions = "You are Big Jay AI OS, a highly capable and secure assistant strictly operating within an isolated project."
        
        combined_prompt = f"""[System Instructions]
{system_instructions}

[RAG Context]
{rag_context if rag_context else "No relevant context found."}

[Chat History]
{history_text if history_text else "No prior history."}

[User Prompt]
{user_text}"""

        # 4. Yield this payload to the AIHubClient to get the LLM's response
        response = self.ai_hub.generate(combined_prompt)

        # 5. Save the final user prompt and LLM response back to the project's .history.json
        self.workspace.update_memory("user", user_text)
        self.workspace.update_memory("assistant", response)

        return response


# --- Example Initialization and Execution ---
if __name__ == "__main__":
    print("Initializing Big Jay AI OS Backend...\n")
    
    # 1. Initialize Components
    # Using local directory './AI_OS_Projects' for demonstration purposes
    workspace = WorkspaceManager(base_dir="./AI_OS_Projects")
    rag_engine = LocalizedRAGEngine(model_name="BAAI/bge-m3")
    ai_hub = AIHubClientMock()
    
    bridge = OSBridge(workspace, rag_engine, ai_hub)
    
    # 2. Mount Project "Syria_Health_Mapping"
    print("Mounting project: Syria_Health_Mapping")
    workspace.mount_project("Syria_Health_Mapping")
    
    # 3. Initialize RAG Engine for the specific project path
    rag_engine.init(workspace.project_path)
    
    # 4. Ingest sample data
    demo_file = os.path.join(workspace.workspace_dir, "syria_hospitals.txt")
    with open(demo_file, "w", encoding="utf-8") as f:
        f.write("The primary hospital in Damascus is Al-Assad University Hospital, handling severe trauma cases. "
                "There is also the Damascus Hospital, known locally as Al-Mujtahid Hospital, handling general emergencies.")
        
    print(f"Ingesting file into local ChromaDB: {demo_file}")
    rag_engine.ingest_file(demo_file)
    
    # 5. Process User Prompt
    prompt = "What are the main hospitals handling emergencies and trauma in Damascus?"
    print(f"\nProcessing User Prompt: '{prompt}'...")
    
    final_response = bridge.handle_prompt(prompt)
    
    print("\n--- LLM Final Response ---")
    print(final_response)
    
    # 6. Verify Memory Update
    print("\n--- Current Project Memory ---")
    print(json.dumps(workspace.get_memory(), indent=2))
