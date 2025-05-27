import yaml
from tkinter import *
from tkinter import ttk, filedialog
from ApiClients.LLMClient import LLMClient
from ApiClients.OpenAIClient import OpenAIClient
from ApiClients.GoogleAIClient import GoogleAiClient
from ApiKeys.apiKeysHandler import ApiKeysHandler


class TkGui:
  def __init__(self):
    self.placeholderPromptText = "Enter your prompt here..."
    self.placeholderResultText = "Result will be displayed here..."
    self.apiKeysHandler = ApiKeysHandler()
    self.clients = []

    # Create the UI
    self.root = Tk()
    self.root.title("LLM Playground")
    self.root.geometry("1920x1080")

    self.menubar = Menu(self.root)
    self.filemenu = Menu(self.menubar, tearoff=0)
    self.menubar.add_cascade(label="File", menu=self.filemenu, font=("Helvetica", 16))
    self.filemenu.add_command(label="API keys", command = self.show_api_keys_window)
    self.filemenu.add_command(label="Refresh", command= self.refresh)

    self.root.config(menu=self.menubar)

    self.leftFrame = Frame(self.root)
    self.leftCanvas = Canvas(self.leftFrame)
    self.leftFrameScrollbar = Scrollbar(self.leftFrame, command=self.leftCanvas.yview)
    self.leftScrollableFrame = Frame(self.leftCanvas)

    self.leftScrollableFrame.bind(
      "<Configure>",
      lambda e: self.leftCanvas.configure(
        scrollregion=self.leftCanvas.bbox("all")
      )
    )

    self.leftCanvas.create_window((0, 0), window=self.leftScrollableFrame, anchor="nw")
    self.leftCanvas.configure(yscrollcommand=self.leftFrameScrollbar.set)
  
    self.leftFrame.pack(side=LEFT, fill=BOTH, expand=True)
    self.leftCanvas.pack(side=LEFT, fill=BOTH, expand=True)
    self.leftFrameScrollbar.pack(side=RIGHT, fill=Y)

    self.rightFrame = Frame(self.root)
    self.rightFrame.pack(side=RIGHT, fill=Y, padx=20, pady=100)
    
    self.topLeftFrame = Frame(self.leftScrollableFrame)
    self.topLeftFrame.pack(side=TOP, fill=X, padx=20, pady=30)

    self.bottomLeftFrame = Frame(self.leftScrollableFrame)
    self.bottomLeftFrame.pack(side=BOTTOM, fill=X, padx=20, pady=30)

    self.Title = Label(self.topLeftFrame, text="LLM Playground", font=("Helvetica", 24))
    self.Title.pack(pady=20)

    self.PromptBoxTitle = Label(self.topLeftFrame, text="Prompt", font=("Helvetica", 16))
    self.PromptBoxTitle.pack(pady=20, anchor=W)
    self.PromptBox = Text(self.topLeftFrame, height=30, width=200)
    self.PromptBox.pack(pady=20, padx=20, fill=X)
    self.PromptBox.insert(END, "Enter your prompt here...")
    self.PromptBox.config(state=NORMAL)
    self.PromptBox.bind("<FocusIn>", lambda event: self.on_focus_in())
    self.PromptBox.bind("<FocusOut>", lambda event: self.on_focus_out())

    self.SubmitButton = Button(self.topLeftFrame, text="Submit", command=self.submit)
    self.SubmitButton.pack(pady=20)

    self.ResultBoxTitle = Label(self.bottomLeftFrame, text="Result", font=("Helvetica", 16))
    self.ResultBoxTitle.pack(pady=20, anchor=W)
    self.ResultBox = Text(self.bottomLeftFrame, height=20, width=200)
    self.ResultBox.pack(pady=20, padx=20, fill=X)
    self.ResultBox.insert(END, "Result will be displayed here...")
    self.ResultBox.config(state=DISABLED)
    self.ResultBox.bind("<FocusIn>", lambda event: self.on_focus_in())
    self.ResultBox.bind("<FocusOut>", lambda event: self.on_focus_out())
    self.ResultBox.config(fg="grey")

  def show_api_keys_window(self):
    self.api_keys_window = Toplevel(self.root)
    self.api_keys_window.title("API Keys")
    self.api_keys_window.geometry("400x400")
    self.api_keys_window.resizable(width=False, height=False)

    # Create a label for the API keys directory
    label = Label(self.api_keys_window, text="API Keys Directory:")
    label.pack(pady=10)
    entry = Entry(self.api_keys_window)
    entry.pack(pady=10)

    # Load the API keys
    self.apiKeysHandler.load_api_keys()
    self.apiKeys = self.apiKeysHandler.api_keys
    print(f"Path to API keys file: {self.apiKeysHandler.api_keys_file}")
    
    # Create a button to select the API keys file
    select_button = Button(self.api_keys_window, text="Select API Keys File", command=self.browse_api_keys_file)
    select_button.pack(pady=20)

    # Create OpenAI API key entry
    openAI_label = Label(self.api_keys_window, text="OpenAI API Key:")
    openAI_label.pack(pady=10)
    key = self.apiKeys.get("OpenAI") if self.apiKeys else ""
    print(f"OpenAI Key: {key}")
    self.openAI_entry = Entry(self.api_keys_window, show = key if key else "")
    self.openAI_entry.pack(pady=10)
    self.openAI_entry.insert(0, key)

    # Create Google GenAI API Key entry
    GoogleAI_label = Label(self.api_keys_window, text="GoogleAI API Key:")
    GoogleAI_label.pack(pady=10)
    key = self.apiKeys.get("GoogleAI") if self.apiKeys else ""
    print(f"GoogleAI Key: {key}")
    self.GoogleAI_entry = Entry(self.api_keys_window, show = key if key else "")
    self.GoogleAI_entry.pack(pady=10)
    self.GoogleAI_entry.insert(0, key)
    
    # Create a button to save the API keys
    save_button = Button(self.api_keys_window, text="Save", command=self.save_api_keys)
    save_button.pack(pady=20)

  
  def save_api_keys(self):
    self.clients = []
    openAiKey = self.openAI_entry.get()
    googleAiKey = self.GoogleAI_entry.get()
    self.apiKeys = []
    
    # Create and set all available clients
    self.set_clients(openAiKey=openAiKey, googleAiKey=googleAiKey)
    
    self.api_keys_window.destroy()
    self.refresh()

  def browse_api_keys_file(self):
    file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")])
    if file_path:
      self.apiKeysHandler.api_keys_file = file_path
      self.apiKeysHandler.load_api_keys()
      self.set_clients()
      self.openAI_entry.insert(0,self.apiKeysHandler.get_api_key("OpenAI"))
      self.GoogleAI_entry.insert(0, self.apiKeysHandler.get_api_key("GoogleAI"))

  def get_selected_client(self, selected_client_str: str):
      for client in self.clients:
        if client.name == selected_client_str:
          self.client = client
          return client
      
      raise ValueError(f"Client {selected_client_str} is not a valid client. Allowed clients are: {[client.name for client in self.clients]}")
  
  def update_model_list(self):
    selected_client = self.get_selected_client(self.LLMClientDropdown.get())
    self.LLMModelDropdown['values'] = []
    self.LLMModelDropdown['values'] = selected_client.allowed_models
    self.LLMModelDropdown.set(selected_client.allowed_models[0])

    if (type(selected_client) == OpenAIClient):
      self.TopKLabel.pack_forget()
      self.TopKSlider.pack_forget()
      self.TemperatureSlider.config(from_=0, to=1, resolution=0.1)
    elif (type(selected_client) == GoogleAiClient):
      self.TopKLabel.pack(pady=20)
      self.TopKSlider.pack()
      self.TemperatureSlider.config(from_=0, to=2, resolution=0.1)

  def on_focus_in(self):
    if self.PromptBox.get("1.0", "end-1c") == self.placeholderPromptText:
      self.PromptBox.delete("1.0", "end-1c")
      self.PromptBox.config(fg="black")

    if self.ResultBox.get("1.0", "end-1c") == self.placeholderResultText:
      self.ResultBox.delete("1.0", "end-1c")
      self.ResultBox.config(fg="black")
    
  def on_focus_out(self):
    if self.PromptBox.get("1.0", "end-1c") == "":
      self.PromptBox.insert("1.0", self.placeholderPromptText)
      self.PromptBox.config(fg="grey")

    if self.ResultBox.get("1.0", "end-1c") == "":
      self.ResultBox.insert("1.0", self.placeholderResultText)
      self.ResultBox.config(fg="grey")

  def set_clients(self, openAiKey = "", googleAiKey = ""):
    # Set OpenAI API client with the Key
    client = OpenAIClient(openAiKey if openAiKey != "" else self.apiKeysHandler.get_api_key("OpenAI"))
    self.apiKeysHandler.set_api_key(client.name, openAiKey if openAiKey != "" else self.apiKeysHandler.get_api_key(client.name))
    self.clients.append(client)

    # Set Google AI API client with the key
    client = GoogleAiClient(googleAiKey if googleAiKey != "" else self.apiKeysHandler.get_api_key("GoogleAI"))
    self.apiKeysHandler.set_api_key(client.name, googleAiKey if googleAiKey != "" else self.apiKeysHandler.get_api_key(client.name))
    self.clients.append(client)


  def submit(self):
    input_text = self.PromptBox.get("1.0", "end-1c")
    
    # Allow for result box to be filled
    self.ResultBox.config(state=NORMAL)

    # Convert the prompt into an object
    messages = self.client.convert_prompt_to_object(input_text)
    if not messages:
      self.ResultBox.insert(END, "Invalid prompt format. Please use {{role <role>}} Role message {{role/}} format.")
      self.ResultBox.config(state=DISABLED)
      return
    
    # Build the request object
    request = self.client.build_request(
      model = self.LLMModelDropdown.get(),
      messages = messages,
      temperature = self.TemperatureSlider.get(),
      max_tokens = int(self.MaxTokensEntry.get()),
      top_k = int(self.TopPSlider.get()),
      top_p = self.TopPSlider.get(),
      frequency_penalty = self.FrequencyPenaltySlider.get(),
      presence_penalty = self.PresencePenaltySlider.get()
    )

    # Call the LLM client
    response = self.client.generate_response(request)
    if not response:
      self.ResultBox.insert(END, "Failed to get a response from the LLM.")
      self.ResultBox.config(state=DISABLED)
    else:
      self.ResultBox.delete("1.0", "end-1c")
      self.ResultBox.insert(END, response)
      self.ResultBox.config(state=DISABLED)
      print(response)
  
  def refresh(self):
    self.root.destroy()
    self.__init__()
    self.run()

  def run(self):
    if not self.apiKeysHandler.are_all_api_keys_set():
      self.show_api_keys_window()
    else:
      self.set_clients()
      
    llm_client_names = [client.name for client in self.clients]
    self.LLMClientLabel = Label(self.rightFrame, text="LLM Client")
    self.LLMClientLabel.pack(pady=20)
    self.LLMClientDropdown = ttk.Combobox(self.rightFrame, values= llm_client_names)
    self.LLMClientDropdown.set("OpenAI")
    self.LLMClientDropdown.pack()
    self.LLMClientDropdown.bind("<<ComboboxSelected>>", lambda event: self.update_model_list())
    
    try:
      clientSelected = self.get_selected_client(self.LLMClientDropdown.get())
      self.LLMModelLabel = Label(self.rightFrame, text="LLM Model")
      self.LLMModelLabel.pack(pady=20)
      self.LLMModelDropdown = ttk.Combobox(self.rightFrame, values= clientSelected.allowed_models, width=50)
      self.LLMModelDropdown.set("gpt-3.5-turbo")
      self.LLMModelDropdown.pack()
    except Exception as e:
      print(f"Error: {e}")
      self.LLMModelLabel = Label(self.rightFrame, text="LLM Model")
      self.LLMModelLabel.pack(pady=20)
      self.LLMModelDropdown = ttk.Combobox(self.rightFrame, values= [], width=50)
      self.LLMModelDropdown.set("No models available")
      self.LLMModelDropdown.pack()

    # Define Sliders for the LLM parameters
    self.TemperatureLabel = Label(self.rightFrame, text="Temperature")
    self.TemperatureLabel.pack(pady=20)
    self.TemperatureSlider = Scale(self.rightFrame, from_=0, to=1, resolution=0.1, orient=HORIZONTAL)
    self.TemperatureSlider.set(0.7)
    self.TemperatureSlider.pack()

    self.TopKLabel = Label(self.rightFrame, text="Top K")
    self.TopKLabel.pack(pady=20)
    self.TopKSlider = Entry(self.rightFrame)
    self.TopKSlider.insert(0, "3")
    self.TopKSlider.pack()

    self.TopPLabel = Label(self.rightFrame, text="Top P")
    self.TopPLabel.pack(pady=20)
    self.TopPSlider = Scale(self.rightFrame, from_=0, to=1, resolution=0.1, orient=HORIZONTAL)
    self.TopPSlider.set(0.7)
    self.TopPSlider.pack()

    # Max Tokens will not be a slider, but a simple entry box
    self.MaxTokensLabel = Label(self.rightFrame, text="Max Tokens")
    self.MaxTokensLabel.pack(pady=20)
    self.MaxTokensEntry = Entry(self.rightFrame)
    self.MaxTokensEntry.insert(0, "1000")
    self.MaxTokensEntry.pack()
    
    self.FrequencyPenaltyLabel = Label(self.rightFrame, text="Frequency Penalty")
    self.FrequencyPenaltyLabel.pack(pady=20)
    self.FrequencyPenaltySlider = Scale(self.rightFrame, from_=0, to=1, resolution=0.1, orient=HORIZONTAL)
    self.FrequencyPenaltySlider.set(0)
    self.FrequencyPenaltySlider.pack()

    self.PresencePenaltyLabel = Label(self.rightFrame, text="Presence Penalty")
    self.PresencePenaltyLabel.pack(pady=20)
    self.PresencePenaltySlider = Scale(self.rightFrame, from_=0, to=1, resolution=0.1, orient=HORIZONTAL)
    self.PresencePenaltySlider.set(0)
    self.PresencePenaltySlider.pack()

    self.root.mainloop()

    

