import os
import random
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from dotenv import load_dotenv
from kivy.core.window import Window

load_dotenv()

Config.set("graphics", "resizable", True)

Window.maximize()


def shuffle_and_copy_file(src, dst):
    with open(src, "r") as f:
        lines = f.readlines()

    random.shuffle(lines)

    with open(dst, "w") as f:
        f.write("".join(lines))


class WindowManager(ScreenManager):
    pass


class MenuWindow(Screen):
    pass


class ExamWindow(Screen):
    def __init__(
        self,
        **kw,
    ):
        super().__init__(**kw)

        self.dir = os.path.split(os.path.abspath(__file__))[0]

        q_file = "questions/questions.txt" if os.getenv("Q_FILE") is None else os.getenv("Q_FILE")
        save_file = "questions/save.txt" if os.getenv("SAVE_FILE") is None else os.getenv("SAVE_FILE")
        self.q_file = os.path.join(self.dir, q_file)
        self.save_file = os.path.join(self.dir, save_file)
        
        self.media_path = os.path.join(self.dir, "media")

        self.question = ""
        self.answer = ""

    def on_enter(self):
        if not os.path.exists(self.q_file):
            shuffle_and_copy_file(self.save_file, self.q_file)
        else:
            shuffle_and_copy_file(self.q_file, self.q_file)

        with open(self.q_file, "r") as f:
            try:
                line = f.readline().split(":")
                self.question = line[0].strip("(")
                self.answer = line[1].strip(")")
            except:
                self.question = ""
                self.answer = ""

        self.ids["question_label"].text = f"Question: {self.question}"

    def check_answer(self):
        self.ids.input.text = f"Answer: {self.answer}"
        self.ids["submit"].disabled = True

        self.box = BoxLayout(orientation="horizontal")
        self.ids["top_level"].add_widget(self.box)
        self.box1 = BoxLayout()
        self.box2 = BoxLayout()
        self.box.add_widget(self.box1)
        self.box.add_widget(self.box2)

        self.thumbs_up = self.box1.add_widget(
            Button(
                background_normal=f"{self.media_path}/thumbs_up.png",
                on_release=self.correct_answer,
            )
        )
        self.thumbs_down = self.box2.add_widget(
            Button(
                background_normal=f"{self.media_path}/thumbs_down.png",
                on_release=self.wrong_answer,
            )
        )

    def wrong_answer(self, _):
        with open(self.q_file, "a") as f:
            f.write(f"{self.question}:{self.answer}")

        with open(self.q_file, "r") as fin:
            data = fin.readlines()
        with open(self.q_file, "w") as fout:
            fout.writelines(data[1:])

        with open(self.q_file, "r") as f:
            try:
                line = f.readline().split(":")
                self.question = line[0].strip("(")
                self.answer = line[1].strip(")")
            except:
                self.question = ""
                self.answer = ""

        self.ids["question_label"].text = f"Question: {self.question}"

        self.ids["input"].text = ""

        count = str(int(self.ids["incorrect"].text.split(":")[1]) + 1)
        self.ids["incorrect"].text = f"Incorrect: {count}"

        self.ids["top_level"].remove_widget(self.box)

        self.ids["submit"].disabled = False

    def correct_answer(self, _):
        with open(self.q_file, "r") as fin:
            data = fin.readlines()
        with open(self.q_file, "w") as fout:
            fout.writelines(data[1:])

        if os.path.getsize(self.q_file) == 0:
            content = GridLayout(cols=1, padding=10)
            content.add_widget(
                Label(text="You have answered all the questions correctly!")
            )
            btn = Button(
                text="Close",
            )
            content.add_widget(btn)

            popup = Popup(
                title="Congratulations",
                content=content,
                auto_dismiss=False,
            )
            btn.bind(on_press=popup.dismiss)
            popup.open()
            shuffle_and_copy_file(self.save_file, self.q_file)

        with open(self.q_file, "r") as f:
            try:
                line = f.readline().split(":")
                self.question = line[0].strip("(")
                self.answer = line[1].strip(")")
            except:
                self.question = ""
                self.answer = ""

        self.ids["question_label"].text = f"Question: {self.question}"

        self.ids["input"].text = ""

        count = str(int(self.ids["correct"].text.split(":")[1]) + 1)
        self.ids["correct"].text = f"Correct: {count}"

        self.ids["top_level"].remove_widget(self.box)

        self.ids["submit"].disabled = False


kv = Builder.load_file("gui.kv")


class Exam(App):
    def build(self):
        return kv


if __name__ == "__main__":
    Exam().run()
