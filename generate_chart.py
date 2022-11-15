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

    # while user_input.lower() != "exit":
        # user_input = input("Press enter to continue or type exit: ")
        # title = input("Title: ")
    # player = 'Justin Verlander'
    x_axis = "Season"
    # y_axis = "K/9"

    title = f"{player}: {y_axis} by {x_axis}"
    parameters = f"{title},{x_axis},{y_axis}"

    # csv_file = input("CSV file: ")
    # csv_file = "./pitcher_stats.csv"
    # df = pd.read_csv(csv_file)  # Data_Baseball\Aaron_Nola.csv
    # df = df[df['Name'] == player].sort_values(by=['Season'])
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
            # dt = datetime.now()
            # dt = dt.strftime("%m-%d-%Y_%H%M%S")
            save_name = "static/images/"+ player.replace(" ", "_") + ".png"
            # save_name = save_name
            # fig.savefig("output/" + save_name)
            fig.savefig(save_name)
            print("Client: figure from server saved as " + save_name)

        return save_name

    except:
        return False


