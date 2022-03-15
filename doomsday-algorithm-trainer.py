from random import randrange
from datetime import timedelta, datetime
import time
from colorama import Fore, Back, Style

B = ""  # Back.MAGENTA  # + Fore.CYAN
R = Back.RED
Y = Back.YELLOW + Fore.BLACK
r = Style.RESET_ALL


def main():
    mode = "date"
    i = "init"
    while i != "q" and i != 0 and i != "":
        if mode == "date":
            mode, i = date_mode(mode, i)
            time.sleep(1)
        elif mode == "config":
            color_print("this is not yet set up")
            mode = "date"


def date_mode(mode, i):
    # generate random date
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2003, 12, 31)
    random_date = generate_random_date(start_date, end_date)

    # ask user for date
    date_string = random_date.strftime("%m/%d/%Y")
    i = input(f"What day of the week is {date_string}? Number 0-6 (sunday - monday)\n")

    # switch to config mode if necessary
    if i == "c":
        mode = "config"
        return mode, i

    # validate the date
    day_of_week = (random_date.weekday() + 1) % 7
    color_print(day_of_week)

    if str(day_of_week) != i:
        explain_logic(random_date)
    else:
        color_print("That is correct!")

    return mode, i


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
    color_print(f"The decade can be broken into {mults_of_12 * 12} + {remainder_of_12}")
    color_print(
        f"The {mults_of_12 * 12} corresponds to a day index of {B}{mults_of_12}"
    )
    color_print(
        f"The {remainder_of_12} corresponds to a day index of {remainder_of_12} + "
        + f"{leap_year_addition} for the leap years, "
        + f"for a result of {R}{addition_beyond_mult_of_12}",
        True,
    )

    # year
    color_print(Y + "YEAR:")
    year_index = century_doomsday + addition_beyond_mult_of_12
    color_print(
        f"The century index of {century_doomsday} plus the decade "
        + f"index of {addition_beyond_mult_of_12} "
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
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


if __name__ == "__main__":
    main()