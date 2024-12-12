import os
import shutil
from typing import Any, Callable, Dict, List


def get_inner_vscode_cmd() -> List[str]:
    return [
        "code-server",
        "--auth",
        "none",
        "--disable-telemetry",
        "--disable-update-check",
        "--disable-workspace-trust",
        "--disable-getting-started-override",
        "--disable-proxy",
    ]

def _get_cmd_factory() -> Callable:

    def _get_cmd(port: int) -> List[str]:
        if not shutil.which("code-server"):
            raise FileNotFoundError(f"Can not find code-server in PATH")

        # Start vscode in CODE_WORKINGDIR env variable if set
        # If not, start in 'current directory', which is $REPO_DIR in mybinder
        # but /home/jovyan (or equivalent) in JupyterHubs
        working_dir = os.getenv("CODE_WORKINGDIR", ".")

        # Customize where extensions are installed 
        extensions_dir = os.getenv("CODE_EXTENSIONSDIR", None)

        os.makedirs(extensions_dir, exist_ok=True)

        # Customize path to self-signed cert and key
        cert = os.getenv("CODE_CERT", None)
        cert_key = os.getenv("CODE_CERT_KEY", None)

        # Customize verbosity
        verbose = os.getenv("CODE_VERBOSE", None)

        cmd = get_inner_vscode_cmd()

        cmd.append("--port=" + str(port))

        if extensions_dir:
            cmd += ["--extensions-dir", extensions_dir]

        if cert and cert_key:
            cmd += ["--cert", cert, "--cert-key", cert_key]

        if verbose:
            cmd += ["--verbose"]

        cmd.append(working_dir)
        return cmd

    return _get_cmd


def setup_vscode() -> Dict[str, Any]:
    return {
        "command": _get_cmd_factory(),
        "timeout": 300,
        "new_browser_tab": True,
        "launcher_entry": {
            "title": "VS Code",
            "icon_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "icons", "vscode.svg"
            ),
        },
    }
