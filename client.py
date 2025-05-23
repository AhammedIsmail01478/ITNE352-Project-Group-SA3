import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    try:
        sock.connect(('localhost', 55555))
        print("The request has been sent")         #Sends connection request to the server
        AckMsg = sock.recv(4096).decode('utf-8')      #Receives acknowedgment message of succesfully establishing connection
        print(AckMsg)

        server_msg = sock.recv(4096).decode('utf-8')     #Server requests for username
        CName = input(server_msg)
        sock.sendall(CName.encode('utf-8'))           #sends the username to the server

        while True:
            print(sock.recv(4096).decode(), end='')  #Receives the Menu list from the server
            choice = input("> ")
            sock.sendall(choice.encode())

            if choice == '3':  # request flight code
                print(sock.recv(1024).decode(), end='')          #Server asks for iata code if option 3 is selected
                iata = input("> ")
                sock.sendall(iata.encode())

            response = sock.recv(65536).decode()         #receives response based on the option they selected.
            print("\n--- Response ---")
            print(response)           #prints the response, with ether flight details, or goodbye message is option 4 was selected
    

            if choice == '4':
                break             #break the while loop when option 4 is selected
    except ConnectionRefusedError:             #Incase the server havent started yet or is not accepting requests yet
        print("Error", "Cannot connect to the server.")
    except Exception as e:
        print(f"[ERROR] : {e}")
