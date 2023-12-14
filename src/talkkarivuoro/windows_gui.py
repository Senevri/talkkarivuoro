from datetime import timedelta
from decimal import Decimal
import toga
from talkkarivuoro.schedule_generator import generate_schedule as generate_ics_schedule
import logging
from toga.window import Dialog

from toga.style.pack import Pack, COLUMN, CENTER


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.warn = logger.warning


class TalkkarivuoroGUI(toga.App):
    _inputs = ()

    def startup(self):
        # Create the main window
        main_box = toga.Box(style=Pack(direction=COLUMN))
        input_container = toga.SplitContainer(style=Pack(flex=1))

        input_style = Pack(padding=8, height=24, font_size=12)

        # Create input fields
        start_date_input = toga.DateInput(style=input_style)
        num_turns_input = toga.NumberInput(
            min=Decimal(1), max=Decimal(100), style=input_style, value=Decimal(4)
        )
        time_step_input = toga.NumberInput(
            min=Decimal(1), max=Decimal(100), style=input_style, value=Decimal(12)
        )
        time_step_unit_input = toga.Selection(items=["Weeks", "Days"], style=input_style)
        event_name_input = toga.TextInput(value="Talkkarivuoro", style=input_style)

        _inputs = (
            start_date_input,
            num_turns_input,
            time_step_input,
            time_step_unit_input,
            event_name_input,
        )

        label_style = input_style.copy()
        label_style.color = "#333333"
        # Create labels
        labels = (
            toga.Label("Start Date:", style=input_style),
            toga.Label("Repeats:", style=input_style),
            toga.Label("Time Between Repeats:", style=input_style),
            toga.Label("Time Step:", style=input_style),
            toga.Label("Event Name:", style=input_style),
        )

        # Create a button to generate the schedule
        generate_button = toga.Button(
            "Generate Schedule",
            on_press=self.generate_schedule,
            style=Pack(
                width=200,
                height=50,
                font_size=20,
                background_color="#777777",
                color="#EEFFFE",
                padding=20,
                alignment=CENTER,
            ),
        )

        # Create a box for labels
        label_box = toga.Box(style=Pack(direction="column"))
        for label in labels:
            label_box.add(label)

        # Create a box for input fields and labels
        input_box = toga.Box(style=Pack(direction="column"))
        for input_dialog in _inputs:
            input_box.add(input_dialog)

        # Add the input box, label box, and button to the main box
        input_container.content = [label_box, input_box]
        main_box.add(input_container)
        main_box.add(generate_button)

        # Create a main window with the main box as its content
        # Create a main window with the main box as its content
        self.main_window = toga.MainWindow(title="Talkkarivuoro Schedule Generator")
        self.main_window.content = main_box
        self.main_window._inputs = _inputs

        self.main_window.show()

    async def save_file_dialog(self, widget: toga.Widget, **kwargs) -> Dialog:
        logger.info(kwargs)
        save_dialog = self.main_window.save_file_dialog(
            title="Save ICS File",
            suggested_filename="yard_maintenance_schedule.ics",
            file_types=["*.ics"],
        )
        return await save_dialog

    async def generate_schedule(self, widget: toga.Widget):
        logger.info(widget)
        splitcontainer_inputs = self.main_window._inputs
        start_date = splitcontainer_inputs[0].value
        num_turns = int(splitcontainer_inputs[1].value)
        time_step_count = splitcontainer_inputs[2].value
        time_step_type = splitcontainer_inputs[3].value
        event_name = splitcontainer_inputs[4].value

        time_step_params = {time_step_type.lower(): int(time_step_count)}
        timedelta()
        time_step = timedelta(**time_step_params)

        # Generate the schedule
        cal = generate_ics_schedule(
            start_date=start_date, num_turns=num_turns, time_step=time_step, event_name=event_name
        )

        save_dialog_path = await self.save_file_dialog(widget)
        logger.warning(save_dialog_path)
        if save_dialog_path:
            # Save the calendar to the selected location
            with open(str(save_dialog_path), "w") as f:
                f.writelines(cal.serialize())

            print(f"Yard maintenance schedule saved to {save_dialog_path}")
