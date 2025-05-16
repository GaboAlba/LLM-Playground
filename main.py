from GUI.tkGUI import TkGui
from ApiClients.OpenAIClient import OpenAIClient
from ApiClients.GoogleAIClient import GoogleAiClient

if __name__ == "__main__":
    # Define the API keys
    openai_api_key = ""
    google_api_key = ""

    # Define the clients
    openai_client = OpenAIClient(api_key=openai_api_key)
    google_client = GoogleAiClient(api_key=google_api_key)

    # Create the GUI
    client_list = [openai_client, google_client]
    app = TkGui(client_list)
    # Run the GUI
    app.run()