import threading
import logging
from flask import Flask
from flask_cors import CORS
from telemetry import watchdog_loop
from api import api_bp

def create_app():
    # Setup Flask
    app = Flask(__name__, static_folder='../dashboard/dist', static_url_path='/')
    CORS(app)
    
    # Register HTTP Routes (API, static files, ttyd proxy)
    app.register_blueprint(api_bp)

    return app

# Expose app globally for WSGI servers like Gunicorn
app = create_app()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

# Start the watchdog
threading.Thread(target=watchdog_loop, daemon=True).start()

if __name__ == '__main__':
    
    app.logger.info("[data-viz-dashboard] Server starting on 0.0.0.0:5000 (Local Development Mode)")
    app.run(host='0.0.0.0', port=5000, threaded=True)
