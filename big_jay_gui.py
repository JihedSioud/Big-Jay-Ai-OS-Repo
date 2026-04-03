import customtkinter as ctk
import os
import subprocess
import webbrowser
import threading
from datetime import datetime

INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("420x850") # Made taller to fit the console
app.title("🚀 Big-Jay AI-OS Command Center")
app.resizable(False, False)

# --- Console Logging System ---
def log_message(msg, level="info"):
    """Pushes a message to the GUI console safely from any thread."""
    console.configure(state="normal")
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Simple color coding based on message type
    if level == "error":
        prefix = "[ERROR]"
    elif level == "success":
        prefix = "[SUCCESS]"
    elif level == "warning":
        prefix = "[UPDATE]"
    else:
        prefix = "[INFO]"
        
    console.insert("end", f"{timestamp} {prefix} {msg}\n")
    console.see("end") # Auto-scroll to bottom
    console.configure(state="disabled")

def run_async_command(command_list, start_msg, success_msg, error_msg, level="success"):
    """Runs a terminal command in the background so the GUI doesn't freeze."""
    log_message(start_msg)
    
    def task():
        try:
            # Run the command and capture the output
            result = subprocess.run(command_list, cwd=INSTALL_PATH, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                # App.after forces the UI update to happen on the main thread to prevent crashes
                app.after(0, log_message, success_msg, level)
            else:
                app.after(0, log_message, f"{error_msg}: {result.stderr.strip()}", "error")
        except Exception as e:
            app.after(0, log_message, f"System Error: {str(e)}", "error")
            
    # Start the background thread
    threading.Thread(target=task, daemon=True).start()

# --- Core Functions ---
def boot_system():
    run_async_command(["docker", "compose", "-p", "big-jay", "up", "-d"], "Booting Docker engines...", "All engines are online and ready!", "success")

def shutdown_system():
    run_async_command(["docker", "compose", "-p", "big-jay", "down"], "Shutting down engines...", "System successfully powered off.", "success")

def update_system():
    run_async_command(["git", "pull"], "Checking GitHub for updates...", "System updated! Please restart this GUI.", "warning")

def open_webui(): 
    log_message("Opening Open WebUI...")
    webbrowser.open("http://localhost:3000")
def open_n8n(): 
    log_message("Opening n8n Automations...")
    webbrowser.open("http://localhost:5678")
def open_dockge(): 
    log_message("Opening Dockge Manager...")
    webbrowser.open("http://localhost:5001")
def open_litellm(): 
    log_message("Opening LiteLLM Gateway...")
    webbrowser.open("http://localhost:4000")
def open_qdrant(): 
    log_message("Opening Vector Database...")
    webbrowser.open("http://localhost:6333/dashboard")

def launch_agent_terminal(): 
    log_message("Launching Windows Python Sandbox...")
    os.system(f'start powershell -NoExit -Command "cd \'{INSTALL_PATH}\\Agents\'; .\\venv\\Scripts\\activate"')
def launch_nemoclaw(): 
    log_message("Launching Linux WSL Sandbox...")
    os.system('start wsl')

# --- Header ---
title_label = ctk.CTkLabel(app, text="Big-Jay AI-OS", font=ctk.CTkFont(size=26, weight="bold"))
title_label.pack(pady=(15, 0))
subtitle_label = ctk.CTkLabel(app, text="System Command Center", font=ctk.CTkFont(size=14), text_color="gray")
subtitle_label.pack(pady=(0, 10))

# Section 1: Power & Updates (NEW)
frame_engine = ctk.CTkFrame(app)
frame_engine.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_engine, text="1. Power & Updates", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_engine, text="▶ Boot System Engine", fg_color="#2b9348", hover_color="#007f5f", command=boot_system).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_engine, text="⏹ Shutdown Engine", fg_color="#d62828", hover_color="#9d0208", command=shutdown_system).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_engine, text="🔄 Check for Updates (GitHub)", fg_color="#f59f00", hover_color="#e67700", text_color="black", command=update_system).pack(pady=5, padx=20, fill="x")

# Section 2: AI Workspaces
frame_dash = ctk.CTkFrame(app)
frame_dash.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_dash, text="2. AI Workspaces", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_dash, text="💬 Open WebUI (Main Chat)", command=open_webui).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_dash, text="⚙️ Open n8n (Automations)", command=open_n8n).pack(pady=5, padx=20, fill="x")

# Section 3: Infrastructure Management
frame_sys = ctk.CTkFrame(app)
frame_sys.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_sys, text="3. Infrastructure Management", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_sys, text="📦 Dockge (Visual Docker Manager)", fg_color="#1d3557", hover_color="#457b9d", command=open_dockge).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_sys, text="🧠 Qdrant (Vector Database)", fg_color="#1d3557", hover_color="#457b9d", command=open_qdrant).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_sys, text="🚦 LiteLLM (Gateway & Tokens)", fg_color="#1d3557", hover_color="#457b9d", command=open_litellm).pack(pady=5, padx=20, fill="x")

# Section 4: Sandboxes
frame_dev = ctk.CTkFrame(app)
frame_dev.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_dev, text="4. Development Sandboxes", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_dev, text="💻 Windows Sandbox (Python)", fg_color="#5c677d", hover_color="#33415c", command=launch_agent_terminal).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_dev, text="🛡️ Linux Sandbox (WSL)", fg_color="#5c677d", hover_color="#33415c", command=launch_nemoclaw).pack(pady=5, padx=20, fill="x")

# --- Visual Notification Console (NEW) ---
console_frame = ctk.CTkFrame(app)
console_frame.pack(pady=10, padx=20, fill="both", expand=True)
ctk.CTkLabel(console_frame, text="System Log", font=ctk.CTkFont(weight="bold", size=12)).pack(pady=(5, 0))

# The actual text box (hacker-style green text on black)
console = ctk.CTkTextbox(console_frame, height=100, state="disabled", fg_color="#0a0a0a", text_color="#00ff00", font=ctk.CTkFont(family="Consolas", size=11))
console.pack(pady=5, padx=10, fill="both", expand=True)

# Initial boot message
log_message("Big-Jay AI-OS Initialized.", "success")
log_message("Awaiting command...")

app.mainloop()