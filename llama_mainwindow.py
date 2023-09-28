import sys

sys.path.append('/mnt/storage1/local_LLM/GPU_LLAMA/GPU_LLAMA/LLM_Assistant/libraries')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# Assuming these imports are correct for your project
from Fileanalyzer import LLMWidget
from LLM_chatbot import LLMChatbotWidget

class SecureLLMApp(App):  # Updated the class name here
    def build(self):
        layout = FloatLayout()

        # File Analyzer Button and Label
        file_analyzer_image = 'upload-to-the-cloud.png'  # Assuming the image is in the same directory as the script
        file_analyzer_btn = Button(
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'x': 0.03, 'center_y': 0.73},
            background_normal=file_analyzer_image,
            background_down=file_analyzer_image
        )
        layout.add_widget(file_analyzer_btn)
        file_analyzer_btn.bind(on_release=self.on_file_analyzer_release)

        file_analyzer_label = Label(
            text="File Analyzer",
            size_hint=(None, 1),
            width=150,
            pos_hint={'x': 0.01, 'center_y': 0.66},
            color=(0, 0, 0, 1),
            font_size=16,
            halign='left'
        )
        layout.add_widget(file_analyzer_label)

        # Chatbot Assistant Button and Label
        chatbot_image = 'text.png'  # Assuming the image is in the same directory as the script
        chatbot_btn = Button(
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'x': 0.03, 'center_y': 0.49},
            background_normal=chatbot_image,
            background_down=chatbot_image,
            background_color=(1, 1, 1, 1)
        )
        layout.add_widget(chatbot_btn)
        chatbot_btn.bind(on_release=self.on_chatbot_btn_release)

        chatbot_label = Label(
            text="Chatbot Assistant",
            size_hint=(None, 1),
            width=150,
            pos_hint={'x': 0.01, 'center_y': 0.42},
            color=(0, 0, 0, 1),
            font_size=16,
            halign='left'
        )
        layout.add_widget(chatbot_label)

        self.border_box = BoxLayout(size_hint=(0.8, 0.8), pos_hint={'x': 0.18, 'y': 0.1})
        layout.add_widget(self.border_box)


        return layout

    def on_file_analyzer_release(self, instance):
        self.border_box.clear_widgets()
        llm_widget = LLMWidget()
        self.border_box.add_widget(llm_widget)

    def on_chatbot_btn_release(self, instance):
        self.border_box.clear_widgets()
        chatbot_widget = LLMChatbotWidget()
        self.border_box.add_widget(chatbot_widget)

if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (900, 600)
    SecureLLMApp().run()  # Updated the app instance creation here
