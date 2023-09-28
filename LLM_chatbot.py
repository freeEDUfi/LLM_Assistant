import sys

# Append the path to the system path
sys.path.append('/mnt/storage1/local_LLM/GPU_LLAMA/GPU_LLAMA/LLM_Assistant/libraries')

from threading import Thread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import time
from langchain.prompts import PromptTemplate
from langchain.llms import LlamaCpp

 

class LLMChatbotWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        self.text_display = TextInput(readonly=True, background_color=[1, 1, 1, 1], foreground_color=[0, 0, 0, 1],
                                      size_hint_y=0.9)
        self.add_widget(self.text_display)

        input_layout = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=44)
        self.text_input = TextInput(hint_text="Enter your text here", size_hint_x=0.8)
        input_layout.add_widget(self.text_input)

        self.button = Button(text="Send", size_hint_x=0.2)
        self.button.bind(on_press=self.display_text)
        input_layout.add_widget(self.button)

        self.add_widget(input_layout)

        # Initializing the model in a separate thread to prevent freezing on startup
        self.llm = None
        thread = Thread(target=self.initialize_llm)
        thread.start()

    def display_text(self, instance):
        question = self.text_input.text
        if not question.strip():  # Ensure the question is not empty or just whitespace
            return
        self.text_display.text = f"Question: {question}\n\nPlease wait..."

        # Clear the text_input widget after fetching its text
        self.text_input.text = ''

        thread = Thread(target=self.get_answer_from_llm, args=(question,))
        thread.start()

    def get_answer_from_llm(self, question):
        # Ensure LlamaCpp model is initialized
        while not self.llm:
            time.sleep(0.1)
        answer = self.ask_llm(question)
        self.answer_from_thread = answer
        Clock.schedule_once(self.update_ui_from_thread)

    def update_ui_from_thread(self, dt):
        self.text_display.text = self.text_display.text.replace("Please wait...", f"Answer: {self.answer_from_thread}")

    def initialize_llm(self):
        try:
            n_gpu_layers = 35
            n_batch = 500
            n_ctx = 700

            self.llm = LlamaCpp(
                model_path="/mnt/storage1/local_LLM/GPU_LLAMA/GPU_LLAMA/LLM_Assistant/llama-2-7b-chat.Q4_K_M.gguf",
                n_gpu_layers=n_gpu_layers,
                n_batch=n_batch,
                n_ctx=n_ctx,
                max_tokens=0,
                verbose=True
            )
        except Exception as e:
            print(f"Failed to initialize LLM: {e}")

    def ask_llm(self, question):
        template = (
            "Question: {question}\n\n"
            "Answer: Please provide short explanation, dont cut off your explanation."
        )
        prompt_template = PromptTemplate.from_template(template)
        formatted_prompt = prompt_template.format(question=question)
        response = self.llm(formatted_prompt)  # Assuming self.llm is correctly initialized and callable
        return response

