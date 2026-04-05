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

# --- Core Engine Logic ---
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
            return "OFFLINE 🔴", f"[{timestamp}] [SUCCESS] NemoClaw Sandbox Stopped."
        else:
            subprocess.run(["wsl", "-d", WSL_DISTRO, "echo", "Booting"], creationflags=subprocess.CREATE_NO_WINDOW)
            return "ONLINE 🟢", f"[{timestamp}] [SUCCESS] NemoClaw Sandbox Started."
    except Exception as e:
        return "ERROR ⚠️", f"Error: {str(e)}"

# --- Dynamic Agent Launcher ---
def deploy_agent(mode_choice):
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    if mode_choice == "🎯 Specialist Team":
        script_name = "mode_specialist.py"
    elif mode_choice == "👔 Manager Router":
        script_name = "mode_manager.py"
    elif mode_choice == "🌌 Ultimate (God Mode)":
        script_name = "mode_ultimate.py"
    else:
        return f"[{timestamp}] [ERROR] No valid agent mode selected."

    os.system(f'start wsl -d {WSL_DISTRO} -e bash -c "cd \'{INSTALL_PATH}/Agents\' && source venv/bin/activate && python {script_name}; exec bash"')
    return f"[{timestamp}] [SUCCESS] Deployed {mode_choice} on Host PC monitor."

# --- Modern Web GUI Layout ---
with gr.Blocks() as app:
    # Centered Custom App Header
    gr.HTML("<h1 style='text-align: center; margin-bottom: 0px;'>🚀 Big-Jay AI-OS</h1>")
    gr.HTML(f"<p style='text-align: center; color: #888; margin-top: 5px;'>Remote Gateway: http://{LOCAL_IP}:7860</p>")
    
    # Global Status
    with gr.Row():
        wsl_status = gr.Label(value=get_wsl_status, label="NemoClaw Environment Status", scale=1)

    # 1. Power Controls (Always Visible)
    with gr.Accordion("⚙️ Core Engine Power", open=True):
        with gr.Row():
            boot_btn = gr.Button("▶ Boot Engines", variant="primary")
            stop_btn = gr.Button("⏹ Shutdown Engines", variant="stop")
        update_btn = gr.Button("🔄 Check for System Updates")

    # 2. Agent Launchpad (Always Visible, Dynamic Dropdown)
    with gr.Accordion("🤖 Agent Execution Launchpad", open=True):
        gr.Markdown("Select the required agent architecture below to deploy it securely on your Host PC.")
        with gr.Row():
            agent_dropdown = gr.Dropdown(
                choices=["🎯 Specialist Team", "👔 Manager Router", "🌌 Ultimate (God Mode)"],
                label="AI Architecture Mode",
                value="🌌 Ultimate (God Mode)", # Default selection
                interactive=True,
                scale=2
            )
            launch_btn = gr.Button("🚀 Deploy Agents", variant="primary", scale=1)

    # 3. Quick Links (Collapsed by Default to save space)
    with gr.Accordion("🌐 Workspaces & Infrastructure", open=False):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🎨 Visual Workspaces")
                gr.Markdown(f"- [💬 Main Chat (WebUI)](http://{LOCAL_IP}:3000)")
                gr.Markdown(f"- [⚙️ Automations (n8n)](http://{LOCAL_IP}:5678)")
                gr.Markdown(f"- [🎨 Agent Studio (Langflow)](http://{LOCAL_IP}:7861)")
            with gr.Column():
                gr.Markdown("### 🖧 System Infrastructure")
                gr.Markdown(f"- [📦 Docker Manager (Dockge)](http://{LOCAL_IP}:5001)")
                gr.Markdown(f"- [🧠 Vector Database (Qdrant)](http://{LOCAL_IP}:6333/dashboard)")
                gr.Markdown(f"- [🚦 API Gateway (LiteLLM)](http://{LOCAL_IP}:4005)")

    # 4. Sandbox Controls (Collapsed by Default)
    with gr.Accordion("🛡️ Advanced Sandbox Controls", open=False):
        gr.Markdown("Manually power the NemoClaw subsystem on or off to manage RAM usage.")
        wsl_btn = gr.Button("⚡ Toggle NemoClaw Engine Power")

    # 5. Output Console
    gr.Markdown("---")
    console_output = gr.Textbox(label="System Output Log", lines=4, interactive=False, placeholder="Awaiting command...")

    # --- Wire up the buttons ---
    boot_btn.click(fn=boot_system, outputs=console_output)
    stop_btn.click(fn=shutdown_system, outputs=console_output)
    update_btn.click(fn=update_system, outputs=console_output)
    wsl_btn.click(fn=toggle_nemoclaw, outputs=[wsl_status, console_output])
    
    # Wire up the new dynamic dropdown launcher
    launch_btn.click(fn=deploy_agent, inputs=[agent_dropdown], outputs=console_output)

if __name__ == "__main__":
    # Launch with the sleek Soft theme
    app.launch(server_name="0.0.0.0", server_port=7860, quiet=True, theme=gr.themes.Soft(primary_hue="indigo"))