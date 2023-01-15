import pathlib
import random

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Input, Label, Static


class NumberSelector(Static):
    def compose(self):
        self.value = 0

        self.value_label = Label(str(self.value))
        self.inc_button = Button("+", id="inc")
        self.dec_button = Button("-", id="dec")
        yield Horizontal(
            self.dec_button,
            self.value_label,
            self.inc_button,
        )

    def on_mount(self):
        self.value_label.styles.width = "1fr"
        self.value_label.styles.text_align = "center"
        self.inc_button.styles.width = "1fr"
        self.dec_button.styles.width = "1fr"


def clean_phrases(phrases: list[str]) -> list[str]:
    phrases = [phrase for phrase in phrases if phrase]
    phrases = [phrase for phrase in phrases if not phrase.startswith("#")]
    return phrases


class NoDotPhrases(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Static("...")  # todo


class PassphraseApp(App):

    BINDINGS = [
        Binding("space,enter", "generate_passphrase", "New Passphrase", key_display="•"),
    ]
    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        self.passphrase_static = Static("Textual-Passphrase-Generator", id="PassphraseStatic")
        yield Horizontal(
            self.passphrase_static,
            id="PassphraseHorizontal",
        )
        yield Horizontal(
            Vertical(
                Label("Include digit", classes="PassphraseOptionLabel"),
                Checkbox(),
                classes="PassphraseOptionGroup",
            ),
            Vertical(
                Label("Titlecase", classes="PassphraseOptionLabel"),
                Checkbox(),
                classes="PassphraseOptionGroup",
            ),
            Vertical(
                Label("Seperator", classes="PassphraseOptionLabel"),
                Input(value="-", placeholder="-", id="PassphraseSeperatorInput"),
                classes="PassphraseOptionGroup",
            ),
            Vertical(
                Label("Phrase length", classes="PassphraseOptionLabel"),
                NumberSelector(),
                classes="PassphraseOptionGroup",
            ),
        )
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
