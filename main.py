from control.pim_control import Controller
from view.pim_view import Printer

def main():
    controller = Controller()
    while True:
        printing=Printer()
        printing.main_page()
        choice0 = input("Enter your choice (1-4, 9): ")
        if choice0 == "1":
            controller.contact_control()
        elif choice0 == "2":
            controller.event_control()
        elif choice0 == "3":
            controller.note_control()
        elif choice0 == "4":
            controller.task_control()
        elif choice0 == "9":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
