import gradio as gr
import os
import subprocess
import socket
from datetime import datetime

INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))
WSL_DISTRO = "Ubuntu"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()

def run_command(command_list, start_msg, success_msg, error_msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log = f"[{timestamp}] [INFO] {start_msg}\n"
    try:
        result = subprocess.run(command_list, cwd=INSTALL_PATH, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode == 0: log += f"[{timestamp}] [SUCCESS] {success_msg}"
        else: log += f"[{timestamp}] [ERROR] {error_msg}\nDetails: {result.stderr.strip()}"
    except Exception as e:
        log += f"[{timestamp}] [ERROR] System Error: {str(e)}"
    return log

def boot_system(): return run_command(["docker", "compose", "-p", "big-jay", "up", "-d"], "Booting Docker engines...", "All engines online!", "Boot failed.")
def shutdown_system(): return run_command(["docker", "compose", "-p", "big-jay", "down"], "Shutting down engines...", "System powered off.", "Shutdown failed.")
def update_system(): return run_command(["git", "pull"], "Checking GitHub...", "System updated! Please refresh.", "Update failed.")

# --- WSL NemoClaw Logic ---
def get_wsl_status():
    try:
        output = subprocess.check_output(["wsl", "-l", "-v"], text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if WSL_DISTRO in output and "Running" in output: return "ONLINE 🟢"
        return "OFFLINE 🔴"
    except: return "ERROR ⚠️"

def toggle_nemoclaw():
    try:
        status = get_wsl_status()
        timestamp = datetime.now().strftime("%H:%M:%S")
        if "ONLINE" in status:
            subprocess.run(["wsl", "--terminate", WSL_DISTRO], creationflags=subprocess.CREATE_NO_WINDOW)
            log = f"[{timestamp}] [SUCCESS] NemoClaw Sandbox Stopped."
            return "OFFLINE 🔴", log
        else:
            subprocess.run(["wsl", "-d", WSL_DISTRO, "echo", "Booting"], creationflags=subprocess.CREATE_NO_WINDOW)
            log = f"[{timestamp}] [SUCCESS] NemoClaw Sandbox Started."
            return "ONLINE 🟢", log
    except Exception as e:
        return "ERROR ⚠️", f"Error: {str(e)}"

# --- Web GUI Layout ---
with gr.Blocks() as app:
    gr.Markdown(f"# 🚀 Big-Jay AI-OS Command Center")
    gr.Markdown(f"**Network Status:** Active 🟢 | **Access this page from your phone at:** `http://{LOCAL_IP}:7860`")
    
    with gr.Row():
        # Left Column: Controls
        with gr.Column(scale=1):
            gr.Markdown("### 1. Power & Updates")
            boot_btn = gr.Button("▶ Boot System Engine", variant="primary")
            stop_btn = gr.Button("⏹ Shutdown Engine", variant="stop")
            update_btn = gr.Button("🔄 Check for Updates (GitHub)")
            
            gr.Markdown("### System Log")
            console_output = gr.Textbox(label="", lines=5, interactive=False, placeholder="Awaiting command...")
            
            boot_btn.click(fn=boot_system, outputs=console_output)
            stop_btn.click(fn=shutdown_system, outputs=console_output)
            update_btn.click(fn=update_system, outputs=console_output)
            
        # Right Column: Network Links & Sandboxes
        with gr.Column(scale=1):
            gr.Markdown("### 2. AI Workspaces")
            gr.Markdown(f"*(Clicking these links will open them in your current browser)*")
            gr.Markdown(f"- [💬 Open WebUI (Main Chat)](http://{LOCAL_IP}:3000)")
            gr.Markdown(f"- [⚙️ Open n8n (Automations)](http://{LOCAL_IP}:5678)")
            gr.Markdown(f"- [🎨 Open Agent Studio](http://{LOCAL_IP}:7861)")
            
            gr.Markdown("### 3. Infrastructure")
            gr.Markdown(f"- [📦 Dockge (Visual Docker Manager)](http://{LOCAL_IP}:5001)")
            gr.Markdown(f"- [🧠 Qdrant (Vector Database)](http://{LOCAL_IP}:6333/dashboard)")
            gr.Markdown(f"- [🚦 LiteLLM (Gateway & Tokens)](http://{LOCAL_IP}:4005)")

            gr.Markdown("### 4. Security Sandboxes")
            with gr.Row():
                # Fetch initial status on load
                wsl_status = gr.Label(value=get_wsl_status, label="NemoClaw WSL Status", scale=1)
                wsl_btn = gr.Button("⚡ Toggle Engine", scale=1)
            
            wsl_btn.click(fn=toggle_nemoclaw, outputs=[wsl_status, console_output])

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, quiet=True, theme=gr.themes.Soft())