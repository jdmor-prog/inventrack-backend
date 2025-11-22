import httpx
import sys

BASE_URL = "http://localhost:8002"

def test_login():
    print("Probando Login en puerto 8002...")
    login_data = {
        "username": "admin@inventrack.com",
        "password": "123456"
    }
    try:
        response = httpx.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            print("Login exitoso en 8002!")
            print(response.json())
        else:
            print(f"Login fallido en 8002: {response.status_code} - {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_login()
