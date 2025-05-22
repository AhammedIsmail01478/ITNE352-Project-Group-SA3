# ITNE352-Project-Group-SA3
Project for ITNE352 by Ahammed Ismail and Bilal Mohammad Tofeeq ID: 202201478 &amp; 202200507 respectively.

## **Project Title**

**Multithreaded Flight Arrival Client/Server Information System**

## **Project Description**



## **Semester**

**2nd Semester,2024-2025**


## **Group Details**

* Group Number: SA3
  
* Course Code: ITNE352/ITCE320

* Section Number: 01

* Students Names: Ahammed Ismail ,Bilal Mohammad Tofeeq  

* Students IDs: 202201478, 202200507

  ## Table of Contents

1- [Requirements](#requirements)

2- [How to](#how-to)

3- [The Scripts](#the-scripts)

4- [Additional Concepts](#additional-concepts)

5- [Acknowledgments](aAcknowledgments)

6- [Conclusion](#conclusion)

## **Requirements**

To establish the project and run the peoject in local environment follow these steps which are given below:

1. **Install Python** Install the latest version of python from python's original website, which is:(https://www.python.org/downloads/)
2. Clone the repository:


3. Navigate to the closed directory:


4. Install required dependencies:
5. **Get a FlightAPI Key**
- Register on   
- Replace 

## **How to Run**
 
 To run the system:

 1. Open two terminal windows, one for client and one for server

 2. In the terminal, go to the directory containing the client and server files.

 3. Start with the server side so it can prepare for incoming reuqests which can be done by running the script:
 ```
 python server.py
 ```

 4. Start the client side next and then connect to server that is already running using the script:
 ```
 python client.py
 ```
 5. Use the Client - side interface to:
     - Client input info
     - Navigates Menu
     - Interacts and retrieves data
   
  
## **The Scripts**

### **Client Script (`client.py`)**






### **Server Script (`server.py`)**
The packages which are used in the Server Script are:
```
import socket
import threading
import json
import requests
```



        
