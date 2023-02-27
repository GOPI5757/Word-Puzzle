from kivy.core.audio import SoundLoader
from start_game import MainApp
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.image import Image

width = 600
height = 750
Config.set('graphics', 'width', str(width))
Config.set('graphics', 'height', str(height))

menu_change_sound = SoundLoader.load("menu_change.wav")


class MainMenu(App):

    def __init__(self):
        self.difficultymap = {"Easy": (10, 7), "Normal": (
            15, 10), "Hard": (25, 15), "Impossible": (40, 25)}
        super().__init__()

    def build(self):
        layout = FloatLayout()
        with layout.canvas:
            Color(0.6, 1, 1, 1)
            Rectangle(pos=(0, 0), size=(10000, 10000))
        self.title = 'Word Puzzle'

        image = Image(source='title.png')
        image.y = 200
        layout.add_widget(image)

        def switch_difficulty(*arg):
            menu_change_sound.play()
            (difficulty_button.text,
             difficulty_button.background_color) = next_difficulty[difficulty_button.text]

        def play(*arg):
            menu_change_sound.play()
            self.stop()
            n, size = self.difficultymap[difficulty_button.text]
            MainApp(n, size).run()
            self.run()

        play_button = Button(
            text="Play", font_name="font\gamefont.ttf", font_size=16,
            background_down="menu_texture_pressed.png", background_normal="menu_texture.png",
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=play)
        play_button.size_hint = ('.25', '.085')
        play_button.pos_hint = {'x': 0.35, 'y': 0.55}

        next_difficulty = {"Easy": ("Normal", (0.9, 0.9, 0.2, 1)),
                           "Normal": ("Hard", (1, 0.1, 0.1, 1)),
                           "Hard": ("Impossible", (0.5, 0.1, 0.9, 1)),
                           "Impossible": ("Easy", (0, 0.8, 0, 1)), }

        difficulty_button = Button(
            text="Easy", font_name="font\gamefont.ttf", font_size=16,
            background_down="menu_texture_pressed.png", background_normal="menu_texture.png",
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=switch_difficulty)

        difficulty_button.size_hint = ('.25', '.085')
        difficulty_button.pos_hint = {'x': 0.35, 'y': 0.45}

        highscore_button = Button(
            text="High Score", font_name="font\gamefont.ttf", font_size=16,
            background_down="menu_texture_pressed.png", background_normal="menu_texture.png",
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1))

        highscore_button.size_hint = ('.25', '.085')
        highscore_button.pos_hint = {'x': 0.35, 'y': 0.35}

        exit_button = Button(
            text="Credits", font_name="font\gamefont.ttf", font_size=16,
            background_down="menu_texture_pressed.png", background_normal="menu_texture.png",
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1))

        exit_button.size_hint = ('.25', '.085')
        exit_button.pos_hint = {'x': 0.35, 'y': 0.25}

        layout.add_widget(exit_button)
        layout.add_widget(highscore_button)
        layout.add_widget(difficulty_button)
        layout.add_widget(play_button)
        return layout


MainMenu().run()
