import requests
import json

API_URL = "http://127.0.0.1:8000/api/v1/chat/"

def chat_with_bot():
    print("🤖 AI Customer Support (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ["quit", "exit"]:
            break
            
        try:
            # Send question to backend
            response = requests.post(API_URL, json={"query": user_query})
            
            if response.status_code == 200:
                data = response.json()
                print(f"AI:  {data['answer']}")
                print(f"     [Sources: {', '.join(data['sources'])}]")
            elif response.status_code == 429:
                print("⚠️  Rate Limit Exceeded! (Wait a minute)")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    chat_with_bot()