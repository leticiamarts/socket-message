# Socket Message Exchange 

## Project Overview

This project is designed to implement a simple message exchange system between a client and a server using TCP sockets. The system allows a user to send messages from the client to the server, which will then print those messages on its terminal. The client can continue sending messages until the user types "exit", which will close the connection.

The project demonstrates basic socket programming concepts and can be a foundational exercise for understanding how network communication works in Python.


## Installation


### Environment

It is recommended to use a virtual environment `(.venv)` for setting up and isolating dependencies.

Personal environment:
- Python 3.11.1
- pip
- Git Bash


### 1. Clone Repository
To get started with the project, clone the repository to your local machine

### 2.  Set Up a Virtual Environment
Navigate to the project directory, create and activate a virtual environment using the following command: <br>
On Windows:

```
python -m venv .venv
source .venv/Scripts/activate
```


On Linux or MacOS:
```
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Once the virtual environment is activated, install the necessary dependencies listed in the `requirements.txt` file:
```
pip install -r requirements.txt
```

### 4. Set Up the `.env` file

The HOST and PORT variables are hidden inside an `.env` file for security reasons, which is not included in the project repository.

To configure the server and client, you must create your own `.env` file in the root directory of the project. The `.env` file should contain the following variables:

```
HOST=your_host
PORT=your_port
```

## Run the project

Once you have everything set up, you can run the server and client as follows:

#### Running the Server
Open a terminal, activate the virtual environment, and run the server:

```
python server.py
```
The server will start and wait for incoming client connections.


#### Running the Client
In another terminal, with the virtual environment activated, run the client:

```
python client.py
```

Once connected, the client will allow you to input messages, which will be sent to the server. Type "exit" to close the connection.

## Communication
- The client sends messages to the server using TCP sockets.
- The server prints each received message to its terminal.
- To disconnect, type exit in the client terminal.

## Example
The client side should look something like this:
```
You: Hello Server!
You: How are you?
You: exit
```

On the other side, the server side must look like:
```
[NEW CONNECTION] Client found: (host, port)
[host] Hello Server!
[host] How are you?
[DISCONNECTED] Client ('host', port) disconnected
```



### Troubleshooting
If you encounter any issues, make sure that the specified PORT is not being used by other services. You can change the port in the .env file to an available one.


At git bash on windows, you can run the following command to kill any task using the port:
```
cmd.exe /c taskkill /PID pid_number /T /F
```

`pid_number` can be found by the command:
```
netstat -ano | findstr :port
```
