# Data Visualization Dashboard - Hermes Plugin 🎯

A production-ready system monitoring dashboard plugin that demonstrates how to integrate custom UI panels into the Hermes Agent gateway. This project serves as a reference implementation for building native frontend plugins for Hermes.

**Built by ZynthLab** • *Build. Scale. Secure.*

---

## 📸 Dashboard Preview

![Data Visualization Dashboard Screenshot](https://raw.githubusercontent.com/Thamindu-Dev/data-viz-dashboard/main/Screenshot.png)

---

## ✨ Features

- **Real-time Metrics Dashboard:** Live CPU load, Memory usage, and Disk storage visualization
- **Native UI Integration:** Custom dashboard tab seamlessly embedded in the Hermes Agent sidebar
- **Slash Command Access:** Quick-access via `/dashboard` from any Hermes chat session
- **Isolated Backend Microservice:** Dedicated Python (Flask) backend on port `5000` for metrics collection
- **Plugin Architecture Reference:** Complete working example of Hermes frontend plugin integration

---

## 📚 What This Project Demonstrates

This repository is a **reference implementation** showing how to add a custom dashboard entry to the Hermes plugin system. It covers:

1. **Frontend UI Integration** - How to inject React components into the Hermes gateway sidebar
2. **Plugin Manifest Configuration** - Proper structure for Hermes to discover and load UI plugins
3. **Backend-Frontend Communication** - Connecting a Flask microservice to real-time dashboard data
4. **Plugin Registration** - Registering custom components with the Hermes plugin registry

---

## 🏗️ Architecture

### Directory Structure

```text
data-viz-dashboard/
├── plugin.yaml                 # Hermes plugin manifest (backend registration)
├── __init__.py                 # Plugin initialization & slash command handler
├── backend/                    # Flask microservice for metrics
│   ├── requirements.txt        # Python dependencies
│   ├── server.py               # Flask app serving system metrics
│   └── venv/                   # Virtual environment
└── dashboard/                  # Frontend plugin entry point
    ├── manifest.json           # UI plugin manifest (Hermes gateway discovery)
    └── dist/
        └── index.js            # Compiled React dashboard component
```

### Plugin Registration Flow

```
Hermes Gateway
    ↓
Discovers dashboard/manifest.json
    ↓
Loads dist/index.js
    ↓
Registers component via window.__HERMES_PLUGINS__.register()
    ↓
Dashboard appears in sidebar under Plugins section
```

---

## 🔧 Key Implementation Files

### 1. Frontend Manifest (`dashboard/manifest.json`)

This file tells Hermes Gateway how to discover and load your UI plugin:

```json
{
  "name": "data-viz-dashboard",
  "label": "Data Viz Dashboard",
  "icon": "chart-bar",
  "tab": { "path": "/data-viz-dashboard" },
  "entry": "dist/index.js"
}
```

**Required fields:**
- `name` - Unique plugin identifier
- `label` - Display name in the UI
- `icon` - Icon identifier for the sidebar tab
- `tab.path` - Route path for the dashboard
- `entry` - Path to compiled React component

### 2. Plugin Registration (`dashboard/dist/index.js`)

The React component must register itself with the global Hermes plugin registry:

```javascript
window.__HERMES_PLUGINS__.register("data-viz-dashboard", YourComponent);
```

This allows Hermes to dynamically load and render your component.

### 3. Backend Integration (`backend/server.py`)

Flask microservice providing real-time metrics:

```python
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    return jsonify({
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    })
```

---

## 🚀 Installation & Setup

### Quick Start

**1. Clone to your Hermes plugins directory:**

```bash
git clone https://github.com/Thamindu-Dev/data-viz-dashboard.git \
  /opt/data/home/.hermes/plugins/data-viz-dashboard
```

**2. Setup Python backend:**

```bash
cd /opt/data/home/.hermes/plugins/data-viz-dashboard/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Start the metrics backend:**

```bash
nohup /opt/data/home/.hermes/plugins/data-viz-dashboard/backend/venv/bin/gunicorn \
  -b 0.0.0.0:5000 --threads 4 server:app > /tmp/dashboard.log 2>&1 &
```

**4. Restart Hermes Gateway:**

```bash
/opt/hermes/bin/hermes restart
```

The gateway will automatically discover and load `dashboard/manifest.json`.

---

## 🎮 Usage

Once installed, access your dashboard through:

### 1. Sidebar Plugin Tab
Open Hermes Agent and click **"Data Viz Dashboard"** in the left sidebar under Plugins.

### 2. Slash Command
In any Hermes chat session:

```
/dashboard
```

Returns a direct link to your dashboard.

---

## 📖 Learning Guide

This project is structured as a learning resource. Key sections to study:

1. **`dashboard/manifest.json`** - Understand plugin discovery mechanism
2. **`dashboard/dist/index.js`** - See React component registration pattern
3. **`backend/server.py`** - Review metrics endpoint implementation
4. **`plugin.yaml`** - Study Hermes backend plugin configuration

Use this as a template when building your own Hermes UI plugins.

---

## 🔧 Technical Stack

- **Backend:** Python 3.8+, Flask, Gunicorn
- **Frontend:** React 18+, TypeScript
- **Metrics:** psutil for system monitoring
- **Integration:** Hermes Plugin Architecture

---

## 🛠️ Building Your Own Plugin

To create a similar plugin:

1. Copy the `dashboard/` folder structure
2. Update `manifest.json` with your plugin name
3. Build your React component and export to `dist/index.js`
4. Register with `window.__HERMES_PLUGINS__.register()`
5. Create corresponding backend in `backend/`
6. Add `plugin.yaml` for Hermes backend registration

---

## 📝 License & Credits

**Developed by Thamindu Hatharasinghe** at [ZynthLab](https://zynthlab.com)

This reference implementation demonstrates Hermes plugin architecture patterns. Use it as a foundation for your own custom dashboard integrations.

---

## 🤝 Contributing

Found a better way to integrate plugins? Contributions welcome!

- Open an issue to discuss improvements
- Submit PRs with enhancements
- Share additional plugin architecture patterns

---

**Last Updated:** June 2026
