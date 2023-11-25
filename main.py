from control.pim_control import Controller
from control.Thread2 import Daemon
from view.pim_view import Printer


# the main function is the start of the system, it handles with the users choice and call corresponding Controller


def main():
    # create a Daemon thread until the end of the system, it repeatedly check the DDL
    # of the events and send email to users
    daemon = Daemon()
    daemon.create_daemon()
    controller = Controller()
    while True:
        printing = Printer()
        printing.main_page()
        choice0 = input("Enter your choice (1-6, 9): ")
        if choice0 == "1":
            controller.contact_control()
        elif choice0 == "2":
            controller.event_control()
        elif choice0 == "3":
            controller.note_control()
        elif choice0 == "4":
            controller.task_control()
        elif choice0 == "5":
            controller.load_control()
        elif choice0 == '6':
            controller.search_control()
        elif choice0 == "9":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
