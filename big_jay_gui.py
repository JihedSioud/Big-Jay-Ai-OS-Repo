import customtkinter as ctk
import os
import subprocess
import webbrowser
import threading
from datetime import datetime

INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))
WSL_DISTRO = "Ubuntu"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("420x900") # Slightly taller to fit the new NemoClaw row
app.title("🚀 Big-Jay AI-OS Command Center")
app.resizable(False, False)

# --- Logic & Engine Controls ---
def log_message(msg, level="info"):
    console.configure(state="normal")
    timestamp = datetime.now().strftime("%H:%M:%S")
    if level == "error": prefix = "[ERROR]"
    elif level == "success": prefix = "[SUCCESS]"
    elif level == "warning": prefix = "[UPDATE]"
    else: prefix = "[INFO]"
    console.insert("end", f"{timestamp} {prefix} {msg}\n")
    console.see("end")
    console.configure(state="disabled")

def run_async_command(command_list, start_msg, success_msg, error_msg, level="success"):
    log_message(start_msg)
    def task():
        try:
            result = subprocess.run(command_list, cwd=INSTALL_PATH, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
                app.after(0, log_message, success_msg, level)
            else:
                app.after(0, log_message, f"{error_msg}: {result.stderr.strip()}", "error")
        except Exception as e:
            app.after(0, log_message, f"System Error: {str(e)}", "error")
    threading.Thread(target=task, daemon=True).start()

def boot_system(): run_async_command(["docker", "compose", "-p", "big-jay", "up", "-d"], "Booting Docker engines...", "Engines online!", "success")
def shutdown_system(): run_async_command(["docker", "compose", "-p", "big-jay", "down"], "Shutting down engines...", "System powered off.", "success")
def update_system(): run_async_command(["git", "pull"], "Checking GitHub...", "System updated!", "warning")

def open_webui(): webbrowser.open("http://localhost:3000")
def open_n8n(): webbrowser.open("http://localhost:5678")
def open_dockge(): webbrowser.open("http://localhost:5001")
def open_litellm(): webbrowser.open("http://localhost:4005") 
def open_qdrant(): webbrowser.open("http://localhost:6333/dashboard")
def open_studio(): webbrowser.open("http://localhost:7861")

def launch_agent_terminal(): os.system(f'start powershell -NoExit -Command "cd \'{INSTALL_PATH}\\Agents\'; .\\venv\\Scripts\\activate"')
def launch_nemoclaw(): os.system('start wsl')

# --- WSL NemoClaw Logic ---
def get_wsl_status():
    try:
        output = subprocess.check_output(["wsl", "-l", "-v"], text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if WSL_DISTRO in output and "Running" in output:
            return "ONLINE 🟢", "#2b9348"
        return "OFFLINE 🔴", "#d62828"
    except:
        return "ERROR ⚠️", "orange"

def toggle_wsl():
    status, _ = get_wsl_status()
    if "ONLINE" in status:
        log_message(f"Terminating NemoClaw Sandbox...")
        subprocess.run(["wsl", "--terminate", WSL_DISTRO], creationflags=subprocess.CREATE_NO_WINDOW)
        log_message("Sandbox Powered Down.", "success")
    else:
        log_message(f"Starting NemoClaw Sandbox...")
        subprocess.run(["wsl", "-d", WSL_DISTRO, "echo", "Booting"], creationflags=subprocess.CREATE_NO_WINDOW)
        log_message("Sandbox Online.", "success")
    update_status_ui()

def update_status_ui():
    stat_text, stat_color = get_wsl_status()
    status_indicator.configure(text=stat_text, text_color=stat_color)
    app.after(5000, update_status_ui) # Auto-refresh every 5 seconds

# --- GUI Layout ---
title_label = ctk.CTkLabel(app, text="Big-Jay AI-OS", font=ctk.CTkFont(size=26, weight="bold"))
title_label.pack(pady=(15, 0))

frame_engine = ctk.CTkFrame(app)
frame_engine.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_engine, text="1. Power & Updates", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_engine, text="▶ Boot System Engine", fg_color="#2b9348", hover_color="#007f5f", command=boot_system).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_engine, text="⏹ Shutdown Engine", fg_color="#d62828", hover_color="#9d0208", command=shutdown_system).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_engine, text="🔄 Check for Updates", fg_color="#f59f00", hover_color="#e67700", text_color="black", command=update_system).pack(pady=5, padx=20, fill="x")

frame_dash = ctk.CTkFrame(app)
frame_dash.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_dash, text="2. AI Workspaces", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_dash, text="💬 Open WebUI (Main Chat)", command=open_webui).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_dash, text="⚙️ Open n8n (Automations)", command=open_n8n).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_dash, text="🎨 Open Agent Studio (Langflow)", command=open_studio).pack(pady=5, padx=20, fill="x")

frame_sys = ctk.CTkFrame(app)
frame_sys.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_sys, text="3. Infrastructure Management", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_sys, text="📦 Dockge (Manager)", fg_color="#1d3557", hover_color="#457b9d", command=open_dockge).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_sys, text="🧠 Qdrant (Vector DB)", fg_color="#1d3557", hover_color="#457b9d", command=open_qdrant).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_sys, text="🚦 LiteLLM (Gateway)", fg_color="#1d3557", hover_color="#457b9d", command=open_litellm).pack(pady=5, padx=20, fill="x")

frame_dev = ctk.CTkFrame(app)
frame_dev.pack(pady=5, padx=20, fill="x")
ctk.CTkLabel(frame_dev, text="4. Security Sandboxes", font=ctk.CTkFont(weight="bold")).pack(pady=5)

status_row = ctk.CTkFrame(frame_dev, fg_color="transparent")
status_row.pack(fill="x", padx=10)
ctk.CTkLabel(status_row, text="NemoClaw Status:").pack(side="left", padx=5)
status_indicator = ctk.CTkLabel(status_row, text="CHECKING...", text_color="yellow", font=ctk.CTkFont(weight="bold"))
status_indicator.pack(side="left")

ctk.CTkButton(frame_dev, text="⚡ Toggle NemoClaw Engine", command=toggle_wsl).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_dev, text="💻 Windows Sandbox (Python)", fg_color="#5c677d", hover_color="#33415c", command=launch_agent_terminal).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(frame_dev, text="🛡️ Open Linux Terminal", fg_color="#5c677d", hover_color="#33415c", command=launch_nemoclaw).pack(pady=5, padx=20, fill="x")

console_frame = ctk.CTkFrame(app)
console_frame.pack(pady=10, padx=20, fill="both", expand=True)
console = ctk.CTkTextbox(console_frame, height=100, state="disabled", fg_color="#0a0a0a", text_color="#00ff00", font=ctk.CTkFont(family="Consolas", size=11))
console.pack(pady=5, padx=10, fill="both", expand=True)

log_message("Big-Jay OS Local Desktop Ready.", "success")
app.after(500, update_status_ui)
app.mainloop()