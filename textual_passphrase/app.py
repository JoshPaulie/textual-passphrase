import pathlib
import random

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import *
from textual.screen import Screen
from textual.widgets import Checkbox, Footer, Static


def clean_phrases(phrases: list[str]) -> list[str]:
    phrases = [phrase.title() for phrase in phrases]
    phrases = [phrase for phrase in phrases if phrase]
    phrases = [phrase for phrase in phrases if not phrase.startswith("#")]
    return phrases


class NoDotPhrases(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Static("...")  # todo


class PassphraseApp(App):

    BINDINGS = [
        Binding("space,enter", "generate_passphrase", "New Passphrase", key_display="Spacebar | Enter"),
    ]
    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        self.passphrase_static = Static("Textual-Passphrase-Generator", id="PassphraseStatic")
        yield self.passphrase_static
        yield Footer()

    def on_mount(self):
        self.phrase_bank = []
        self.current_passphrase = ""

        self.passphrase_sep = "-"
        self.passphrase_phrase_len = 3
        self.passphrase_titlecase = True

        phrase_file = pathlib.Path.home() / ".phrases"

        if phrase_file.exists():
            phrases = phrase_file.open().read().splitlines()
            self.phrase_bank.extend(clean_phrases(phrases))
        else:
            # Push no file found screen
            # Close app
            pass

        self.action_generate_passphrase()

    def action_generate_passphrase(self) -> None:
        picked_phrases: list[str] = []
        for _ in range(self.passphrase_phrase_len):
            unpicked_phrases = [phrase for phrase in self.phrase_bank if phrase not in picked_phrases]
            picked_phrases.append(random.choice(unpicked_phrases))

        if self.passphrase_titlecase:
            picked_phrases = [phrase.title() for phrase in picked_phrases]

        passphrase = self.passphrase_sep.join(picked_phrases)
        self.current_passphrase = passphrase
        self.passphrase_static.update(passphrase)
