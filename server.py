import socket
import threading

HOST = '0.0.0.0'
PORT = 8989

accounts = {
    "1": {"balance": 1000},
    "2": {"balance": 500}
}

def validate_input(data):
    try:
        account, operation = data.split(",")
        if operation.startswith("check"):
            return account, "check"
        elif operation.startswith("deposit"):
            amount = float(operation.split(" ")[1])
            if amount <= 0:
                return None, "Invalid deposit amount"
            return account, ("deposit", amount)
        elif operation.startswith("withdraw"):
            amount = float(operation.split(" ")[1])
            if amount <= 0:
                return None, "Invalid withdrawal amount"
            return account, ("withdraw", amount)
        else:
            return None, "Invalid request"
    except (ValueError, IndexError):
        return None, "Invalid input format"

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            account, operation = validate_input(data)
            if operation == "check":
                if account not in accounts:
                    response = "Invalid account!"
                else:
                    balance = accounts[account]["balance"]
                    response = f"Your balance is: ${balance}"
            elif operation == "deposit":
                if account not in accounts:
                    response = "Invalid account!"
                else:
                    amount = operation[1]
                    accounts[account]["balance"] += amount
                    response = f"Deposited ${amount}. New balance: ${accounts[account]['balance']}"
            elif operation == "withdraw":
                if account not in accounts:
                    response = "Invalid account!"
                else:
                    balance = accounts[account]["balance"]
                    amount = operation[1]
                    if amount > balance:
                        response = "Insufficient funds!"
                    else:
                        accounts[account]["balance"] -= amount
                        response = f"Withdrew ${amount}. New balance: ${accounts[account]['balance']}"
            else:
                response = operation

            conn.sendall(response.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print(f"Client {addr} disconnected")

def start_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening on port {PORT}")
            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_server()
    