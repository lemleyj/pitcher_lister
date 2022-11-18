import pandas as pd
import socket
import pickle
from datetime import datetime

def generate_chart(df, player, y_axis):
    """
    Sends a request to my partner's microservice to generate a graphic for the pitcher. 
    """
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    user_input = ""

    x_axis = "Season"

    title = f"{player}: {y_axis} by {x_axis}"
    parameters = f"{title},{x_axis},{y_axis}"

    df = df.to_json()
    try: 

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(bytes(parameters, encoding="utf-8"))
            print(s.recv(1024))
            s.send(b"start_sending_data")
            print(s.recv(1024))
            print("Client: sending data")
            s.sendall(bytes(df, encoding="utf-8"))
            s.send(b"\ndone_sending_data")
            data = s.recv(200000)
            fig = pickle.loads(data)
            save_name = "static/images/"+ player.replace(" ", "_") + ".png"
            fig.savefig(save_name)
            print("Client: figure from server saved as " + save_name)

        return save_name

    except:
        return False


