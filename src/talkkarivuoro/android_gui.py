from decimal import Decimal
import toga
from talkkarivuoro.schedule_generator import generate_schedule as generate_ics_schedule
import logging
from toga.window import Dialog
import tempfile
import webbrowser
import jpype

# import jnius
from toga.style.pack import Pack, COLUMN
from datetime import timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.warn = logger.warning


class TalkkarivuoroGUI(toga.App):
    def startup(self):
        # Create the main window
        main_box = toga.Box(style=Pack(direction=COLUMN))

        input_style = Pack(padding=10)

        # Create input fields
        start_date_input = toga.DateInput(style=input_style)
        num_turns_input = toga.NumberInput(
            min=Decimal(1), max_value=Decimal(100), style=input_style, value=Decimal(4)
        )
        time_step_input = toga.NumberInput(
            min=Decimal(1), max_value=Decimal(100), style=input_style, value=Decimal(12)
        )
        time_step_unit_input = toga.Selection(items=["Weeks", "Days"], style=input_style)
        event_name = toga.TextInput(style=input_style, value="Talkkarivuoro")

        # Create labels
        labels = (
            toga.Label("Start Date:", style=input_style),
            toga.Label("Repeats:", style=input_style),
            toga.Label("Time Between Repeats:", style=input_style),
            toga.Label("Time Step:", style=input_style),
            toga.Label("Event Name", style=input_style),
        )

        # Create a button to generate the schedule
        generate_button = toga.Button("Generate Schedule", on_press=self.generate_schedule)

        # Add the input fields, labels, and button to the main box
        main_box.add(labels[0])
        main_box.add(start_date_input)
        main_box.add(labels[1])
        main_box.add(num_turns_input)
        main_box.add(labels[2])
        main_box.add(time_step_input)
        main_box.add(labels[3])
        main_box.add(time_step_unit_input)
        main_box.add(labels[4])
        main_box.add(event_name)
        main_box.add(generate_button)

        # Create a main window with the main box as its content
        self.main_window = toga.MainWindow(title="Talkkarivuoro Schedule Generator")
        self.main_window.content = main_box
        self.main_window.show()

    # async def save_file_dialog(self, widget: toga.Widget, **kwargs) -> str:
    #     logger.info(kwargs)
    #     save_dialog = self.main_window.android.open_file_dialog(
    #         title="Save ICS File",
    #         suggested_filename="yard_maintenance_schedule.ics",
    #         file_types=[("ICS Files", "*.ics")],
    #         select_folder=False,
    #         save=True,
    #     )
    #     save_dialog.show()

    #     if save_dialog.path:
    #         return save_dialog.path
    #     else:
    #         return ""

    async def generate_schedule(self, widget: toga.Widget):
        logger.info(widget)
        start_date = self.main_window.content.children[1].value
        num_turns = self.main_window.content.children[3].value
        time_step_int = int(self.main_window.content.children[5].value)
        time_step_unit = self.main_window.content.children[7].value
        event_name = self.main_window.content.children[9].value

        # Convert time_step to timedelta based on the selected unit
        if time_step_unit == "Days":
            time_step = timedelta(days=time_step_int)
        else:
            time_step = timedelta(weeks=time_step_int)

        # Generate the schedule
        cal = generate_ics_schedule(
            start_date=start_date,
            num_turns=int(num_turns),
            time_step=time_step,
            event_name=event_name,
        )
        self.share_ics(cal)

    def share_ics(self, cal):
        # Generate the ICS file

        ics_content = cal.serialize()

        # Save the ICS file to a temporary location
        temp_file_path = tempfile.mktemp(suffix=".ics")
        with open(temp_file_path, "w") as f:
            f.write(ics_content)

        jpype.startJVM(jpype.getDefaultJVMPath())
        try:
            # Get the Android classes
            Intent = jpype.JClass("android.content.Intent")
            Uri = jpype.JClass("android.net.Uri")

            # Create the intent
            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/calendar")
            intent.set
            inptent.putExtra(Intent.EXTRA_SUBJECT, "My Schedule")
            intent.putExtra(Intent.EXTRA_TEXT, ics_content)

            # Launch the share dialog
            jpype.JClass("android.content.Context").getApplicationContext().startActivity(
                Intent.createChooser(intent, "Share")
            )

        finally:
            jpype.ShutdownJVM()
