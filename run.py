import sys
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('student_data')

student_info = SHEET.worksheet('student_info')

enrolled_stud = student_info.get_all_values()


def print_welcome_msg():
    """
    Prints a welcome message to the terminal.
    Starts the program and shows app menu.
    """
    print("\n")
    print("Welcome to My Enrolment Pal, your school data management system.\n")
    menu = """ What would you like to do today?
    1. Enter 1 to CHECK an individual student's complete info.
    2. Enter 2 to ADD a new student to your database.
    3. Enter 3 to CALCULATE the number of students for each study path.
    """
    print(menu)


def input_handler():
    """
    Handles user input
    """
    while True:
        try:
            user_input = int(input("Please enter your choice here:\n"))
            if user_input > 0 and user_input < 4:
                pass
            else:
                print("You can only enter values from 1 to 3. Try again.\n")
        except ValueError:
            print("You can only enter values from 1 to 3. Try again.\n")

        if user_input == 1:
            input_name()
        elif user_input == 2:
            add_student()
        elif user_input == 3:
            curriculum_calculator()


def next_step():
    """
    Used to move on to the next step as desired by the user.
    Depending on the user's input, it restarts the application or prints a closing message."
    """
    next_menu = """ What would you like to do next?
    1. Enter 1 to CHECK an individual student's complete info.
    2. Enter 2 to ADD a new student to your database.
    3. Enter 3 to CALCULATE the number of students for each study path.
    4. Enter 4 to CLOSE the program.
    """
    print(next_menu)

    while True:
        try:
            user_input = int(input("Please enter your choice here:\n"))
            if user_input > 0 and user_input < 5:
                pass
            else:
                print("You can only enter values from 1 to 4. Try again.\n")
        except ValueError:
            print("You can only enter values from 1 to 4. Try again.\n")

        if user_input == 1:
            input_name()
        elif user_input == 2:
            add_student()
        elif user_input == 3:
            curriculum_calculator()
        elif user_input == 4:
            print("That's it for today. Thank you for using My Enrolment Pal!")
            sys.exit()


def input_name():
    """
    Receives user input in the form of a student's name.
    Offers feedback as to the validity of the input.
    """
    print("You can CHECK your students data here.")
    print("Student names must be formatted as follows: 'John Smith'.")
    print("Enter first and last name separated by a blank space.\n")

    while True:
        stud_name = input("Please enter the student's name here:\n")
        if name_validator(stud_name):
            print(f"Correct input! Checking {stud_name}'s status now...\n")
            check_student(stud_name)
            next_step()
        else:
            print("Incorrect input. Student names must be formatted as follows: 'John Smith'.\n")


def name_validator(name):
    """
    Checks the validity of the user input.
    Returns a message to provide the user with relevant feedback.
    """
    result = True
    for char in name:
        if not char.isalpha() and not char.isspace():
            result = False
    return result


def check_student(stud_name):
    """
    Runs a loop through the students' name in the spreadsheet.
    Informs the user about the enrolment status of the checked student.
    """
    all_names = student_info.col_values(1)
    checked_stud = [name for name in all_names if name == stud_name]
    if checked_stud:
        print(f"Yes, {stud_name} is one of your students!")
    elif not checked_stud:
        print(f"Sorry, {stud_name} is currently not enroled.\n")
        next_step()

    stud_name_cell = student_info.find(stud_name)
    complete_stud_info = student_info.row_values(stud_name_cell.row)
    print(f"And here is {stud_name}'s complete info: {complete_stud_info}")
    print("The above values are: Full Name, Age, Country, Preferred Language, Proficiency Level, Main Goal\n")


def add_student():
    """
    Allows user to enter new student data.
    """
    print("You can ADD your new student's data here.")
    print("Please enter the data separated by commas as follows:")
    print("Name,Age,Country,Preferred Language,Proficiency Level,Main Goal.\n")
    print("The 'Preferred Language' can be English or French.")
    print("Valid 'Proficiency Level' values are: A1, A2, B1, B2, C1, C2.")
    print("The 'Main Goal' can be chosen among 'Business', 'Citizenship' and 'Art & Literature'.\n")
    while True:
        new_data = input("Enter the student's info here:\n").split(",")
        if new_info_validator(new_data):
            print("Valid data. Adding new student data to database now...\n")
            student_info.append_row(new_data)
            print(f"{new_data[0]} is now registered in your database. Well done!\n")
            next_step()
        else:
            print("Invalid input. Please make sure to enter the required six values. Try again.\n")


def new_info_validator(info):
    """
    Checks the validity of user input for new student info.
    Returns a message to provide the user with relevant feedback.
    """
    result = True
    if len(info) < 6 or len(info) > 6:
        result = False
    return result


def curriculum_calculator():
    """
    Calculates the number of students for each available study path.
    Returns relevant information to the user.
    """
    print("You can CALCULATE the number of students for each curriculum here.")
    print("Please enter one of the following: Business, Citizenship, Art & Literature")
    queried_curr = input("Please enter the chosen curriculum here:\n").capitalize()
    all_curriculum = student_info.col_values(6)
    business_curr = 0
    citizenship_curr = 0
    art_lit_curr = 0

    for curriculum in all_curriculum:
        if curriculum == "Business":
            business_curr += 1
        elif curriculum == "Citizenship":
            citizenship_curr += 1
        elif curriculum == "Art & Literature":
            art_lit_curr += 1
    while True:
        if queried_curr == "Business":
            print(f"The number of students for the {queried_curr} curriculum is {business_curr}.")
            next_step()
        elif queried_curr == "Citizenship":
            print(f"The number of students for the {queried_curr} curriculum is {citizenship_curr}.")
            next_step()
        elif queried_curr == "Art & Literature":
            print(f"The number of students for the {queried_curr} curriculum is {art_lit_curr}.")
            next_step()


def main():
    """
    Run all program functions
    """
    print_welcome_msg()
    input_handler()
    input_name()
    add_student()
    new_info_validator()
    curriculum_calculator()
    next_step()


main()
