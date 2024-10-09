import os
from flask import Flask, render_template, jsonify
import glob

app = Flask(__name__)

# Update directory paths
directory_path = os.path.join('Goftino_Monitoring', 'static')

# Helper function to find the latest file starting with a specific prefix
def find_latest_file(prefix):
    # Search for files that start with the given prefix
    files = glob.glob(os.path.join(directory_path, prefix + '*.png'))  # Ensure you're looking for PNG files
    print(f"Searching for files starting with '{prefix}'")
    
    if files:
        # Find the most recent file based on modification time
        latest_file = max(files, key=os.path.getmtime)
        print(f"Found latest file: {latest_file}")
        
        # Extract and return the file name only (without the full path)
        return os.path.basename(latest_file)
    
    return ""  # Return an empty string if no file is found

@app.route('/image_data')
def get_image_data():
    # Dynamically get the file names for the images
    single_png = find_latest_file('single')
    double_png = find_latest_file('double')
    
    return jsonify({
        'single_png': single_png,
        'double_png': double_png
    })

# Optional route to serve the main page
@app.route('/')
def home():
    # Find the latest PNG files for each box
    single_png_file = find_latest_file('single')
    double_png_file = find_latest_file('double')

    # Render the template with the file names
    return render_template('index.html', single_png=single_png_file, double_png=double_png_file)

if __name__ == '__main__':
    app.run(port=8585)
