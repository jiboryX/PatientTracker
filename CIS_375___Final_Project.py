#Hussain Aljibory 8/17/2023
import tkinter as tk
from tkinter import messagebox

# Define the Patient class to store patient information
class Patient:
    def __init__(self, name, information):
        self.name = name
        self.information = information

# Define the PatientTracker class to manage user accounts and patient records
class PatientTracker:
    def __init__(self):
        self.users = {}
        self.logged_in_user = None

    # Load user data from file during initialization
    def load_from_file(self):
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, patient_str = line.strip().split(':')
                    patients_data = patient_str.split('|')
                    patients = [Patient(p.split(',')[0], p.split(',')[1]) for p in patients_data]
                    self.users[username] = {'password': password, 'patients': patients}
        except FileNotFoundError:
            pass

    # Save user data to file
    def save_to_file(self):
        with open('users.txt', 'w') as file:
            for username, data in self.users.items():
                password = data['password']
                patients = data['patients']
                patients_data = '|'.join([f"{p.name},{p.information}" for p in patients])
                file.write(f"{username}:{password}:{patients_data}\n")

    # Register a new user
    def register(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return False
        self.users[username] = {'password': password, 'patients': []}
        print("Registration successful.")
        return True

    # Log in a user
    def login(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            self.logged_in_user = username
            print(f"Logged in as {self.logged_in_user}")
        else:
            print("Invalid credentials")

    # Add a patient record for the logged-in user
    def add_patient_record(self, patient_name, patient_information):
        if self.logged_in_user:
            patient = Patient(patient_name, patient_information)
            self.users[self.logged_in_user]['patients'].append(patient)
            print("Patient record added.")
        else:
            print("Please log in first.")

    # View patient records for the logged-in user
    def view_patient_records(self):
        if self.logged_in_user:
            patients = self.users[self.logged_in_user]['patients']
            if patients:
                print("Your Patient Records:")
                for idx, patient in enumerate(patients, start=1):
                    print(f"{idx}. Name: {patient.name}, Information: {patient.information}")
            else:
                print("You have no patient records.")
        else:
            print("Please log in first.")

# Define the main GUI application class
class PatientTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Tracker App")

        self.tracker = PatientTracker()
        self.tracker.load_from_file()

        # Create GUI elements
        self.label = tk.Label(root, text="Welcome to the Patient Tracker App")
        self.label.pack()

        self.button_register = tk.Button(root, text="Register", command=self.register)
        self.button_register.pack()

        self.button_login = tk.Button(root, text="Login", command=self.login)
        self.button_login.pack()

        self.button_exit = tk.Button(root, text="Exit", command=root.quit)
        self.button_exit.pack()

        self.records_window = None

    def register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")

        label_username = tk.Label(register_window, text="Username:")
        label_username.pack()
        entry_username = tk.Entry(register_window)
        entry_username.pack()

        label_password = tk.Label(register_window, text="Password:")
        label_password.pack()
        entry_password = tk.Entry(register_window, show="*")
        entry_password.pack()

        button_register = tk.Button(register_window, text="Register", command=lambda: self.handle_registration(entry_username.get(), entry_password.get(), register_window))
        button_register.pack()

    def handle_registration(self, username, password, window):
        if self.tracker.register(username, password):
            messagebox.showinfo("Registration", "Registration successful.")
            window.destroy()
        else:
            messagebox.showerror("Registration", "Username already exists.")

    def login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")

        label_username = tk.Label(login_window, text="Username:")
        label_username.pack()
        entry_username = tk.Entry(login_window)
        entry_username.pack()

        label_password = tk.Label(login_window, text="Password:")
        label_password.pack()
        entry_password = tk.Entry(login_window, show="*")
        entry_password.pack()

        button_login = tk.Button(login_window, text="Login", command=lambda: self.handle_login(entry_username.get(), entry_password.get(), login_window))
        button_login.pack()

    def handle_login(self, username, password, window):
        self.tracker.login(username, password)
        if self.tracker.logged_in_user:
            self.show_patient_records()
            window.destroy()
        else:
            messagebox.showerror("Login", "Invalid credentials.")

    def show_patient_records(self):
        if self.records_window:
            self.records_window.destroy()

        self.records_window = tk.Toplevel(self.root)
        self.records_window.title("Patient Records")

        self.tracker.view_patient_records()
        patients = self.tracker.users[self.tracker.logged_in_user]['patients']

        if patients:
            label_records = tk.Label(self.records_window, text="Your Patient Records:")
            label_records.pack()

            for idx, patient in enumerate(patients, start=1):
                label = tk.Label(self.records_window, text=f"{idx}. Name: {patient.name}, information: {patient.information}")
                label.pack()
        else:
            label_no_records = tk.Label(self.records_window, text="You have no patient records.")
            label_no_records.pack()

        button_add_record = tk.Button(self.records_window, text="Add Patient Record", command=self.add_patient_record)
        button_add_record.pack()
    def update_patient_records_display(self):
        if self.records_window:
            self.records_window.destroy()

        self.records_window = tk.Toplevel(self.root)
        self.records_window.title("Patient Records")

        self.tracker.view_patient_records()
        patients = self.tracker.users[self.tracker.logged_in_user]['patients']

        if patients:
            label_records = tk.Label(self.records_window, text="Your Patient Records:")
            label_records.pack()

            for idx, patient in enumerate(patients, start=1):
                label = tk.Label(self.records_window, text=f"{idx}. Name: {patient.name}, information: {patient.information}")
                label.pack()
        else:
            label_no_records = tk.Label(self.records_window, text="You have no patient records.")
            label_no_records.pack()

        button_add_record = tk.Button(self.records_window, text="Add Patient Record", command=self.add_patient_record)
        button_add_record.pack()
    def add_patient_record(self):
        if self.records_window:
            self.records_window.destroy()

        self.records_window = tk.Toplevel(self.root)
        self.records_window.title("Add Patient Record")

        label_patient_name = tk.Label(self.records_window, text="Patient Name:")
        label_patient_name.pack()
        entry_patient_name = tk.Entry(self.records_window)
        entry_patient_name.pack()

        label_patient_information = tk.Label(self.records_window, text="Patient information:")
        label_patient_information.pack()
        entry_patient_information = tk.Entry(self.records_window)
        entry_patient_information.pack()

        button_submit_record = tk.Button(self.records_window, text="Submit Record", command=lambda: self.handle_record_submission(entry_patient_name.get(), entry_patient_information.get(), self.records_window))
        button_submit_record.pack()

    def handle_record_submission(self, name, information, window):
        if name and information:
            self.tracker.add_patient_record(name, information)
            self.tracker.save_to_file()
            messagebox.showinfo("Record Submission", "Patient record added successfully.")
            self.update_patient_records_display()
            window.destroy()
        else:
            messagebox.showerror("Record Submission", "Please enter both patient name and information.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientTrackerApp(root)
    root.mainloop()