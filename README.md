# AgenticOS - Hermes System Intelligence Dashboard 🚀

A real-time, high-performance system monitoring dashboard built as a production-grade plugin for the **Hermes Agent**. 

This plugin demonstrates **Advanced Native UI Integration**, seamlessly injecting a custom React-based frontend into the Hermes Gateway sidebar—extending the framework beyond its standard capabilities by bridging backend AI with real-time frontend observability.

**Built by ZynthLab** • *Build. Scale. Secure.*

---

## ✨ Features

- **Native Sidebar Integration:** Custom "DATA VIZ DASHBOARD" tab seamlessly embedded in the Hermes Agent UI
- **Real-time Metrics:** Live CPU load, Memory usage, and Disk storage monitoring with sub-second refresh rates
- **Slash Command Support:** Quick-access via `/dashboard` from any Hermes chat session
- **Isolated Backend Architecture:** Dedicated Python (Flask) microservice on port `5000` for independent scaling and fault isolation
- **Zero-Configuration Deployment:** Automated environment provisioning, dependency management, and service orchestration

---

## 🏗️ Architecture

This repository demonstrates an advanced pattern for integrating custom UI into Hermes by leveraging undocumented framework capabilities. Standard Hermes plugins focus on backend interactions; this implementation showcases native frontend integration.

### Directory Structure

```text
data-viz-dashboard/
├── plugin.yaml                 # Backend plugin manifest
├── __init__.py                 # Plugin registration & slash command handler
├── backend/                    # Python microservice (Flask/Gunicorn)
│   ├── requirements.txt        # Python dependencies
│   ├── server.py               # Flask application & metrics endpoints
│   └── venv/                   # Virtual environment
└── dashboard/                  # Frontend plugin entry point
    ├── manifest.json           # UI manifest for Hermes Gateway discovery
    └── dist/
        └── index.js            # Compiled React component bundle
```

### Key Implementation Details

**1. Frontend Manifest (`dashboard/manifest.json`)**

The Gateway discovers and loads frontend plugins via this manifest:

```json
{
  "name": "data-viz-dashboard",
  "label": "Data Viz Dashboard",
  "icon": "chart-bar",
  "tab": { "path": "/data-viz-dashboard" },
  "entry": "dist/index.js"
}
```

**2. Plugin Registration (`dashboard/dist/index.js`)**

The compiled React component registers itself with the global Gateway object:

```javascript
window.__HERMES_PLUGINS__.register("data-viz-dashboard", YourComponent);
```

This pattern enables native UI integration without modifying the core Hermes codebase.

---

## 🚀 Installation & Setup

### Option 1: Automated Installation (Recommended)

If your Hermes installation supports plugin management:

1. Navigate to **Plugins** section in the Hermes Agent UI
2. Select **Install from URL** or **Import**
3. Paste the repository URL:
   ```
   https://github.com/Thamindu-Dev/data-viz-dashboard
   ```
4. Click **Install** — the system will automatically handle environment setup, dependencies, and service startup

### Option 2: Manual Installation

**Clone to Hermes plugins directory:**

```bash
git clone https://github.com/Thamindu-Dev/data-viz-dashboard.git \
  /opt/data/home/.hermes/plugins/data-viz-dashboard
```

**Setup Python environment:**

```bash
cd /opt/data/home/.hermes/plugins/data-viz-dashboard/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Start the backend service:**

```bash
nohup /opt/data/home/.hermes/plugins/data-viz-dashboard/backend/venv/bin/gunicorn \
  -b 0.0.0.0:5000 --threads 4 server:app > /tmp/dashboard.log 2>&1 &
```

**Restart Hermes Gateway:**

```bash
/opt/hermes/bin/hermes restart
```

The Gateway will discover `dashboard/manifest.json` and load the UI plugin automatically.

---

## 🎮 Usage

Access the AgenticOS Dashboard via two methods:

### 1. Native UI Tab
Open the Hermes Agent interface and click **"DATA VIZ DASHBOARD"** in the left sidebar under Plugins.

### 2. Slash Command
In any Hermes chat session, type:

```
/dashboard
```

The agent returns a direct URL to the dashboard interface.

---

## 🔧 Technical Stack

- **Backend:** Python 3.8+, Flask, Gunicorn
- **Frontend:** React 18+, TypeScript
- **Integration:** Hermes Agent Framework (custom plugin architecture)
- **Monitoring:** System metrics via psutil, real-time updates via WebSocket/REST

---

## 📝 License & Credits

**Developed by Thamindu Hatharasinghe** at [ZynthLab](https://zynthlab.com)

This project explores advanced integration patterns within the Hermes framework ecosystem. Feel free to fork, extend, and build upon these patterns for your own agent applications.

---

## 🤝 Contributing

Contributions are welcome! If you discover additional framework capabilities or optimization patterns, please open an issue or submit a pull request.

---

**Last Updated:** June 2026
