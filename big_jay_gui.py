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
app.geometry("880x680") # Transformed into a wide dashboard layout
app.title("Big-Jay AI-OS Command Center")
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
def run_specialists(): os.system(f'start wsl -d {WSL_DISTRO} -e bash -c "cd \'{INSTALL_PATH}/Agents\' && source venv/bin/activate && python mode_specialist.py; exec bash"')
def run_manager(): os.system(f'start wsl -d {WSL_DISTRO} -e bash -c "cd \'{INSTALL_PATH}/Agents\' && source venv/bin/activate && python mode_manager.py; exec bash"')
def run_ultimate(): os.system(f'start wsl -d {WSL_DISTRO} -e bash -c "cd \'{INSTALL_PATH}/Agents\' && source venv/bin/activate && python mode_ultimate.py; exec bash"')

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
    app.after(5000, update_status_ui) 

# --- GUI Layout ---
title_label = ctk.CTkLabel(app, text="🚀 Big-Jay AI-OS Command Center", font=ctk.CTkFont(size=26, weight="bold"))
title_label.pack(pady=(15, 10))

# Main container for Two-Column Layout
content_frame = ctk.CTkFrame(app, fg_color="transparent")
content_frame.pack(fill="both", expand=True, padx=20)
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(1, weight=1)

# ==================== LEFT COLUMN ====================
left_col = ctk.CTkFrame(content_frame, fg_color="transparent")
left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

# 1. Power & Updates
frame_engine = ctk.CTkFrame(left_col)
frame_engine.pack(pady=(0, 15), fill="x")
ctk.CTkLabel(frame_engine, text="1. Power & Updates", font=ctk.CTkFont(weight="bold")).pack(pady=5)

power_btn_frame = ctk.CTkFrame(frame_engine, fg_color="transparent")
power_btn_frame.pack(fill="x", padx=15, pady=5)
power_btn_frame.grid_columnconfigure((0,1), weight=1)
ctk.CTkButton(power_btn_frame, text="▶ Boot System", fg_color="#2b9348", hover_color="#007f5f", command=boot_system).grid(row=0, column=0, padx=(0,5), sticky="ew")
ctk.CTkButton(power_btn_frame, text="⏹ Shutdown", fg_color="#d62828", hover_color="#9d0208", command=shutdown_system).grid(row=0, column=1, padx=(5,0), sticky="ew")
ctk.CTkButton(frame_engine, text="🔄 Check for Updates", fg_color="#f59f00", hover_color="#e67700", text_color="black", command=update_system).pack(pady=(0, 15), padx=15, fill="x")

# 2. AI Workspaces
frame_dash = ctk.CTkFrame(left_col)
frame_dash.pack(pady=(0, 15), fill="x")
ctk.CTkLabel(frame_dash, text="2. AI Workspaces", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_dash, text="💬 Open WebUI (Main Chat)", command=open_webui).pack(pady=5, padx=15, fill="x")
ctk.CTkButton(frame_dash, text="⚙️ Open n8n (Automations)", command=open_n8n).pack(pady=5, padx=15, fill="x")
ctk.CTkButton(frame_dash, text="🎨 Open Agent Studio (Langflow)", command=open_studio).pack(pady=(5, 15), padx=15, fill="x")

# 3. Infrastructure
frame_sys = ctk.CTkFrame(left_col)
frame_sys.pack(fill="x")
ctk.CTkLabel(frame_sys, text="3. Infrastructure Management", font=ctk.CTkFont(weight="bold")).pack(pady=5)

sys_btn_frame = ctk.CTkFrame(frame_sys, fg_color="transparent")
sys_btn_frame.pack(fill="x", padx=15, pady=5)
sys_btn_frame.grid_columnconfigure((0,1), weight=1)
ctk.CTkButton(sys_btn_frame, text="📦 Dockge", fg_color="#1d3557", hover_color="#457b9d", command=open_dockge).grid(row=0, column=0, padx=(0,5), pady=5, sticky="ew")
ctk.CTkButton(sys_btn_frame, text="🧠 Qdrant", fg_color="#1d3557", hover_color="#457b9d", command=open_qdrant).grid(row=0, column=1, padx=(5,0), pady=5, sticky="ew")
ctk.CTkButton(sys_btn_frame, text="🚦 LiteLLM (Gateway)", fg_color="#1d3557", hover_color="#457b9d", command=open_litellm).grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

# ==================== RIGHT COLUMN ====================
right_col = ctk.CTkFrame(content_frame, fg_color="transparent")
right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

# 4. Sandboxes
frame_dev = ctk.CTkFrame(right_col)
frame_dev.pack(pady=(0, 15), fill="x")
ctk.CTkLabel(frame_dev, text="4. Security Sandboxes", font=ctk.CTkFont(weight="bold")).pack(pady=5)

status_row = ctk.CTkFrame(frame_dev, fg_color="#151515", corner_radius=8)
status_row.pack(fill="x", padx=15, pady=5)
ctk.CTkLabel(status_row, text="NemoClaw Status:").pack(side="left", padx=10, pady=5)
status_indicator = ctk.CTkLabel(status_row, text="CHECKING...", text_color="yellow", font=ctk.CTkFont(weight="bold"))
status_indicator.pack(side="right", padx=10, pady=5)

ctk.CTkButton(frame_dev, text="⚡ Toggle NemoClaw Engine", command=toggle_wsl).pack(pady=10, padx=15, fill="x")

term_btn_frame = ctk.CTkFrame(frame_dev, fg_color="transparent")
term_btn_frame.pack(fill="x", padx=15, pady=(0, 15))
term_btn_frame.grid_columnconfigure((0,1), weight=1)
ctk.CTkButton(term_btn_frame, text="💻 Win Sandbox", fg_color="#5c677d", hover_color="#33415c", command=launch_agent_terminal).grid(row=0, column=0, padx=(0,5), sticky="ew")
ctk.CTkButton(term_btn_frame, text="🛡️ Linux Term", fg_color="#5c677d", hover_color="#33415c", command=launch_nemoclaw).grid(row=0, column=1, padx=(5,0), sticky="ew")

# 5. Agent Launchpad
frame_launch = ctk.CTkFrame(right_col)
frame_launch.pack(fill="x")
ctk.CTkLabel(frame_launch, text="5. Agent Launchpad", font=ctk.CTkFont(weight="bold")).pack(pady=5)
ctk.CTkButton(frame_launch, text="🎯 Run Specialist Team", height=38, fg_color="#457b9d", hover_color="#1d3557", command=run_specialists).pack(pady=5, padx=15, fill="x")
ctk.CTkButton(frame_launch, text="👔 Run Manager Router", height=38, fg_color="#457b9d", hover_color="#1d3557", command=run_manager).pack(pady=5, padx=15, fill="x")
ctk.CTkButton(frame_launch, text="🌌 Run Ultimate (God Mode)", height=45, font=ctk.CTkFont(weight="bold"), fg_color="#8338ec", hover_color="#3a0ca3", command=run_ultimate).pack(pady=(5, 15), padx=15, fill="x")

# ==================== BOTTOM SPAN ====================
# Console Log
console_frame = ctk.CTkFrame(app)
console_frame.pack(pady=(15, 20), padx=20, fill="both", expand=True)
ctk.CTkLabel(console_frame, text="System Output Log", font=ctk.CTkFont(weight="bold", size=12)).pack(anchor="w", padx=10, pady=(5,0))
console = ctk.CTkTextbox(console_frame, height=100, state="disabled", fg_color="#0a0a0a", text_color="#00ff00", font=ctk.CTkFont(family="Consolas", size=12))
console.pack(pady=(0, 10), padx=10, fill="both", expand=True)

log_message("Big-Jay OS Dashboard Initialized.", "success")
app.after(500, update_status_ui)
app.mainloop()