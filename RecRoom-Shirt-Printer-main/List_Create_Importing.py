import numpy as np


try:
    import ctypes
    import time
    from typing import Tuple, List

    import pyautogui
    import pyperclip
    from PIL import ImageGrab
    import cv2

    import Encoding
    from common import setup_logger, is_window_active, color_in_coords
except Exception as e:
    exit(input(f"ERROR: {e}"))

done_button_ref = cv2.imread("done_button_original.png")
SCREEN_DIMENSIONS = []


def monitor_check():
    global SCREEN_DIMENSIONS
    # Check if the users monitor is 1440p or 1080p
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    SCREEN_DIMENSIONS = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if round(SCREEN_DIMENSIONS[0] / SCREEN_DIMENSIONS[1], 2) != 1.78:
        return -1
    return 1


Coords = Tuple[int, int]

# Set this to false if you don't want color checking,
# or if you're not in the `ListCreateImporting` room
color_checking: bool = True


def copy_to_recroom(img_data: list[str], delay: float = 0.3, last_successful_string: str or None = None,
                    ask_to_continue: bool = True) -> None:
    """
    Function copies 512 char string into RecRoom List Creates.

    :param img_data: A list of strings of color data for each pixel
    :param delay: The main delay between actions
    :param last_successful_string: The last successfully copied string.
           Useful if importing fails somewhere in the middle
    :param ask_to_continue: Ask the user for input before starting copying
    """
    window_title = "Rec Room"
    num_strings = len(img_data)
    monitor_check()

    # Coordinates for all the buttons
    input_field: Coords = (int(SCREEN_DIMENSIONS[0] * 0.5), int(SCREEN_DIMENSIONS[1] * 0.34))
    

    color_checking_coords: List[Tuple[int, int]] = [(int(SCREEN_DIMENSIONS[0] * 0.25),
                                                     int(SCREEN_DIMENSIONS[1] * 0.5)),
                                                    (int(SCREEN_DIMENSIONS[0] * 0.35),
                                                     int(SCREEN_DIMENSIONS[1] * 0.5) + 5)]

    if ask_to_continue:
        if "n" in input(f"\nProceed to copy all {num_strings} strings to {window_title}? [y/n] ").lower():
            return
    time_at_start = time.time()

    for num, string in enumerate(img_data):
        # Every loop check if RecRoom is the window in focus.
        is_window_active(window_title)

        if last_successful_string:
            # `last_successful_string` is not None
            if last_successful_string in string:
                # `last_successful_string` is in the current string -> set the var. to None
                last_successful_string = None
            else:
                # `last_successful_string` is not in the current string -> move to the next string
                continue
        else:
            # `last_successful_string` is None -> user did not enter any string to continue from
            pass

        # Copy current string into clipboard
        pyperclip.copy(string)
        print(f"Copying string #{num + 1}/{num_strings}")
        time.sleep(delay)

        for _ in range(10):
            # Click `List Create` string entry
            pyautogui.click()
            time.sleep(delay)

            # Click on the input field
            pyautogui.click(input_field)
            time.sleep(delay / 2)

            # Paste the string into input field
            pyautogui.hotkey("ctrl", "v")
            time.sleep(delay)

            # Click "Done"
            try:
            # Use image recognition to find the "Done" button's coordinates
                screenshot = ImageGrab.grab()
                screenshot_cv2 = np.array(screenshot)
                screenshot_cv2 = cv2.cvtColor(screenshot_cv2, cv2.COLOR_RGB2BGR)
                
                match = cv2.matchTemplate(screenshot_cv2, done_button_ref, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                button_x, button_y = max_loc

                # Calculate button center coordinates
                button_width, button_height = done_button_ref.shape[1], done_button_ref.shape[0]
                center_x = button_x + button_width // 2
                center_y = button_y + button_height // 2
                pyautogui.click(center_x, center_y)

                # Click the button using the found coordinates
                print(f"Clicking button at coordinates: {button_x}, {button_y}")
                pyautogui.click(button_x, button_y)
                pyautogui.click(161, 427)
                
                
            except Exception as e:
             print(f"Image recognition failed: {e}")
            time.sleep(delay)


            # Exit out of the input field menu
            pyautogui.press("esc")
            time.sleep(delay / 2)

            if color_checking:
                color_check_image = ImageGrab.grab()
                # Check for `purple` (string input background)
                if color_in_coords(image=color_check_image,
                                   color=(157, 145, 187),
                                   coordinates=color_checking_coords,
                                   tolerance=60):
                    break
                print("Failed")
                # time.sleep(delay)
            else:
                break

        # Move down using trigger handle in right hand
        pyautogui.click(button='right')
        time.sleep(delay / 3)

    # Print out the time used for importing
    time_to_copy = time.time() - time_at_start
    minutes = time_to_copy // 60
    seconds = time_to_copy % 60
    print(f"Copying complete. Copied {num_strings} strings in {minutes} min and {seconds:.1f} sec")


def main(from_file: bool = False):
    if monitor_check() == -1:
        exit(input("\nScreen aspect ratio not optimal for importing.\n"
                   "Press enter to exit\n"
                   "> "))
    if not from_file:
        # Call function for encoding an image
        image, img_data = Encoding.main(list_size=64)
    else:
        try:
            with open("image_data.txt", "r", encoding="UTF-8") as f:
                temp: list[str] = f.readlines()
                img_data = [line.strip() for line in temp]
        except FileNotFoundError:
            print("The file `image_data.txt` was not found. ")
            image, img_data = Encoding.main(list_size=64)

    "########### GLOBAL IMPORTING DELAY ############"
    # This is the delay that controls the speed of the importing process
    # If you're experiencing miss-input/failed string input, increase this number
    # Increasing the delay means longer importing times
    delay: float = 0.3
    "########### GLOBAL IMPORTING DELAY ############"

    "###### LAST SUCCESSFULLY IMPORTED STRING ######"
    # If the importing failed/the string did not import successfully, enter THE LAST IMPORTED STRING into `last_string`
    # variable (instead of `None`)
    # This will re-import all the data from that string onward (including the last string/the one you entered as last)
    last_string = None
    "###### LAST SUCCESSFULLY IMPORTED STRING ######"

    copy_to_recroom(img_data=img_data, delay=delay, last_successful_string=last_string)


log = setup_logger()

if __name__ == "__main__":
    try:
        main(from_file="y" in input("Use the encoded data in `image_data.txt`? [yes/no]\n > "))
    except (Exception, KeyboardInterrupt):
        log.exception("ERROR", exc_info=True)