from random import randrange
from datetime import timedelta, datetime
import time


def main():
    i = "init"
    mode = "date"
    while i != "q" and i != 0 and i != "":
        if mode == "date":
            # generate random date
            start_date = datetime(2000, 1, 1)
            end_date = datetime(2003, 12, 31)
            random_date = generate_random_date(start_date, end_date)

            # ask user for date
            i = input(
                f"What day of the week is {random_date}? Number 0-6 (sunday - monday)\n"
            )

            # switch to config mode if necessary
            if i == "c":
                mode = "config"
                continue

            # validate the date
            day_of_week = (random_date.weekday() + 1) % 7
            print(day_of_week)

            if str(day_of_week) != i:
                explain_logic(random_date)
            else:
                print("That is correct!")

            time.sleep(1)
        elif mode == "config":
            print("this is not yet set up")
            break


def explain_logic(date):
    year = date.year
    month = date.month
    day = date.day

    # year explanation
    # century doomsday
    century = year // 100
    century_doomsdays = {0: 2, 1: 0, 2: 5, 3: 3}
    century_doomsday = century_doomsdays[century % 4]
    print(f"{century}00's doomsday is {century_doomsday}\n")
    # decade doomsday
    decade = year % 100
    mults_of_12 = decade // 12
    remainder_of_12 = decade % 12
    leap_year_addition = remainder_of_12 // 4
    addition_beyond_mult_of_12 = remainder_of_12 + leap_year_addition
    print(f"The decade can be broken into {mults_of_12 * 12} + {remainder_of_12}")
    print(f"The {mults_of_12 * 12} corresponds to a day index of {mults_of_12}")
    print(
        f"The {remainder_of_12} corresponds to a day index of {remainder_of_12} +"
        + f"{leap_year_addition} for the leap years,"
        + f"for a result of {addition_beyond_mult_of_12}\n"
    )

    year_index = century_doomsday + addition_beyond_mult_of_12
    print(
        f"The century index of {century_doomsday} plus the decade"
        + f" index of {addition_beyond_mult_of_12} "
        + f"results in a year index of {year_index} and a doomsday of {year_index % 7}"
    )

    # month explanation
    # day explanation
    print("explained!")


def generate_random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


if __name__ == "__main__":
    main()