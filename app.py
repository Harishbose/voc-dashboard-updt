from flask import Flask, render_template, send_file, jsonify
import pandas as pd
import os
import json

app = Flask(__name__, static_folder='static', template_folder='.')

# Load CSV data
def load_data():
    try:
        # Try multiple possible CSV file names
        csv_files = ['latest_t_mapped_clean.csv', 'latest_t_mapped.csv', 'latest_t.csv']
        
        for csv_file in csv_files:
            if os.path.exists(csv_file):
                print(f"Loading data from {csv_file}")
                df = pd.read_csv(csv_file)
                print(f"Loaded {len(df)} rows from {csv_file}")
                return df.to_json(orient='records')
        
        print(f"Warning: No CSV file found. Available files: {os.listdir('.')}")
        return json.dumps([])
    except Exception as e:
        print(f"Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return json.dumps([])

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get CSV data"""
    try:
        data = load_data()
        return jsonify(json.loads(data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/csv')
def download_csv():
    """API endpoint to download CSV"""
    try:
        csv_file = 'latest_t_mapped.csv'
        if os.path.exists(csv_file):
            return send_file(csv_file, as_attachment=False, mimetype='text/csv')
        return jsonify({"error": "CSV not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "VOC Dashboard is running"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
