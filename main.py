from kivy.core.audio import SoundLoader
from packages.board_generator import generate
from packages.start_game import MainApp
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
import json

width = 600
height = 750
Config.set('graphics', 'width', str(width))
Config.set('graphics', 'height', str(height))

menu_change_sound = SoundLoader.load('sounds\menu_change.wav')
game_music = SoundLoader.load('sounds\game_music.mp3')
game_music.loop = True


class MainMenu(App):

    def __init__(self):
        super().__init__()

    def build(self):
        self.icon = r'files\icon.ico'
        game_music.play()
        layout = FloatLayout()
        with layout.canvas:
            Color(0.6, 1, 1, 1)
            Rectangle(pos=(0, 0), size=(10000, 10000))
        self.title = 'Word Puzzle'

        image = Image(source=r'images\title.png')
        image.y = 200
        layout.add_widget(image)

        def switch_difficulty(*arg):
            menu_change_sound.play()
            (difficulty_button.text,
             difficulty_button.background_color) = next_difficulty[difficulty_button.text]

        def play(*arg):
            menu_change_sound.play()
            self.stop()
            MainApp(difficulty_button.text).run()
            self.run()

        def show_high_score(*arg):
            layout.clear_widgets()
            exit_to_main_button = Button(
                text='Main Menu', font_name='font\gamefont.ttf', font_size=16,
                background_down=r'images\menu_texture_pressed.png', background_normal=r'images\menu_texture.png',
                background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=lambda _: (self.stop(), MainMenu().run()))
            exit_to_main_button.size_hint = ('.3', '.085')
            exit_to_main_button.pos_hint = {'x': 0.35, 'y': 0.15}
            file = open('highscores.json')
            scores = json.load(file)

            s = ''
            for difficulty in ['Easy', 'Normal', 'Hard', 'Impossible']:
                if difficulty in scores:
                    seconds = scores[difficulty]
                    min, sec = divmod(seconds, 60)
                    hr, min = divmod(min, 60)
                    s += f'\n\n{difficulty} - {hr:0>2}:{min:0>2}:{sec:0>2}'
                else:
                    s += f'\n\n{difficulty} - Nil'

            score = Label(text=s, color=(0.7, 0.2, 0.3, 1),
                          font_name='font/gamefont.ttf', font_size=32)
            score.pos_hint = {'x': 0, 'y': 0.3}
            with score.canvas:
                Color(0.6, 1, 1, 1)
                Rectangle(pos=score.pos, size=score.size)

            layout.add_widget(score)
            layout.add_widget(exit_to_main_button)

        def show_credits(*arg):
            layout.clear_widgets()
            exit_to_main_button = Button(
                text='Main Menu', font_name='font\gamefont.ttf', font_size=16,
                background_down=r'images\menu_texture_pressed.png', background_normal=r'images\menu_texture.png',
                background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=lambda _: (self.stop(), MainMenu().run()))
            exit_to_main_button.size_hint = ('.3', '.085')
            exit_to_main_button.pos_hint = {'x': 0.35, 'y': 0.15}

            s = '''
            Developer - Vigneswar A


            Program Used - Python (kivy)


            Sound Source - mixkit.co


            Images Software - GIMP


            Font Source - dafont.com
            '''
            credit = Label(text=s, color=(0.7, 0.2, 0.3, 1),
                           font_name='font/gamefont.ttf', font_size=20)

            credit.pos_hint = {'x': -0.1, 'y': 0.1}
            with credit.canvas:
                Color(0.6, 1, 1, 1)
                Rectangle(pos=credit.pos, size=credit.size)

            layout.add_widget(credit)
            layout.add_widget(exit_to_main_button)

        play_button = Button(
            text='Play', font_name='font\gamefont.ttf', font_size=16,
            background_down=r'images\menu_texture_pressed.png', background_normal=r'images\menu_texture.png',
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=play)
        play_button.size_hint = ('.3', '.085')
        play_button.pos_hint = {'x': 0.35, 'y': 0.55}

        next_difficulty = {'Easy': ('Normal', (0.9, 0.9, 0.2, 1)),
                           'Normal': ('Hard', (1, 0.1, 0.1, 1)),
                           'Hard': ('Impossible', (0.5, 0.1, 0.9, 1)),
                           'Impossible': ('Easy', (0, 0.8, 0, 1)), }

        difficulty_button = Button(
            text='Easy', font_name='font\gamefont.ttf', font_size=16,
            background_down=r'images\menu_texture_pressed.png', background_normal=r'images\menu_texture.png',
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=switch_difficulty)

        difficulty_button.size_hint = ('.3', '.085')
        difficulty_button.pos_hint = {'x': 0.35, 'y': 0.45}

        highscore_button = Button(
            text='High Score', font_name='font\gamefont.ttf', font_size=16,
            background_down=r'images\menu_texture_pressed.png', background_normal=r'images\menu_texture.png',
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=show_high_score)

        highscore_button.size_hint = ('.3', '.085')
        highscore_button.pos_hint = {'x': 0.35, 'y': 0.35}

        credits_button = Button(
            text='Credits', font_name='font\gamefont.ttf', font_size=16,
            background_down=r'images\menu_texture_pressed.png', background_normal=r'images\menu_texture.png',
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=show_credits)

        credits_button.size_hint = ('.3', '.085')
        credits_button.pos_hint = {'x': 0.35, 'y': 0.25}

        exit_button = Button(
            text='Exit', font_name='font\gamefont.ttf', font_size=16,
            background_down=r'images\menu_texture_pressed.png', background_normal=r'images\menu_texture.png',
            background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=self.stop)

        exit_button.size_hint = ('.3', '.085')
        exit_button.pos_hint = {'x': 0.35, 'y': 0.15}

        layout.add_widget(credits_button)
        layout.add_widget(exit_button)
        layout.add_widget(highscore_button)
        layout.add_widget(difficulty_button)
        layout.add_widget(play_button)
        return layout


MainMenu().run()
