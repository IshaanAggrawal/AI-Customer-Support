import os
import requests

API_URL = "http://127.0.0.1:8000/api/v1/docs/upload"
ADMIN_KEY = "2a62" 

DATA_FOLDER = os.path.join("backend", "data")

def ingest_data():
    if not os.path.exists(DATA_FOLDER):
        print(f"❌ Error: Folder '{DATA_FOLDER}' not found.")
        print(f"   Current working directory: {os.getcwd()}")
        return

    valid_extensions = (".txt", ".md", ".csv", ".json")
    files = [f for f in os.listdir(DATA_FOLDER) 
            if f.lower().endswith(valid_extensions)]
    
    if not files:
        print(f"⚠️  No valid files found in '{DATA_FOLDER}'.")
        return

    print(f"🚀 Found {len(files)} files in '{DATA_FOLDER}'. Starting ingestion...")
    print("-" * 50)
    for filename in files:
        file_path = os.path.join(DATA_FOLDER, filename)
        
        headers = {"x-api-key": ADMIN_KEY}

        try:
            with open(file_path, "rb") as f:
                files_data = {"file": (filename, f, "text/plain")}
                
                print(f"Uploading {filename}...", end=" ")
                response = requests.post(API_URL, headers=headers, files=files_data)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Success! ({data['chunks_ingested']} chunks)")
                elif response.status_code == 403:
                    print("❌ Failed: Invalid API Key.")
                else:
                    print(f"❌ Failed: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"❌ Error uploading {filename}: {e}")

    print("-" * 50)
    print("🎉 Ingestion complete!")

if __name__ == "__main__":
    ingest_data()