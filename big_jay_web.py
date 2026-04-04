import gradio as gr
import os
import subprocess
import socket
from datetime import datetime

INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))

# Auto-detect your PC's local IP address on the Wi-Fi network
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
        # 0x08000000 is the Windows flag to hide terminal popups
        result = subprocess.run(command_list, cwd=INSTALL_PATH, capture_output=True, text=True, creationflags=0x08000000)
        if result.returncode == 0:
            log += f"[{timestamp}] [SUCCESS] {success_msg}"
        else:
            log += f"[{timestamp}] [ERROR] {error_msg}\nDetails: {result.stderr.strip()}"
    except Exception as e:
        log += f"[{timestamp}] [ERROR] System Error: {str(e)}"
    return log

def boot_system():
    return run_command(["docker", "compose", "-p", "big-jay", "up", "-d"], "Booting Docker engines...", "All engines are online and ready!", "Boot failed.")

def shutdown_system():
    return run_command(["docker", "compose", "-p", "big-jay", "down"], "Shutting down engines...", "System successfully powered off.", "Shutdown failed.")

def update_system():
    return run_command(["git", "pull"], "Checking GitHub for updates...", "System updated! Please refresh this page.", "Update failed.")

# --- Build the Web GUI ---
with gr.Blocks(theme=gr.themes.Soft(), title="Big-Jay OS") as app:
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
            
            # Link buttons to functions
            boot_btn.click(fn=boot_system, outputs=console_output)
            stop_btn.click(fn=shutdown_system, outputs=console_output)
            update_btn.click(fn=update_system, outputs=console_output)
            
        # Right Column: Network Links
        with gr.Column(scale=1):
            gr.Markdown("### 2. AI Workspaces")
            gr.Markdown(f"*(Clicking these on your phone will open them in your phone's browser)*")
            gr.Markdown(f"- [💬 Open WebUI (Main Chat)](http://{LOCAL_IP}:3000)")
            gr.Markdown(f"- [⚙️ Open n8n (Automations)](http://{LOCAL_IP}:5678)")
            
            gr.Markdown("### 3. Infrastructure Management")
            gr.Markdown(f"- [📦 Dockge (Visual Docker Manager)](http://{LOCAL_IP}:5001)")
            gr.Markdown(f"- [🧠 Qdrant (Vector Database)](http://{LOCAL_IP}:6333/dashboard)")
            gr.Markdown(f"- [🚦 LiteLLM (Gateway & Tokens)](http://{LOCAL_IP}:4005)")

            gr.Markdown("---")
            gr.Markdown("*Note: Windows and Linux Sandboxes are local development environments and must be launched natively from the host PC terminal.*")

# Broadcast to the local network on port 7860
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, quiet=True)