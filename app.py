from flask import Flask, render_template, send_file, jsonify, send_from_directory
import pandas as pd
import os
import json

# Set up app with proper static folder configuration
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    """Serve the main dashboard"""
    try:
        # Load Original Code.html (CX Customer Dashboard)
        with open('Original Code.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            if html_content and len(html_content) > 5000:
                print(f"✓ Loaded Original Code.html ({len(html_content)} bytes)")
                return html_content
            else:
                print("⚠ Original Code.html is too small or empty")
                raise Exception("HTML file appears to be empty")
    except Exception as e:
        print(f"Error loading Original Code.html: {e}")
        print("Trying index.html as fallback...")
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
                if html_content and len(html_content) > 1000:
                    print(f"✓ Loaded index.html ({len(html_content)} bytes)")
                    return html_content
        except:
            pass
        
        print("Falling back to diagnostic page...")
        try:
            with open('diagnostic.html', 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return jsonify({"error": "Unable to load dashboard"}), 500

# Load CSV data
def load_data():
    try:
        # Try multiple possible CSV file names
        csv_files = ['latest_t_mapped_clean.csv', 'latest_t_mapped.csv', 'latest_t.csv']
        
        for csv_file in csv_files:
            file_path = os.path.join(os.getcwd(), csv_file)
            print(f"Checking for {csv_file}...")
            if os.path.exists(file_path):
                print(f"✓ Found {csv_file}, loading data...")
                df = pd.read_csv(file_path)
                print(f"✓ Loaded {len(df)} rows from {csv_file}")
                return df.to_json(orient='records')
        
        print(f"⚠ Warning: No CSV file found")
        print(f"Files in directory: {os.listdir('.')}")
        return json.dumps([])
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return json.dumps([])

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
