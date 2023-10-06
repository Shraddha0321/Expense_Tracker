import flet
from flet import *
import datetime
from math import pi

from pyparsing import White


def create_dark_gradient():
    gradient = LinearGradient(
        begin=alignment.top_center,
        end=alignment.bottom_center,
        colors=[
            "#ffffff",
        ],
    )
    return gradient


class Button(UserControl):
    def __init__(self, entry_form):
        self.entry_form = entry_form
        self.btn = FloatingActionButton(
            content=Icon(
                name=icons.ADD,
                size=18,
                color=colors.WHITE,
                animate_rotation=animation.Animation(600, "easeOutBack"),
            ),
            bottom=0,
            right=0,
            width=42,
            height=42,
            shape=CircleBorder(),
            offset=transform.Offset(-0.5, -0.5),
            bgcolor="white",
            on_click=lambda e: self.show_hide_entry_form(e),
        )
        super().__init__()

    def show_hide_entry_form(self, e: ContainerTapEvent):
        if self.entry_form.height == 0:
            self.entry_form.height = 200
            self.btn.content.rotate = transform.Rotate(pi / 4)
        else:
            self.entry_form.height = 0
            self.btn.content.rotate = transform.Rotate(0)

        self.btn.content.update()
        self.entry_form.update()

    def build(self):
        return self.btn


class MainContent(UserControl):
    def __init__(self):
        self.body = Container(
            width=270,
            height=550,
            border_radius=35,
            border=border.all(5, colors.WHITE),
            padding=padding.only(left=15, top=25, right=15, bottom=10),
            gradient=LinearGradient(
                begin=alignment.top_center,
                end=alignment.bottom_center,
                colors=["#a64d79", "#a64d79", "#a64d79", "#a64d79"],
            ),
            clip_behavior=ClipBehavior.HARD_EDGE,
        )

        self.main_stack = Stack()
        self.card_row = Row(scroll="hidden")
        self.recent_activity_column = Column(scroll="hidden", expand=True)

        self.entry_form = Container(
            width=270,
            height=0,
            margin=margin.only(left=-15, right=-15, top=-25, bottom=25),
            bgcolor="#a64d79",
            animate=animation.Animation(300, "decelerate"),
            alignment=alignment.center,
            content=Text(
                "FORM ENTRY HERE",
            ),
        )

        self.generate_card_txns()
        self.generate_recent_activity()
        super().__init__()

    def set_entry_form(self):
        self.main_stack.controls.append(self.entry_form)

    def set_card_text(self, value, size, color):
        return Text(value=value, size=size, color=color, weight="bold")

    def generate_card_txns(self):
        # Define the place, price, and card lists
        place = ["Pharmacy", "Netflix Co.", "Store"]
        price = ["15000", "10000", "8000"]
        card = ["Credit Card - 2103", "Debit Card - 0321", "Debit Card - 0321"]

        # Create a list of three dictionaries, each representing a card transaction
        transactions = [
            {
                "time": datetime.datetime.now().strftime("%H:%M"),
                "place": place[i],
                "price": price[i],
                "card": card[i],
            }
            for i in range(3)
        ]

        # Create a list of Container objects using list comprehension
        container_list = [
            Container(
                width=200,
                height=220,
                border_radius=15,
                padding=20,
                gradient=create_dark_gradient(),
                content=Column(
                    spacing=4,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.set_card_text(transaction["time"], 10, "black"),
                        self.set_card_text(transaction["place"], 13, "black"),
                        Divider(height=80, color="white"),
                        self.set_card_text(transaction["price"], 20, "black"),
                        self.set_card_text(transaction["card"], 9, "black"),
                    ],
                ),
            )
            for transaction in transactions
        ]
        self.card_row.controls = container_list

    def generate_recent_activity(self):
        label = ["Housing", "Travelling", "Group Expenses 2023"]
        misc = ["s.expense@gmail.com", "k@hh.com", "sgroup@gmail.com"]

        items = [
            Container(
                width=260,
                height=55,
                bgcolor="#ffffff",
                padding=10,
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        Text(label[i], color="black", weight="bold", size=11),
                        Text(misc[i], color="#333333", weight="bold", size=8),
                    ],
                ),
            )
            for i in range(3)
            for i in range(3)
        ]

        self.recent_activity_column.controls = items

    def build(self):
        items: list = [
            Column(
                controls=[
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text("Expense Tracker", color="white", size=20, weight="w600"),
                            Icon(
                                name=icons.MORE_HORIZ_ROUNDED,
                                color="white",
                                rotate=transform.Rotate(pi / 2),
                            ),
                        ],
                    ),
                    Row(
                        controls=[
                            Text(
                                "Todays Transactions",
                                color="white",
                                size=11,
                                weight="bold",
                            )
                        ],
                    ),
                    Divider(height=5, color="transparent"),
                    self.card_row,
                    Divider(height=5, color="transparent"),
                    Row(
                        controls=[
                            Text(
                                "Recent Activity", color="white", size=15, weight="bold"
                            )
                        ],
                    ),
                    self.recent_activity_column,
                ],
            ),
            self.entry_form,
        ]
        self.main_stack.controls = items
        self.body.content = self.main_stack
        return self.body


def main(page: Page):
    # page settings
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    # page.padding = padding.only(right=100)
    page.bgcolor = "#212328"

    # create instances
    main = MainContent()
    btn = Button(main.entry_form)

    # add controls
    page.add(
        Stack(
            width=270,
            height=550,
            clip_behavior=ClipBehavior.HARD_EDGE,
            controls=[main, btn],
        )
    )

    # refresh page
    page.update()


if __name__ == "__main__":
    flet.app(target=main)
