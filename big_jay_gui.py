import customtkinter as ctk
import os
import subprocess
import webbrowser

INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x720")
app.title("🚀 Big-Jay AI-OS Command Center")
app.resizable(False, False)

# --- Functions ---
def boot_system(): subprocess.Popen(["docker", "compose", "up", "-d"], cwd=INSTALL_PATH, creationflags=subprocess.CREATE_NO_WINDOW)
def shutdown_system(): subprocess.Popen(["docker", "compose", "down"], cwd=INSTALL_PATH, creationflags=subprocess.CREATE_NO_WINDOW)

def open_webui(): webbrowser.open("http://localhost:3000")
def open_n8n(): webbrowser.open("http://localhost:5678")
def open_dockge(): webbrowser.open("http://localhost:5001")
def open_litellm(): webbrowser.open("http://localhost:4000")
def open_qdrant(): webbrowser.open("http://localhost:6333/dashboard")

def open_agent_folder(): os.startfile(os.path.join(INSTALL_PATH, "Agents"))
def launch_agent_terminal(): os.system(f'start powershell -NoExit -Command "cd \'{INSTALL_PATH}\\Agents\'; .\\venv\\Scripts\\activate"')
def launch_nemoclaw(): os.system('start wsl')

# --- Header ---
title_label = ctk.CTkLabel(app, text="Big-Jay AI-OS", font=ctk.CTkFont(size=26, weight="bold"))
title_label.pack(pady=(15, 0))
subtitle_label = ctk.CTkLabel(app, text="System Command Center", font=ctk.CTkFont(size=14), text_color="gray")
subtitle_label.pack(pady=(0, 15))

# Section 1: Power Control
frame_engine = ctk.CTkFrame(app)
frame_engine.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_engine, text="1. Power Control", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_engine, text="▶ Boot System Engine", fg_color="#2b9348", hover_color="#007f5f", command=boot_system).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_engine, text="⏹ Shutdown Engine", fg_color="#d62828", hover_color="#9d0208", command=shutdown_system).pack(pady=5, padx=20, fill="x")

# Section 2: AI Workspaces
frame_dash = ctk.CTkFrame(app)
frame_dash.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_dash, text="2. AI Workspaces", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_dash, text="💬 Open WebUI (Main Chat)", command=open_webui).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_dash, text="⚙️ Open n8n (Automations)", command=open_n8n).pack(pady=5, padx=20, fill="x")

# Section 3: System Management (NEW)
frame_sys = ctk.CTkFrame(app)
frame_sys.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_sys, text="3. Infrastructure Management", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_sys, text="📦 Dockge (Visual Docker Manager)", fg_color="#f59f00", hover_color="#e67700", text_color="black", command=open_dockge).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_sys, text="🧠 Qdrant (Vector Database)", fg_color="#1d3557", hover_color="#457b9d", command=open_qdrant).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_sys, text="🚦 LiteLLM (Gateway & Tokens)", fg_color="#1d3557", hover_color="#457b9d", command=open_litellm).pack(pady=5, padx=20, fill="x")

# Section 4: Sandboxes
frame_dev = ctk.CTkFrame(app)
frame_dev.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_dev, text="4. Development Sandboxes", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_dev, text="💻 Windows Sandbox (Python)", fg_color="#5c677d", hover_color="#33415c", command=launch_agent_terminal).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_dev, text="🛡️ Linux Sandbox (WSL)", fg_color="#5c677d", hover_color="#33415c", command=launch_nemoclaw).pack(pady=5, padx=20, fill="x")

app.mainloop()