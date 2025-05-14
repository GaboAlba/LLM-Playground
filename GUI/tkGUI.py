from tkinter import *
from tkinter import ttk
from ApiClients.LLMClient import LLMClient

class TkGui:
  def __init__(self, clients: list[LLMClient]):
    self.clients = clients
    self.root = Tk()
    self.root.title("LLM Playground")
    self.root.geometry("1920x1080")
    self.root.resizable(width=True, height=True)

    self.Title = Label(self.root, text="LLM Playground", font=("Helvetica", 24))
    self.Title.pack(pady=20)

    self.TextBox = Text(self.root, height=20, width=100)
    self.TextBox.pack(pady=20)

    self.SubmitButton = Button(self.root, text="Submit", command=self.submit)
    self.SubmitButton.pack(pady=20)

  def get_selected_client(self, selected_client_str: str):
      for client in self.clients:
        if client.name == selected_client_str:
          return client
      
      raise ValueError(f"Client {selected_client_str} is not a valid client. Allowed clients are: {[client.name for client in self.clients]}")
  
  def update_model_list(self):
    selected_client = self.get_selected_client(self.LLMClientDropdown.get())
    self.LLMModelDropdown['values'] = []
    self.LLMModelDropdown['values'] = selected_client.allowed_models
    self.LLMModelDropdown.set(selected_client.allowed_models[0])

  def submit(self):
    input_text = self.TextBox.get("1.0", "end-1c")
    print(input_text)  # Replace with actual LLM call
  
  def Refresh(self):
    self.root.destroy()
    self.root.__init__()

  def run(self):
    llm_client_names = [client.name for client in self.clients]
    self.LLMClientLabel = Label(self.root, text="LLM Client")
    self.LLMClientLabel.pack(pady=20)
    self.LLMClientDropdown = ttk.Combobox(self.root, values= llm_client_names)
    self.LLMClientDropdown.set("OpenAI")
    self.LLMClientDropdown.pack()
    self.LLMClientDropdown.bind("<<ComboboxSelected>>", lambda event: self.update_model_list())
    
    clientSelected = self.get_selected_client(self.LLMClientDropdown.get())
    self.LLMModelLabel = Label(self.root, text="LLM Model")
    self.LLMModelLabel.pack(pady=20)
    self.LLMModelDropdown = ttk.Combobox(self.root, values= clientSelected.allowed_models, width=50)
    self.LLMModelDropdown.set("gpt-3.5-turbo")
    self.LLMModelDropdown.pack()

    self.root.mainloop()

    

