from tkinter import *
from tkinter import ttk
from ApiClients.LLMClient import LLMClient

class TkGui:
  def __init__(self, clients: list[LLMClient]):
    self.placeholderPromptText = "Enter your prompt here..."
    self.placeholderResultText = "Result will be displayed here..."
    self.clients = clients
    self.client = clients[0]
    self.root = Tk()
    self.root.title("LLM Playground")
    self.root.geometry("1920x1080")
    self.root.resizable(width=True, height=True)

    self.leftFrame = Frame(self.root)
    self.leftFrame.pack(side=LEFT, fill=Y, padx=20, pady=30)

    self.rightFrame = Frame(self.root)
    self.rightFrame.pack(side=RIGHT, fill=Y, padx=20, pady=100)
    
    self.topLeftFrame = Frame(self.leftFrame)
    self.topLeftFrame.pack(side=TOP, fill=X, padx=20, pady=30)

    self.bottomLeftFrame = Frame(self.leftFrame)
    self.bottomLeftFrame.pack(side=BOTTOM, fill=X, padx=20, pady=30)

    self.Title = Label(self.root, text="LLM Playground", font=("Helvetica", 24))
    self.Title.pack(pady=20)

    self.PromptBoxTitle = Label(self.topLeftFrame, text="Prompt", font=("Helvetica", 16))
    self.PromptBoxTitle.pack(pady=20, anchor=W)
    self.PromptBox = Text(self.topLeftFrame, height=30, width=200)
    self.PromptBox.pack(pady=20)
    self.PromptBox.insert(END, "Enter your prompt here...")
    self.PromptBox.config(state=NORMAL)
    self.PromptBox.bind("<FocusIn>", lambda event: self.on_focus_in())
    self.PromptBox.bind("<FocusOut>", lambda event: self.on_focus_out())

    self.SubmitButton = Button(self.topLeftFrame, text="Submit", command=self.submit)
    self.SubmitButton.pack(pady=20)

    self.ResultBoxTitle = Label(self.bottomLeftFrame, text="Result", font=("Helvetica", 16))
    self.ResultBoxTitle.pack(pady=20, anchor=W)
    self.ResultBox = Text(self.bottomLeftFrame, height=20, width=200)
    self.ResultBox.pack(pady=20)
    self.ResultBox.insert(END, "Result will be displayed here...")
    self.ResultBox.config(state=DISABLED)
    self.ResultBox.bind("<FocusIn>", lambda event: self.on_focus_in())
    self.ResultBox.bind("<FocusOut>", lambda event: self.on_focus_out())
    self.ResultBox.config(fg="grey")

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
  
  def Refresh(self):
    self.root.destroy()
    self.root.__init__()

  def run(self):
    llm_client_names = [client.name for client in self.clients]
    self.LLMClientLabel = Label(self.rightFrame, text="LLM Client")
    self.LLMClientLabel.pack(pady=20)
    self.LLMClientDropdown = ttk.Combobox(self.rightFrame, values= llm_client_names)
    self.LLMClientDropdown.set("OpenAI")
    self.LLMClientDropdown.pack()
    self.LLMClientDropdown.bind("<<ComboboxSelected>>", lambda event: self.update_model_list())
    
    clientSelected = self.get_selected_client(self.LLMClientDropdown.get())
    self.LLMModelLabel = Label(self.rightFrame, text="LLM Model")
    self.LLMModelLabel.pack(pady=20)
    self.LLMModelDropdown = ttk.Combobox(self.rightFrame, values= clientSelected.allowed_models, width=50)
    self.LLMModelDropdown.set("gpt-3.5-turbo")
    self.LLMModelDropdown.pack()

    # Define Sliders for the LLM parameters
    self.TemperatureLabel = Label(self.rightFrame, text="Temperature")
    self.TemperatureLabel.pack(pady=20)
    self.TemperatureSlider = Scale(self.rightFrame, from_=0, to=1, resolution=0.1, orient=HORIZONTAL)
    self.TemperatureSlider.set(0.7)
    self.TemperatureSlider.pack()

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

    

