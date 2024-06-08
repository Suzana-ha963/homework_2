import socket

HOST = '127.0.0.1'
PORT = 8989

def validate_input(account, operation, amount=None):
    if not account:
        return "Invalid account name"
    if operation not in ["check", "deposit", "withdraw", "exit"]:
        return "Invalid operation"
    if operation in ["deposit", "withdraw"] and (amount is None or amount <= 0):
        return "Invalid amount"
    return None

def connect_and_send(account, operation, amount=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = f"{account},{operation}"
            if amount:
                data += f" {amount}"
            s.sendall(data.encode())
            response = s.recv(1024).decode()
            print(response)
    except Exception as e:
        print(f"Error: {e}")

def main():
    account = input("Enter account number: ")
    while True:
        operation = input("Enter operation (check, deposit, withdraw, exit): ")
        if operation == "exit":
            break
        if operation in ["deposit", "withdraw"]:
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("Invalid amount")
                continue
        else:
            amount = None
        error = validate_input(account, operation, amount)
        if error:
            print(error)
        else:
            connect_and_send(account, operation, amount)

if __name__ == "__main__":
    main()