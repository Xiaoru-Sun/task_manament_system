
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re
import numpy as np

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#DEFINE ALL FUNCTIONS

def menu():
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        # to register new user
        register_user()
    elif menu == 'a':
        # to add new task
        add_new_task()
    elif menu == 'va':
         # to view all the tasks
        view_all_task()      
    elif menu == 'vm':
        # to view all the tasks assigned to the current user
        view_my_task()
    elif menu == "gr":
        generate_report()
        # to generate report   
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")

def check_username(name):
    return bool(name not in username_password and
                len(name) >= 4 and
                re.search(r'^[a-z][a-z0-9]+$', name))

def check_password(password):
    """password should
    be 6-10 characters long
    Contain at least 1 number
    Contain at least 1 capital letter
    Contain at least 1 lowercase letter
    Contain at least 1 special symbol
    """
    return bool(re.search(r'\d', password) and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[@$!%*#?&]', password) and
            5<len(password)<11)

def mark_complete(task):
    task["completed"] == "Yes"
    print("This task has been marked as completed.")

def edit_task(task):
    task_due_date = task["due_date"]
    task_username = task["username"]
    print(f"This task is assigned to: {task_username}.")
    print(f"The task is due on: {task_due_date}.")
    curr_date = date.today()
    six_months = date.today() + relativedelta(months=+6)

    list_to_edit = ["due_date","username","both"]
    while True:
        try:
            element_to_edit=int(input('''Please enter '0' if you need to edit the task due date, enter '1'
if you need to edit the username, or enter'2' if you need to edit both.
'''))
            if element_to_edit in range(3):
                break
            else:
                print("You need to enter a number 0, or 1, or 2 to choose what you would like to edit.")
                continue
        except:
            print("The input has to be a whole number from 0 to 2!.")

    if element_to_edit == 0:
        print("You have selected to edit the task due date.")
        print("Please enter the due date you want to change into.")

        while True:
            try:
                new_task_due_date = input("Due date of task (YYYY-MM-DD): ")
                new_due_date_time = datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                if new_due_date_time.date() < curr_date or new_due_date_time.date() > six_months :
                    print("Invalid due date.")
                    print("Due date should be within 6 months from today! Please put another date.")
                    continue
                #if the date that meets the required format,the program goes back to the while loop
                else:break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        task["due_date"] = new_due_date_time
        # To verify the type of task's due datef print(type(task["due_date"]))
        print("The task due date has been updated.")

    elif element_to_edit == 1:
        print("You have selected to edit the username of the task.")
        print("Please see all the usernames", user_list)
        
        new_task_username = input("Please enter the username you want to assign the task to: ").lower()
        while new_task_username not in username_password:
            print("The username is invalid.")
            print("The username does not exist in the data.")
            new_task_username = input("Please enter the username you want to assign the task to: ").lower()

        task["username"] = new_task_username
        print("The task username has been updated.")

    elif element_to_edit == 2:
        print("You have selected to edit both the username and the due date.")
        print("Please see all the usernames", user_list)
       
        new_task_username = input("Please enter the username you want to assign the task to: ").lower()
        while new_task_username not in username_password:
            print("Invalid username! The username does NOT exist in the data.")
            new_task_username = input("Please enter the username you want to assign the task to: ").lower()
        task["username"] = new_task_username
    
        print("Please enter the due date you want to change into.")
        while True:
            try:
                new_task_due_date = input("Due date of task (YYYY-MM-DD): ")
                new_due_date_time = datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                if new_due_date_time.date() < curr_date or new_due_date_time.date() > six_months :
                    print("Invalid due date.")
                    print("Due date should be within 6 months from today! Please put another date.")
                    continue
                else:break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        task["due_date"] = new_due_date_time
        
        print("The task username and the due date have been updated.")
        print(f"The task username has been changed from {task_username} to {new_task_username}.")
        print(f"The task description has been changed from {task_due_date} to {new_task_due_date}.")


def register_user():
    # - Request input of a new username
    print("Please enter a username.")
    print("The username should ONLY contain small letters and numbers, must have at least 4 characters and start with numbers.")
    new_username = input("New Username: ")
    # - Test whether username is valid 
    # reset the condtions!
    while check_username(new_username) is False:
        print("Invalid input")
        new_username = input("New Username: ")

    # - Request input of a new password
    while True:
        print("""password is 6-10 characters and should contain at least one lower&upper letter,
        one number and one special character from [@$!%*#?&]""")
        new_password = input("New Password: ")
        if check_password(new_password):
            break
        else:
            continue

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")
    # - Check if the new password and confirmed password are the same.
    while new_password != confirm_password:
        print("Passwords do NOT match. Please try again.")
        confirm_password = input("Confirm Password: ")

    # - If they are the same, add them to the user.txt file,
    username_password[new_username] = new_password
    print("New user successfully added")

    # try except expression
    with open("user.txt","a") as out_file:
        out_file.write("\n"+new_username+";"+new_password)

def add_new_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.'''
    print("You have selected to add new task. Each time only one task can be added.")
    # - Request input of an username
    task_username = input("Name of person assigned to task: ")
    # - Test if the username exists and requests input again if the username does not exist
    while task_username not in username_password:
        print("User does not exist. Please enter a valid username.")
        task_username = input("Name of person assigned to task: ")
    # - Request input of a title
    print("The title should contain at least 10 characters.")
    task_title = input("Title of Task: ")
    while len(task_title) < 10:
        task_title = input("Title of Task: ")
    # - Request input of task description
    print("The task description should contain at least 15 characters.")
    task_description = input("Description of Task: ")
    while len(task_description) < 15:
        task_description = input("Description of Task: ")

    curr_date = date.today()
    six_months = date.today() + relativedelta(months=+6)
    # - Validate task due date's format and test whether it is later than today's date
    # The format has to be correct for comparing with today's date
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            if due_date_time.date() < curr_date or due_date_time.date() > six_months :
                print("Invalid due date.")
                print("Due date should be within 6 months from today! Please put another date.")
                """ if the date that meets the required format,the program goes back to the while loop"""
                continue
            else: break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    # - Save the newly added task in a dictionary
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    #- Add this new task to the task list
    task_list.append(new_task)
 
# - Open task.txt in "a" mode to add new task into the file without overwriting the other tasks
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"\n{task_username};{task_title};{task_description};{task_due_date};{curr_date};'No'")
    print("Task successfully added.")


    
def view_all_task():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
    print("You have selected to view all the tasks.")
    if len(task_list) == 0:
        print("There is no task.")
    else:
        print("Please see all the tasks as below;")
        for index,task in enumerate(task_list):
            print("\nTask",index+1)
            for key,value in task.items():
                if key == 'completed' and bool(value) == True:
                    print(key, ";", "Yes")
                elif key == 'completed' and bool(value) == False:
                    print(key, ":", "No")
                else:
                    print(key,":",value)

        check_task_or_not = input("\nDo you want to go into any particular task? Type 'Y' for 'Yes' or 'N' for 'No': ").upper()
        while check_task_or_not not in ("Y","N"):
            print("You need to choose 'Y' or 'N'")
            check_task_or_not = input("Do you want to go into any particular task? Type 'Y' for 'Yes' or 'N' for 'No': ").upper()
        
        if check_task_or_not == "N":
            print("Go back to main menu...")
            menu()
        else:
            while True:
                try:
                    ref_of_task = int(input(f"There are in total {len(task_list)} tasks.\n"
                                            f"Each task has been assigned a number and enter a number from 1 to {len(task_list)}: "))
                    if ref_of_task in range(1,len(task_list)+1):
                        print(f"You have seleted the task {ref_of_task}: ")
                        break
                    else:
                        continue
                except:
                    print(f"You should enter ONLY number here!")
            print("Please see this task as below;\n ")
            for key,value in task_list[ref_of_task-1].items():
                print(key,": ", value)

            status_of_completed = task_list[ref_of_task-1]["completed"]

            if status_of_completed == "Yes":
                print("This task has been completed. It can NOT be edited.")
            else:
                print("This task is NOT completed so you can modify the task.")
                mark_task_as_completed_or_not = input("\nDo you want to mark the task as completed? Type 'Y' for 'Yes' or 'N' for 'No': ").upper()
                while mark_task_as_completed_or_not not in ( "Y" ,"N"):
                    print("You need to choose 'Y' or 'N'")
                    mark_task_as_completed_or_not=input("Please enter 'Y' for 'Yes' or 'N' for 'No': ").upper()
                if mark_task_as_completed_or_not == "Y":
                    mark_complete(task_list[ref_of_task-1])
                else:

                    edit_task_or_not = input("\nDo you want to edit the task? Type 'Y' for 'Yes' or 'N' for 'No': ").upper()
                    while edit_task_or_not not in ("Y","N"):
                        print("You need to choose 'Y' or 'N'")
                        edit_task_or_not = input("Please enter 'Y' for 'Yes' or 'N' for 'No': ").upper()
                    if edit_task_or_not == "Y":
                        print("You can edit the task now.")
                        print("Please note only the username to whom the task is assigned to and the due date can be edited\n")
                        edit_task(task_list[ref_of_task-1])


def view_my_task():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    print("You have selected to view tasks assigned to youself.")

    num_of_my_task = 0
    for t in task_list:
        if t['username'] == curr_user:
            num_of_my_task += 1
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
    if num_of_my_task == 0:
        print("There is no task assigned to you.")
    else:
        print(f"Above is all the tasks assigned to you. There is {num_of_my_task} in total.")

def displayData(list_of_dicts):
    import pandas as pd
    from IPython import display
    df = pd.DataFrame(list_of_dicts)
    print(df)
    df.to_csv('user_overview.csv')
    print("The file 'user_overview.csv' has been generated.")
    return df

def generate_report():
    print("You have selected to generate report.")
    total_num_of_task = len(task_list)
    total_num_of_completed_task = 0
    total_num_of_overdue_task = 0
    with open("task_overview.txt","w") as task_overview_report:
        if len(task_list) == 0:
            print("There is no task so no report can be generated!")
        else:
            for task in task_list:
                if task["completed"]:
                    total_num_of_completed_task += 1
                elif task["completed"] == False and task["due_date"].date() < date.today():
                    total_num_of_overdue_task += 1
 
            total_num_of_uncompleted_task = total_num_of_task - total_num_of_completed_task
            
            l1 = f"The total number of tasks: {total_num_of_task}\n"
            l2 = f"The total number of completed tasks: {total_num_of_completed_task}\n"
            l3 = f"The total number of uncompleted and overdue tasks: {total_num_of_overdue_task}\n"
            l4 = f"The percentage of uncompleted tasks: {str(100*total_num_of_uncompleted_task / total_num_of_task)+'%'}\n"
            l5 = f"The percentage of overdue tasks: {str(100*total_num_of_overdue_task / total_num_of_task)+'%'}\n"
            # print(l1)
            # print(l2)
            # print(l3)
            # print(l4)
            # print(l5)
            overview_report_content = l1 + l2 + l3 + l4 + l5
            task_overview_report.write(overview_report_content)
            print("The report 'task-overview.txt' has been generated.")
    
    user_overview_data = []
    num_of_all_users = len(user_data)
    num_of_all_tasks = len(task_list)
    for item in user_data:
        user = item.split(";")[0]
        num_of_assigned_task = 0
        num_of_completed_task = 0
        num_of_overdue_task = 0
        data_by_user = {}
        for task in task_list:
            if user == task["username"]:
                num_of_assigned_task +=1
                if task["completed"]:
                    num_of_completed_task +=1
                elif task["completed"] is False and task["due_date"].date() < date.today():
                    num_of_overdue_task +=1
        num_of_uncompleted_task = num_of_assigned_task - num_of_completed_task
        data_by_user["user"] = user
        data_by_user["assigned_task_to_user"] = num_of_assigned_task
        data_by_user["completed"] = num_of_completed_task
        data_by_user["uncompleted"] = num_of_uncompleted_task
        data_by_user["overdue"] = num_of_overdue_task
        
        if num_of_assigned_task != 0:
            data_by_user["percentage_of_completion"] = str (num_of_completed_task *100 /num_of_assigned_task) + "%"
            data_by_user["percentage_of_umcompleted_task"] = str(num_of_uncompleted_task *100 / num_of_assigned_task) +"%"
            data_by_user["percentage_of_overdue"] = str(num_of_overdue_task *100 / num_of_assigned_task) + "%"

        else:
            data_by_user["percentage_of_completion"] = "No tasks assigned"
            data_by_user["percentage_of_umcompleted_task"] = "No tasks assigned"
            data_by_user["percentage_of_overdue"] ="No tasks assigned"

        user_overview_data.append(data_by_user)
    report_format = input("""Do you want to generate your user overview report in which format?
    Enter 'C' for 'csv' or 'T' for 'txt': """).upper()
    while report_format not in ["C","T"]:
        report_format = input("""Do you want to generate your user overview report in which format?
    Enter 'C' for 'csv' or 'T' for 'txt': """).upper()
    if report_format == "C":
        displayData(user_overview_data)
        print("The report 'user_overview.csv' has been generated.")
    else:
        with open("user_overview.txt","w") as user_overview_report:
            user_overview_report.write(f"The total number of all the users: {num_of_all_users}")
            user_overview_report.write(f"\nThe total number of all the tasks: {num_of_all_tasks}\n")
            for item in user_overview_data:
                user_overview_report.write(f"\nUsername: {item['user']}\n")
                user_overview_report.write(f"The number of tasks assigned: {item['assigned_task_to_user']}\n")
                user_overview_report.write(f"The number of completed tasks: {item['completed']}\n")
                user_overview_report.write(f"The number of uncompleted tasks: {item['uncompleted']}\n")
                user_overview_report.write(f"The number of overdue tasks: {item['overdue']}\n")
                user_overview_report.write(f"The percentage of completed tasks: {item['percentage_of_completion']}\n")
                user_overview_report.write(f"The percentage of uncompleted tasks: {item['percentage_of_umcompleted_task']}\n ")
                user_overview_report.write(f"The percentage of overdue tasks: {item['percentage_of_overdue']}\n")
        print("The report 'user_overview.txt' has been generated.")

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]
task_list = []
for t_str in task_data:
    curr_t = {}
# Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)
    


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
user_list = []
username_password = {}
for user in user_data:
    username, password = user.split(';')
    user_list.append(username)
    username_password[username] = password


#log in part. it is necessary to have username_password dictionary ready prior to log in part
logged_in = False
#while not logged_in:
print("LOGIN")
curr_user = input("Username: ")
while curr_user not in username_password:
    print("User does not exist")
    curr_user = input("Username: ")

curr_pass = input("Password: ")
if username_password[curr_user] != curr_pass:
    print("Wrong password")
    print("Your account will be locked up after 3 times of incorrect attemps.")
    ### add something for what happens when there are no times left
    for i in range(3):
        print(f"You have {3-i} times left")
        curr_pass = input("Password: ")
        if username_password[curr_user] == curr_pass:
            print("Password is correct")
            print("Login Successful!")
            logged_in = True
            break
        else:
            print("Wrong password.")         
else:
    print("Login Successful!")
    logged_in = True

if logged_in == False:
    print("Your account is blocked.")

while logged_in is True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    menu()