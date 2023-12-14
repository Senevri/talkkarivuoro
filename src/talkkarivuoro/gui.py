import toga
import logging
import toga.platform

platform = toga.platform.get_current_platform()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.warn = logger.warning


if platform == "windows":
    from talkkarivuoro.windows_gui import TalkkarivuoroGUI
else:
    from talkkarivuoro.android_gui import TalkkarivuoroGUI
