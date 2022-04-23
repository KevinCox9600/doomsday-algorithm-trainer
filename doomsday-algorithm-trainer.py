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


class Settings:
    mode = "menu"
    input = ""
    format = "text"  # question date format
    quit = False
    timed = False
    hard_mode = True


def main():
    settings = Settings()
    while not settings.quit:
        if settings.mode == "menu":
            display_menu(settings)
        if settings.mode == "date":
            run_date_mode(settings)
        elif settings.mode == "config":
            run_config_mode(settings)


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


def run_config_mode(settings):
    # TODO: allow setting hard mode (see question for limited time), timing, date format
    color_print("this is not yet set up")
    settings.mode = "date"


def get_date_string(date, format="text"):
    if format == "text":
        return date.strftime("%B %d %Y")
    elif format == "number":
        return date.strftime("%m/%d/%Y")


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
