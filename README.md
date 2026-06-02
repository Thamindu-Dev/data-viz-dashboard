# AgenticOS - Hermes System Intelligence Dashboard 🚀

A real-time, high-performance system monitoring dashboard built as a custom plugin for the **Hermes Agent**. 

This plugin features a breakthrough **reverse-engineered Frontend UI integration**, allowing a custom React-based dashboard to be natively injected into the Hermes Gateway sidebar—a feature entirely undocumented in the official Hermes developer guides.

Built by **ZynthLab** • *Build. Scale. Secure.*

---

## ✨ Features

* **Native Sidebar Integration:** Seamlessly injects a custom "DATA VIZ DASHBOARD" tab directly into the Hermes Agent UI.
* **Real-time Metrics:** Live tracking of CPU load, Memory usage, and Disk storage.
* **Integrated Terminal:** A dedicated live stream terminal interface for direct system access.
* **Slash Command Support:** Type `/dashboard` in any Hermes chat session to retrieve a quick access link.
* **Isolated Backend:** Runs a dedicated Python (Flask) backend on port `5000` to serve the UI and metrics independently.

---

## 🏗️ The Undocumented UI Architecture

The official Hermes documentation only details Python-based backend plugins. However, this repository demonstrates the **undocumented method** for building native Frontend UI plugins. 

If you are building your own Hermes UI plugins, your structure **must** follow this exact pattern:

```text
data-viz-dashboard/
├── plugin.yaml                 # Standard backend manifest
├── __init__.py                 # Slash command & backend registration
├── backend/                    # Your Python backend (Flask/FastAPI)
└── dashboard/                  # MUST be named exactly 'dashboard'
    ├── manifest.json           # The Frontend Manifest (Not plugin.yaml)
    └── dist/
        └── index.js            # Compiled React component
```

### Key Frontend Requirements:

1. **The `manifest.json`:** Must reside in the `dashboard/` directory and use the `tab` and `entry` schema:

    ```json
    {
      "name": "data-viz-dashboard",
      "label": "Data Viz Dashboard",
      "icon": "chart-bar",
      "tab": { "path": "/data-viz-dashboard" },
      "entry": "dist/index.js"
    }
    ```
2. **JS Registration:** The `index.js` file must register the UI using the global Hermes Plugins object, not the standard SDK export:
    ```javascript
    window.__HERMES_PLUGINS__.register("data-viz-dashboard", YourComponent);
    ```

---

## 🚀 Installation & Setup

**1. Clone the repository into your Hermes plugins directory:**
```bash
git clone https://github.com/your-username/data-viz-dashboard.git /opt/data/home/.hermes/plugins/data-viz-dashboard
```

**2. Setup the Python Backend:**

```bash
cd /opt/data/home/.hermes/plugins/data-viz-dashboard/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Start the Backend Server:**
Ensure the background service is running on port 5000:

```bash
nohup /opt/data/home/.hermes/plugins/data-viz-dashboard/backend/venv/bin/python3 server.py &
```

**4. Restart Hermes Gateway:**
Restart your Hermes Docker container or gateway service to allow it to discover the new `dashboard/manifest.json`:

```bash
/opt/hermes/bin/hermes restart
```

---

## 🎮 Usage

There are two ways to access the AgenticOS Dashboard:

1. **Native UI Tab:** Open the Hermes Agent web interface and click on **"DATA VIZ DASHBOARD"** in the left sidebar under the Plugins section.
2. **Slash Command:** In any active Hermes chat session, type:

    ```text
    /dashboard
    ```

The agent will return a direct, clickable URL to the dashboard.

---

## 🛡️ License & Credits

Developed by **Thamindu Hatharasinghe** at [ZynthLab](https://zynthlab.com).
Reverse-engineered for the community. Feel free to fork, build upon, and explore the hidden capabilities of the Hermes framework!
