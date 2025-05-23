import socket
import threading
import json
import requests
clients_list = {}         #List of active clients
clients_list_lock = threading.Lock()       #To prevent list corruption when multple threads try to access client_list

def display_active_clients(clients_list):      #Used to display list of active clients, it is called everytime a client leaves or joins
    for addr in clients_list:
            print(f"{clients_list[addr]} is connected with IP: {addr[0]} - Port: {addr[1]}")
    print(84*"=" + "\n")


def retrieve_flight_data(API_key, icao):       #Function to retrieve data from API and to save it into a json file
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        'access_key': API_key,
        'arr_icao': icao,
        'limit': 100
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        with open('SA3.json', 'w') as f:
            json.dump(data, f, indent=4)           #json file newly created or fully edited existing json file to only include flght records of the selected airport only
        return data
    else:
        print(f"API error: {response.status_code}")
        return None
        
def handle_client(conn, sockaddr, data):           #function to handle each client seperately through threads
    try:
        AckMsg = f'Accepted request from {sockaddr[0]} with port number {sockaddr[1]}'
        print(AckMsg)
        conn.sendall(AckMsg.encode('utf-8'))         #Sending Ack message to client on succesfully establishing a socket connection
        conn.sendall(("SERVER >> Please state your Username: ").encode('utf-8'))       #Requesting user to input Username

        clientName=conn.recv(4096).decode('utf-8').strip()
        with clients_list_lock:
            clients_list[sockaddr] = clientName          #Added new client to the list
        print(clientName,'has connected with address',sockaddr)

        print("\n" + 30*"=", "CURRENT ACTIVE CLIENTS", 30*"=")     #Displaays the list of current Active Clients
        display_active_clients(clients_list)

        menu = ("\nChoose an option (1-4):\n"
                    "1. View All Arrived Flights\n"
                    "2. View All Delayed Flights\n"
                    "3. View Particular Flight\n"
                    "4. Quit\n> ")
        
        while True:
            conn.sendall(menu.encode('utf-8'))          #Sending Menu to the client
            choice = conn.recv(1024).decode().strip()    #receives the input from the client for the option they selected

            if choice == '1':
                print(f"{clientName} has selected option {choice}: View All Arrived Flights")
                results = []
                for flight in data['data']:
                    if flight['arrival']['actual'] is None:      #Arrival None/null means flights already arrived
                        results.append({
                            'Flight (IATA code)': flight['flight']['iata'],
                            'Departure Airport': flight['departure']['airport'],
                            'Arrival Time': flight['arrival']['actual'],
                            'Arrival Terminal': flight['arrival']['terminal'],
                            'Arrival Gate': flight['arrival']['gate']
                        })
                conn.sendall(json.dumps(results, indent=2).encode())

            elif choice == '2':
                print(f"{clientName} has selected option {choice}: View All Delayed Flights")
                results = []
                for flight in data['data']:
                    delay = flight['arrival']['delay']
                    if delay and delay > 0:       #Delay > 0 means still in delay
                        results.append({
                            'Flight (IATA code)': flight['flight']['iata'],
                            'Departure Airport': flight['departure']['airport'],
                            'Original Departure Time': flight['departure']['scheduled'],
                            'Estimated Time of Arrival': flight['arrival']['estimated'],
                            'Arrival Terminal': flight['arrival']['terminal'],
                            'Delay (min)': delay,
                            'Arrival Gate': flight['arrival']['gate']
                        })
                conn.sendall(json.dumps(results, indent=2).encode())

            elif choice == '3':
                conn.sendall(b"Enter flight IATA code: ")
                iata_code = conn.recv(1024).decode().strip().upper()
                print(f"{clientName} has selected option {choice}: View Particular Flight with iataa code: {iata_code}")
                found = False
                for flight in data['data']:
                    if flight['flight']['iata'] == iata_code:
                        info = {
                            'Flight (IATA code)': flight['flight']['iata'],
                            'Departure Airport': flight['departure']['airport'],
                            'Departure Gate': flight['departure']['gate'],
                            'Departure Terminal': flight['departure']['terminal'],
                            'Arrival Airport': flight['arrival']['airport'],
                            'Arrival Gate': flight['arrival']['gate'],
                            'Arrival Terminal': flight['arrival']['terminal'],
                            'Status': flight['flight_status'],
                            'Scheduled Departure Time': flight['departure']['scheduled'],
                            'Scheduled Arrival Time': flight['arrival']['scheduled']
                        }
                        conn.sendall(json.dumps(info, indent=2).encode())
                        found = True
                        break
                if not found:
                    conn.sendall(b"Flight not found.\n")

            elif choice == '4':
                print(f"{clientName} has selected option {choice}: Quit")
                print(f"{clientName} has disconnected!")
                conn.sendall(b"Goodbye!\n")
                break
            else:
                conn.sendall(b"Invalid option.\n")

    except ConnectionResetError:
        print(f"[WARNING] Client at {sockaddr} disconnected unexpectedly!")        #Incase the client doesnt disconnect or close socket gracefully through sock.close()
    
    except Exception as e:
        print(f"[ERROR] Unexpected error with {sockaddr}: {e}")
    finally:   #Finishes the conversation by removing the client from the active client list, closing the socket with conn.close() and by displaying the updated client list
        with clients_list_lock:
            if sockaddr in clients_list:
                del clients_list[sockaddr]
        conn.close()
        print(f"Connection with address {sockaddr} has been closed !")

        print("\n" + 30*"=", "CURRENT ACTIVE CLIENTS", 30*"=")     #Displays the list of current Active Clients
        if not clients_list:
            print("No Active Clients at the Moment! Awaiting New Clients...")
            print(84*"=" + "\n")
        else:
            display_active_clients(clients_list)



if __name__ == "__main__":        #Main thread
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(('localhost', 55555))         #Starting server by binding socket
        print("Server has succesfully started!")

        API_key = "5ff2c6cdc5522f0aa5ec48d239139ede"      #Free API access key from aviationstack.com
        data = None
        while data is None:
            valid_icao = False
            while not valid_icao:
                arr_icao = input("Enter the airport code (arr_icao): ").strip().upper()        #Ask the server user to Enter the airport code (arr_icao) and check its validity
                if len(arr_icao) == 4 and arr_icao.isalpha():
                    valid_icao=True
                else:
                    print("ERROR: Invalid code, Please try again!")
    
            data = retrieve_flight_data(API_key, arr_icao)
            if data is None:
                print("Please Try Again!")
        print("Flight Data succesfully retrieved!")

        server_sock.listen(6)
        print("Server is listening on localhost port 55555. Waiting for requests!")

        while True:
            try:
                conn,sockaddr=server_sock.accept()
                thread = threading.Thread(target=handle_client, args=(conn, sockaddr, data))
                thread.start()                                #Starts threads to communicate with multiple clients at once
            except Exception as e:
                print(f"[ERROR] Could not accept the request: {e}")