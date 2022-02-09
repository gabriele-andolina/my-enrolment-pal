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

welcome_message = """Welcome to My Enrolment Pal, your digital aid for data management.\n
What would you like to do today?
1. Enter "i" to check a student's complete info.
2. Enter "a" to add a new student to your database.
3. Enter "c" to calculate the number of students for each study path.
"""
print(welcome_message)


def input_handler():
    """
    Handles user input
    """
    user_input = input("Please enter your choice here: ")
    print(user_input)


input_handler()
