from textual import log
from textual.app import App, ComposeResult
from textual.containers import Container, Content
from textual.events import Blur, Focus, Mount, Unmount
from textual.message import MessageTarget
from textual.reactive import reactive
from textual.widgets import Footer, Header, Input, Static

from formulae import calculate


class HelloDisplay(Static):
    msg = reactive("")
    weight = reactive("")
    hydration = reactive("")

    def update_message(self, msg):
        self.msg = msg


class SourdoughCalculator(App):
    """A Textual app to calculate sourdough bread weights."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("escape", "unfocus", "Unfocus")]
    WEIGHT = 1000
    HYDRATION = 70
    SALT = 2
    STARTER = 20
    STARTER_HYDRATION = 100

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            Static("Weight"),
            Input("1000", id="weight_in"),
            Static("Hydration %"),
            Input("70", id="hydration_in"),
            Static("Salt %"),
            Input("2", id="salt_in"),
            Static("Starter %"),
            Input("20", id="starter_in"),
            Static("Starter Hydration %"),
            Input("100", id="starter_hydration_in"),
            Static("Final Recipe:"),
            Content(HelloDisplay()),
        )
        self.dark = False

    def action_toggle_dark(self) -> None:
        self.dark: bool = not self.dark

    async def action_unfocus(self):
        await self.query_one("#weight_in").post_message(Blur(self))
        await self.query_one(Footer).post_message(Focus(self))

    def generate_recipie(self) -> str:
        recipie = calculate(
            target_weight=float(self.WEIGHT),
            hydration_pct=float(self.HYDRATION),
            salt_pct=float(self.SALT),
            starter_pct=float(self.STARTER),
            starter_hydration=float(self.STARTER_HYDRATION),
        )
        recipe_str = (
            f"Flour: {recipie.flour} | "
            f"Water: {recipie.water} | "
            f"Starter: {recipie.starter} | "
            f"Salt: {recipie.salt}"
        )
        return recipe_str

    def on_input_submitted(self, event: Input.Submitted) -> None:
        event_id = event.input.id
        if event_id == "weight_in":
            self.WEIGHT = event.value
        if event_id == "hydration_in":
            self.HYDRATION = event.value
        if event_id == "salt_in":
            self.SALT = event.value
        if event_id == "starter_in":
            self.STARTER = event.value
        if event_id == "starter_hydration_in":
            self.STARTER_HYDRATION = event.value
        recipe_str = self.generate_recipie()
        self.query_one(HelloDisplay).update(recipe_str)

    def on_mount(self):
        recipe_str = self.generate_recipie()
        self.query_one(HelloDisplay).update(recipe_str)


if __name__ == "__main__":
    app = SourdoughCalculator()
    app.run()
