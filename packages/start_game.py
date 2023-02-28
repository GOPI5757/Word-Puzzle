from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from packages.board_generator import generate
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from functools import partial
from kivy.core.text import FontContextManager as FCM
from kivy.graphics import Color, Rectangle
import threading
import time
import json

grid_color = (0.6, 1, 1, 1)
word_color = (0.7, 0.9, 0.3, 1)
width = 600
height = 750
Config.set('graphics', 'width', str(width))
Config.set('graphics', 'height', str(height))
match_sound = SoundLoader.load('sounds\match_sound.wav')
wrong_sound = SoundLoader.load('sounds\wrong_sound.wav')
win_sound = SoundLoader.load('sounds\win_sound.wav')


class MainApp(App):
    def __init__(self, difficulty, /, *args, **kwargs):
        self.difficulty = difficulty
        self.word_count, self.size = {'Easy': (10, 7), 'Normal': (
            15, 10), 'Hard': (25, 15), 'Impossible': (40, 25)}[self.difficulty]
        self.press_handler = None
        self.title = 'Word Puzzle'
        self.timer_running = True
        super().__init__(*args, **kwargs)
        self.ender = None
        self.seconds = 0

    def on_stop(self):
        self.timer_running = False
        return super().on_stop()

    def build(self):
        self.icon = r'files\icon.ico'
        layout = BoxLayout(orientation='vertical')
        board, words = generate(self.size, self.word_count)

        self.score_display = BoxLayout()
        self.score_display.size_hint = (1, 0.1)
        time_display = Button(font_name='font\gamefont.ttf',
                              text='Time: 00:00:00', background_disabled_normal='', color=(1, 1, 1, 1), background_color=(0, 0, 0, 1), font_size=16, background_normal='')
        self.score_display.add_widget(time_display)
        self.timer_running = True
        layout.add_widget(self.score_display)
        score = 0

        def timer():
            while self.timer_running:
                self.seconds += 1
                time.sleep(1)
                mins, sec = divmod(self.seconds, 60)
                hour, mins = divmod(mins, 60)
                time_display.text = f'Time: {hour:0>2}:{mins:0>2}:{sec:0>2}'

        def scored():
            nonlocal score
            score += 1

        self.score_function = scored
        threading.Thread(target=timer).start()
        self.press_handler = PressHandler(self)
        self.game_board = GameBoard(board, self.press_handler)
        self.words_display = GridLayout(cols=5, rows=10)
        self.words_display.size_hint = (1, 0.2)
        label_dict = {}
        self.added_words = {}
        for key, word in words.items():
            if word not in label_dict:
                label_dict[word] = Button(
                    font_name='font\gamefont.ttf', disabled=True, background_disabled_normal=r'images\word_texture.png', text=word, border=(1, 1, 1, 1), disabled_color=(0, 0, 0, 1), background_color=word_color, font_size=10)
                self.words_display.add_widget(label_dict[word])
            self.added_words[key] = label_dict[word]

        layout.add_widget(self.game_board)
        layout.add_widget(self.words_display)

        def end():
            try:
                highscores = json.load(open(r'files\highscores.json', 'r'))
            except:
                highscores = {}

            if self.difficulty not in highscores:
                highscores[self.difficulty] = self.seconds
            else:
                highscores[self.difficulty] = min(
                    self.seconds, highscores[self.difficulty])

            json.dump(highscores, open(r'files\highscores.json', 'w'))
            layout.clear_widgets()
            with layout.canvas:
                Color(0.6, 1, 1, 1)
                Rectangle(pos=(0, 0), size=(10000, 10000))

            score = Button(font_name='font\gamefont.ttf',
                           font_size=36,
                           text=f'You have completed\n\n   the word puzzle\n\n  in {time_display.text}!',
                           background_color=(0, 0, 0, 0),
                           color=(0, 0, 0, 1))
            exit_to_main = Button(
                text='Exit', font_name='font\gamefont.ttf', font_size=16,
                background_down=r'images\menu_texture_pressed.png', background_normal=r'images\menu_texture.png',
                background_color=(0, 0.8, 0, 1), border=(1, 1, 1, 1), color=(0, 0, 0, 1), on_press=self.stop)

            exit_to_main.size_hint = ('.2', '.1')
            exit_to_main.pos_hint = {'x': 0.4}
            layout.add_widget(score)
            layout.add_widget(exit_to_main)

        self.ender = end
        return layout


class PressHandler:
    def __init__(self, parent: MainApp):

        self.first_click = False
        self.first_coord = None
        self.parent = parent
        self.completed = set()
        self.found_words = set()
        self.word_count = None

    def __call__(self, i, j, button):
        if self.word_count is None:
            self.word_count = len(set(self.parent.added_words.values()))

        if (i, j) in self.completed:
            return
        if not self.first_click:
            self.first_click = True
            self.first_coord = (i, j)
            self.parent.game_board.board[i][j].background_color = (
                0.1, 0.8, 1, 1)
            return

        self.first_click = False
        key = (self.first_coord, (i, j))
        if key in self.parent.added_words and self.parent.added_words[key] not in self.found_words:
            match_sound.play()
            self.parent.score_function()
            self.found_words.add(self.parent.added_words[key])
            self.parent.added_words[key].background_color = (0, 1, 0, 1)
            (x, y), (ex, ey) = key
            length = len(self.parent.added_words[key].text)
            ox, oy = (ex-x)//(length-1), (ey-y)//(length-1)
            for i in range(length):
                self.parent.game_board.board[x
                                             + ox*i][y+oy*i].background_color = (0, 1, 0, 1)
                self.completed.add((x+ox*i, y+oy*i))

            if len(self.found_words) == self.word_count:
                win_sound.play()
                self.parent.ender()

        else:
            def color_switch(ax, ay, bx, by):
                self.parent.game_board.board[ax][ay].background_color = (
                    1, 0, 0, 1)
                self.parent.game_board.board[bx][by].background_color = (
                    1, 0, 0, 1)
                time.sleep(0.25)
                self.parent.game_board.board[ax][ay].background_color = grid_color
                self.parent.game_board.board[bx][by].background_color = grid_color

            switch_effect = threading.Thread(target=partial(
                color_switch, i, j, self.first_coord[0], self.first_coord[1]))
            switch_effect.start()
            wrong_sound.play()


class GameBoard(GridLayout):
    def __init__(self, board, pressed, **kwargs):
        super().__init__(**kwargs)
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = Button(
                    text=self.board[i][j], on_press=partial(pressed, i, j), font_name=r'font\gamefont.ttf',
                    font_size=18, color=(0, 0, 0, 1), background_normal=r'images\board_texture.png', background_color=(0.6, 1, 1, 1), background_down=r'images\board_texture_pressed.png', border=(0, 0, 0, 0))
                self.add_widget(self.board[i][j])
