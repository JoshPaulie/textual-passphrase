import pathlib
import random

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Static


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
        Binding("left,h", "navigate_passphrase_bank(-1)", "Previous", key_display="⬅ Left"),
        Binding("right,l", "navigate_passphrase_bank(1)", "Next/New", key_display="Right ➡"),
    ]
    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        self.passphrase_static = Static(id="PassphraseStatic")
        self.current_passphrase_n_static = Static(id="CurrentPassphraseNStatic")
        yield self.current_passphrase_n_static
        yield self.passphrase_static
        yield Footer()

    def on_mount(self):
        self.phrase_bank = []
        self.generated_passphrases = []
        self.current_passphrase = 0
        self.passphrase_phrase_len = 3

        phrase_file = pathlib.Path.home() / ".phrases"

        if phrase_file.exists():
            phrases = phrase_file.open().read().splitlines()
            self.phrase_bank.extend(clean_phrases(phrases))
            self.generated_passphrases.append(self.generate_passphrase())
            self.passphrase_static.update(self.generated_passphrases[self.current_passphrase])
        else:
            # Push no file found screen
            pass

        print(self.phrase_bank)

    def generate_passphrase(self):
        picked_phrases = []
        for _ in range(self.passphrase_phrase_len):
            unpicked_phrases = [phrase for phrase in self.phrase_bank if phrase not in picked_phrases]
            picked_phrases.append(random.choice(unpicked_phrases))
        return "-".join(picked_phrases)

    def action_navigate_passphrase_bank(self, move_amt: int) -> None:
        # todo: Make this into match case
        if move_amt < 0 and self.current_passphrase <= 0:
            return

        if move_amt > 0 and self.current_passphrase == len(self.generated_passphrases) - 1:
            self.generated_passphrases.append(self.generate_passphrase())

        self.current_passphrase += move_amt

        self.passphrase_static.update(self.generated_passphrases[self.current_passphrase])
        self.current_passphrase_n_static.update(f"({self.current_passphrase + 1}/{len(self.generated_passphrases)})")
