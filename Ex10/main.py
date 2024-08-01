from flask import Flask, send_file
from google.cloud import storage

app = Flask(__name__)

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ConorLynam/Coding/PythonGcpExercises/Ex10/key.json"

@app.route('/download/<bucket_name>/<object_id>', methods=['GET'])
def download(bucket_name, object_id):
    if not bucket_name or not object_id:
        return 'Missing bucket name or object_id', 400
    
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_id)
        # Creates a file
        blob.download_to_filename(object_id)
        return send_file(object_id, as_attachment=True)
    except Exception as e:
        return str(e), 500
        

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081)

