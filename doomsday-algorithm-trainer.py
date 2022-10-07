from random import randrange
from datetime import timedelta, datetime
import time
import sys
from colorama import Fore, Back, Style

B = ""  # Back.MAGENTA  # + Fore.CYAN
R = Back.RED
Y = Back.YELLOW + Fore.BLACK
r = Style.RESET_ALL

ANSWER_HISTORY_FILE = "history.txt"
#-------------------------
class TimeOutForInputTaking():
    #this class is something like None
    #all None are equal
    #All None will return True for "None is None"
    #its just like that

    THAT_OBJECT = None
    """
    fact:
        this class doent make any instance more than once
        it makes an instance at first time (which is 'THAT_OBJECT')
        then returns it all the other times when
        you request an instance from it
    """


    def __init__(self):
        if self.__class__.THAT_OBJECT  == None:
            self.__class__.THAT_OBJECT = self
        else:
            return self.__class__.THAT_OBJECT


    def __eq__(self, b):
        return self.__class__ == b.__class__
#--------------------------------------------------
def input_with_time_out(delay):
    #it doenst do anything beyond what its name say
    #it wont print guidning text
    #nor will do anything for timing out
    #all these actions mus tbe handled
    #by considering what this function will output
    #it will output an isntance of TimeOutForInputTaking for timing out cases
    output = ""
    time_started = time.time()

    while True:
        if msvcrt.kbhit():
            x=input()
            return input

        if time_started <= time.time()-delay:
            break

    return TimeOutForInputTaking()
# ------------------------
# mode related functions
def display_menu(settings):
    # TODO: allow printing stats
    print("What would you like to do?")
    print("1. Practice the doomsday method")
    print("2. Configure settings")
    mode = input("> ")
    if mode == "1":
        settings.mode = "date"
    elif mode == "2":
        settings.mode = "config"
    elif mode == "":
        settings.quit = True


# -------------------------
def run_date_mode(settings):
    # generate random date
    start_date = datetime(1999, 1, 1)
    end_date = datetime(2003, 12, 31)
    random_date = generate_random_date(start_date, end_date)

    # ask user for date
    date_string = get_date_string(random_date, settings.format)
    start_time = time.time()
    print(
        f"What day of the week is {date_string}? Number 0-6 (sunday - monday)",
        end="\r",
    )
    time.sleep(3)
    sys.stdout.write("\033[K")
    settings.input = input("> ")
    end_time = time.time()

    # switch to config mode if necessary
    if settings.input == "c":
        settings.mode = "config"
        return
    elif settings.input == "q" or settings.input == 0 or settings.input == "":
        settings.quit = True
        return

    # validate the date
    day_of_week = (random_date.weekday() + 1) % 7
    color_print(day_of_week)

    # record the answer and print explanation if necessary
    time_elapsed = settings.timed and (end_time - start_time)
    if str(day_of_week) != settings.input:
        explain_logic(random_date)
        record_answer(random_date, False, settings, time_elapsed)
    else:
        color_print("That is correct!")
        record_answer(random_date, True, settings, time_elapsed)

    input("Press enter to continue")
    print("\n")


# ---------------------------


def run_config_mode(settings):
    # TODO: allow setting hard mode (see question for limited time), timing, date format
    color_print("this is not yet set up")
    settings.mode = "menu"


# -----------------------------------
class Mode:
    def __init__(self, mode_title, mode_function):
        self.mode_title = mode_title
        self.mode_function = mode_function

    def can_be_called(self, current_setting_mode):
        return current_setting_mode == self.mode_title

    def call_mode_function(self, settings):
        self.mode_function(settings)


# modes
menu_mode = Mode(mode_title="menu", mode_function=display_menu)
date_mode = Mode(mode_title="date", mode_function=run_date_mode)
config_mode = Mode(mode_title="config", mode_function=run_config_mode)
modes = [menu_mode, date_mode, config_mode]
# -----------------------------------
class Settings:
    def __init__(
        self,
        mode="menu",
        input="",
        format="text",
        quit=False,
        timed=False,
        hard_mode=True,
    ):
        self.mode = mode
        self.input = input
        self.format = format
        self.quit = quit
        self.timed = timed
        self.hard_mode = hard_mode


# -----------------------------------
def run_any_mode_if_called(settings):
    for i1 in modes:
        if i1.can_be_called(settings.mode):
            i1.call_mode_function(settings)
            break


# -----------------------------------


def main():
    settings = Settings()
    while not settings.quit:
        run_any_mode_if_called(settings)


# -----------------------------------


def get_date_string(date, format="text"):
    if format == "text":
        return date.strftime("%B %d %Y")
    elif format == "number":
        return date.strftime("%m/%d/%Y")


def record_answer(date, correct, settings, time_elapsed=None):
    with open(ANSWER_HISTORY_FILE, "a") as f:
        date_string = date.strftime("%m/%d/%Y")
        correct_string = "correct" if correct else "incorrect"
        elapsed = round(time_elapsed, 1) if time_elapsed else "not-timed"

        f.write(
            f"{date_string} {correct_string} {elapsed} {settings.hard_mode} {settings.format}\n"
        )


def explain_logic(date):
    year = date.year
    month = date.month
    day = date.day

    # century doomsday
    color_print(Y + "CENTURY:")
    century = year // 100
    century_doomsdays = {0: 2, 1: 0, 2: 5, 3: 3}
    century_doomsday = century_doomsdays[century % 4]
    color_print(f"{century}00's doomsday is {R}{century_doomsday}", True)

    # decade doomsday
    color_print(Y + "DECADE:")
    decade = year % 100
    mults_of_12 = decade // 12
    remainder_of_12 = decade % 12
    leap_year_addition = remainder_of_12 // 4
    addition_beyond_mult_of_12 = remainder_of_12 + leap_year_addition
    raw_decade_offset = addition_beyond_mult_of_12 + mults_of_12
    decade_offset = raw_decade_offset % 7
    color_print(f"The decade can be broken into {mults_of_12 * 12} + {remainder_of_12}")
    color_print(
        f"The {mults_of_12 * 12} corresponds to a day index of {B}{mults_of_12}"
    )
    color_print(
        f"The decade index corresponds to the multiple of 12 ({mults_of_12}) "
        + f"plus a day index of {remainder_of_12} + "
        + f"{leap_year_addition} for the leap years, "
        + f"for a result of {raw_decade_offset} mod 7 = {R}{decade_offset}",
        True,
    )

    # year
    color_print(Y + "YEAR:")
    year_index = century_doomsday + decade_offset
    color_print(
        f"The century index of {century_doomsday} plus the decade "
        + f"index of {decade_offset} "
        + f"results in a year index of {year_index} and a doomsday of {R}{year_index % 7}",
        True,
    )

    # month explanation
    color_print(Y + "MONTH:")
    # add extra day to jan/feb if leap year (year divisible by 4 but not 100)
    leap_year_addition = (
        1 if decade % 4 == 0 and ((decade != 0) or (century % 4 == 0)) else 0
    )
    month_doomsdays = {
        1: 3 + leap_year_addition,
        2: 28 + leap_year_addition,
        3: 14,
        4: 4,
        5: 9,
        6: 6,
        7: 11,
        8: 8,
        9: 5,
        10: 10,
        11: 7,
        12: 12,
    }
    month_doomsday = month_doomsdays[month]
    color_print(f"The month is {month}, so the doomsday falls on {month_doomsday}\n")

    # day explanation
    color_print(Y + "DAY:")
    day_offset = day - month_doomsday
    effective_offset = day_offset % 7
    color_print(
        f"The day offset is {B}{day}{r} - {B}{month_doomsday}{r} = {B}{day_offset}{r} -> {R}{effective_offset}",
        True,
    )

    # final result
    color_print(Y + "RESULT:")
    result = (year_index + effective_offset) % 7
    color_print("Adding these together:")
    color_print(
        f"The year index of {year_index} plus the day offset of {effective_offset}"
    )
    color_print(f"= {R}{result}", True)
    weekday = (date.weekday() + 1) % 7
    if result != weekday:
        color_print(R + "THERE IS AN ERROR" + repr(result) + repr(weekday), True)


def color_print(text, newline=False):
    """Reset print style after printing"""
    print(str(text) + Style.RESET_ALL)
    if newline:
        print()


def generate_random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta) if int_delta else 0
    return start + timedelta(seconds=random_second)


if __name__ == "__main__":
    main()
