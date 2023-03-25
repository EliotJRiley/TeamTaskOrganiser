#=====importing libraries===========
from datetime import datetime

#====Login Section====
username_password = {}
with open("user.txt", "r") as file:
    details = file.readlines()
    
for line in details:
    separate = line.split(", ")
    username_password[separate[0].strip()] = separate[1].strip()

#Tracks if the logged in account has admin privileges
admin_privileges = False

login_success = False

while not login_success:
    username_attempt = input("Please enter the username of the account you would like to log into ")
    
    if username_attempt in username_password:
        password_attempt = input("Please enter the password associated with the username you entered ")

        if username_password[username_attempt] == password_attempt:
            login_success = True
            print(f"You've successfully logged into account: {username_attempt}")
        
        else:
            print("Incorrect password, please try again")
    else:
        print("Incorrect username, please try again")

#username_attempt will continue to be used as the variable that stores the name of the logged in account
if username_attempt == "admin":
    admin_privileges = True

#Defining functions area, we will start with reg_user
def reg_user():
    registered_user = False
    while not registered_user:
        new_username = input("Please enter the username for the new account you would like to create ")
        
        
        with open("user.txt", "r") as file:
            details = file.readlines()
    
        for line in details:
            separate = line.split(", ")
            username_password[separate[0].strip()] = separate[1].strip()
        if new_username in username_password.keys():
            print(f"That username is already in use, as a reminder here are the existing usernames in the system \n{list(username_password.keys())} \n please try again")
            continue
        new_password = input("Please enter the password you would like to use to access this account ")
        password_confirmation = input("Please re-enter the password you just entered to ensure you entered what you intended to ")
        
        if new_password == password_confirmation:
            with open("user.txt", "a") as f:
                f.write('\n' + new_username + ", " +  new_password)
            registered_user = True
        
        else:
            print("your passwords did not match, please try again")
    return f"You have registered a new user, with username {new_username}"

#Defining add_task ---------------------------------------------
def add_task():
    username = input("Please enter the username of the person this task will be assigned to ")
    title = input("Please enter the title of this task ")
    description = input("Please enter a relevant description for this task ")
    due_date = input("Please enter the due date for this task ")
    current_date = datetime.now().date().strftime("%d %b %Y")
    task_complete = "No"
    with open("tasks.txt", "a") as f:
        f.write("\n" + username + ", " + title + ", " + description + ", " + current_date + ", " + due_date + ", " + task_complete)


#Defining view_all
def view_all():
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
        
    for line in tasks:
        line = line.split(", ")
        task_dict = {
            "assigned_to": line[0],
            "task": line[1],
            "task_description": line[2],
            "date_assigned": line[3],
            "due_date": line[4],
            "task_complete": line[5].strip("\n")
        }

        print("_" * 100)
        print(f"Task:                       {task_dict['task']}")
        print(f"Assigned to:                {task_dict['assigned_to']}")
        print(f"Date assigned:              {task_dict['date_assigned']}")
        print(f"Due date:                   {task_dict['due_date']}")
        print(f"Task Complete?              {task_dict['task_complete']}")
        print(f"Task Description:           {task_dict['task_description']}")
        print("_" * 100)


#Defining view_mine ---------------------------------------
def view_mine():
    tasks = []
    with open("tasks.txt", "r") as f:
        for line in f:
            line = line.strip().split(", ")
            if line[0] == username_attempt:
                task = {
                    "assigned_to": line[0],
                    "task": line[1],
                    "task_description": line[2],
                    "date_assigned": line[3],
                    "due_date": line[4],
                    "task_complete": line[5].strip()
                }
                tasks.append(task)

    if not tasks:
        print("You have no tasks assigned to you.")
        return

    for i, task in enumerate(tasks, start=1):
        print("_" * 100)
        print(f"Task number:                {i}")
        print(f"Task:                       {task['task']}")
        print(f"Assigned to:                {task['assigned_to']}")
        print(f"Date assigned:              {task['date_assigned']}")
        print(f"Due date:                   {task['due_date']}")
        print(f"Task Complete?              {task['task_complete']}")
        print(f"Task Description:           {task['task_description']}")
        print("_" * 100)

    while True:
        option = input("Please select a task number to edit or '-1' to go back to the menu ")
        if option == "-1":
            return
        task_index = int(option) - 1
        if task_index < 0 or task_index >= len(tasks):
            print("Invalid task number.")
            continue
        task = tasks[task_index]
        print(f"You have selected Task {task['task']}")
        want_to_update = input("Would you like to update the task to complete or change who it's assigned to, enter '1' for first choice or '2' for second ")
        if want_to_update == "1":
            if task['task_complete'] == 'No':
                task['task_complete'] = 'Yes'
                lines_of_tasks = []
                with open("tasks.txt", "r") as f:
                    for line in f:
                        line = line.strip().split(", ")
                        if line[0] == task['assigned_to'] and line[1] == task['task']:
                            line[5] = 'Yes'
                        lines_of_tasks.append(", ".join(line) + "\n")
                with open("tasks.txt", "w") as f:
                    f.writelines(lines_of_tasks)
                print("You have successfully set the task to complete")
            else:
                print("The task is already completed.")
        elif want_to_update == "2" and task['task_complete'] == "No":
            new_assign = input(f"Who would you like to assign task to, instead of {task['assigned_to']}? ")
            lines_of_tasks = []
            with open("tasks.txt", "r") as f:
                for line in f:
                    line = line.strip().split(", ")
                    if line[1] == task['task']:
                        line[0] = new_assign
                    lines_of_tasks.append(", ".join(line) + "\n")
            with open("tasks.txt", "w") as f:
                f.writelines(lines_of_tasks)
            print("You have successfully updated who the task is assigned to")
        else:
            print("You cannot change who a completed task is assigned to, sorry")

def get_report():
    #Generating task_overview.txt
    with open("tasks.txt", "r") as f:
        f = f.readlines()
        today = datetime.today().strftime("%d %b %Y")
        total_tasks = len(f)
        complete_counter = 0
        overdue_tasks = 0
        for line in f:
            line = line.split(",")
            if line[5].strip() == "Yes":
                complete_counter += 1
            if line[4] > today:
                overdue_tasks += 1
        incomplete_tasks = total_tasks - complete_counter
        incomplete_task_percent = ((total_tasks - complete_counter)/total_tasks) * 100
        overdue_task_percent = ((overdue_tasks)/total_tasks) * 100
        with open("task_overview.txt", "w") as f:
            f.write(f"Total tasks:                  {total_tasks}\n")
            f.write(f"Completed tasks:              {complete_counter}\n")
            f.write(f"Incomplete tasks:             {incomplete_tasks}\n")
            f.write(f"Percentage of tasks incomplete: {round(incomplete_task_percent, 2)}%\n")
            f.write(f"Overdue tasks:                {overdue_tasks}\n")
            f.write(f"Percentage of overdue tasks:  {round(overdue_task_percent, 2)}%\n")


    #Generating user_overview.txt
    with open("tasks.txt", "r") as f:
        f = f.readlines()
        today = datetime.today().strftime("%d %b %Y")
        total_tasks = len(f)
        users = {}
        for line in f:
            line = line.split(", ")
            username = line[0]
            completed = line[5].strip() == "Yes"
            overdue = line[4] > today
            if username in users:
                users[username]["total"] += 1
                if completed:
                    users[username]["completed"] += 1
                else:
                    if line[4] > today:
                        users[username]["overdue"] += 1
            else:
                users[username] = {"total": 1, "completed": int(completed), "overdue": int(overdue)}
        
        with open("user_overview.txt", "w") as f:
            f.write(f"Total tasks: {total_tasks}\n")
            for username, stats in users.items():
                f.write(f"\nUser: {username}\n")
                f.write(f"Total tasks assigned to user: {stats['total']}\n")
                f.write(f"Percentage of total tasks assigned to user: {(stats['total'] / total_tasks) * 100:.2f}%\n")
                f.write(f"Percentage assigned to user that are completed: {(stats['completed'] / stats['total']) * 100:.2f}%\n")
                f.write(f"Percentage assigned to user to still be completed: {((stats['total'] - stats['completed']) / stats['total']) * 100:.2f}%\n")
                f.write(f"Percentage of tasks that are incomplete and overdue: {(stats['overdue'] / stats['total']) * 100:.2f}%\n")
            
def get_statistics():
    try:
        with open("user_overview.txt", "r") as f:
            users = f.readlines()
            total_users = len(users)
        with open("task_overview.txt", "r") as f:
            tasks = f.readlines()
            total_tasks = len(tasks)
        
    except FileNotFoundError:
        get_report()
        with open("user_overview.txt", "r") as f:
            users = f.readlines()
            total_users = len(users)
        with open("task_overview.txt", "r") as f:
            tasks = f.readlines()
            total_tasks = len(tasks)
    print("_" * 100)
    print(f"Number of users in system:      {total_users}")
    print(f"Number of tasks in system:      {total_tasks}")
    print("_" * 100)

while True:
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
s - Display statistics
va - View all tasks
vm - view my task
gr - Generate reports
e - Exit
: ''').lower()

    #For registering a user, the logged in account must be an admin to access this block
    if menu == 'r' and admin_privileges:
        reg_user()      


    elif menu == "r" and not admin_privileges:
        print("You are not an admin, you cannot register a new user")

    
    #For adding a new task to the system, at the current stage of the program it is possible to assign a task to a user who does not exist, this could be updated so it check the username input for being a valid username that's registered
    elif menu == 'a':
        add_task()


    
    #For accessing the statistics in the system, we track the number of users and tasks by counting the number of lines in their respective text files
    elif menu == "s" and admin_privileges:
        get_statistics()

    elif menu == "s" and not admin_privileges:
        print("\n You are not an admin, you cannot access statistics for the system \n")

    
    
    #For viewing all the tasks in the system 
    elif menu == 'va':
        view_all()
        
        

    #For viewing the users' own tasks, we use any_tasks as a test to see if the user has any tasks at all assigned to them
    elif menu == 'vm':
        view_mine()


    #For exiting the system
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    elif menu == "gr":
        get_report()


    #We use .lower() so the menu input isn't case sensitive, but the user can still enter an invalid letter so this message is for that case
    else:
        print("You have made a wrong choice, Please Try again")