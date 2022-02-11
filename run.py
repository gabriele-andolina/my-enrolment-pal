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

print("Welcome to My Enrolment Pal, your school data management system.\n")
menu = """ What would you like to do today?
    1. Enter 1 to check an individual student's complete info.
    2. Enter 2 to add a new student to your database.
    3. Enter 3 to calculate the number of students for each study path.
    """
print(menu)


def input_handler():
    """
    Handles user input
    """
    while True:
        try:
            user_input = int(input("Please enter your choice here: "))
            if user_input > 0 and user_input < 4:
                pass
            else:
                print("You can only enter values from 1 to 3. Try again.")
        except ValueError:
            print("Oops... that doesn't look like a number. Try again.")

        if user_input == 1:
            get_student_data()


def get_student_data():
    """
    Matches user input with name values in the spreadsheet.
    Returns full data for chosen student.
    """
    print("Very well! You can check your students data below.")
    print("The student name must be formatted in this way: 'John Smith'.")
    print("Please enter only first and last name separated by a blank space.")
    stud_name = input("Please enter the student's name here: ")
    try:
        for char in stud_name:
            if char.isalpha() or char.isspace():
                retrieve_data()
    except ValueError:
        print("Sorry, invalid data. Try again.")


def retrieve_data():
    print("Valid data. Now we can move on.")


def main():
    """
    Run all program functions
    """
    input_handler()
    get_student_data()


main()
