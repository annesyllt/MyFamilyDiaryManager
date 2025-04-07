import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyodbc
from PIL import Image, ImageTk
from datetime import datetime

def get_db_connection(): 
    #Establish Connection to SQL Server
  try:
 
       
        CONNECTION_STRING = ("Driver={ODBC Driver 17 for SQL Server};"
 
                    "Server=LAPTOP-LCV3Q19R;"
 
                    "Database=Project;"
 
                    "Trusted_Connection=yes;")
            #  establish a connection
        conn = pyodbc.connect(CONNECTION_STRING)
 
        #print(" Connection successful!")
        return conn
  except Exception as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
        return None

# ---- Main Application ----
class MyFamilyDiaryManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Family Diary Manager")
        self.geometry("500x400")

        # Create a menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create a container to hold different pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary to store pages
        self.pages = {}

        # Adding pages
        for Page in (LoginPage, RegisterPage, ChildrenPage, EventPage, ThankYouPage):
            page = Page(self.container, self)
            self.pages[Page.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Add menu options
        page_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Navigate Pages", menu=page_menu)
        page_menu.add_command(label="Login Page", command=lambda: self.show_page("LoginPage"))
        page_menu.add_command(label="Register Page", command=lambda: self.show_page("RegisterPage"))
        page_menu.add_command(label="ChildrenPage", command=lambda: self.show_page("ChildrenPage"))
        page_menu.add_command(label="Diary Page", command=lambda: self.show_page("EventPage"))
        page_menu.add_command(label="Thank You Page", command=lambda: self.show_page("ThankYouPage"))

        # Show the first page (Login Page)
        self.show_page("LoginPage")

    # Bring the requested page to the front
    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

# ---- Page 1: Login Page ----
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #Background image
        bunnies_image = Image.open("bunnies.jpg")
        bunnies_image = bunnies_image.resize((490,390))
        bunnies_image = ImageTk.PhotoImage(bunnies_image)

        img_label = tk.Label(self, image = bunnies_image)
        img_label.image = bunnies_image
        img_label.pack(padx=5, pady= 5, fill='both')

        Login_Frame = tk.Frame(self, bg='light pink')
        #Welcome Label
        tk.Label(Login_Frame, text = "Welcome to My Family Diary Manager!", bg='light pink').pack()
        tk.Label(Login_Frame, text="The Place to Get Organised for the Exciting Week Ahead.", bg='light pink').pack()

        #Username labels and input boxes
        Username_Label=tk.Label(Login_Frame, text = "Username:", bg='light pink')
        Username_Label.pack()
    
        self.Username_Entrybox = tk.Entry(Login_Frame)
        self.Username_Entrybox.pack()

        #Password labels and input boxes
        Password_Label=tk.Label(Login_Frame, text="Password:", bg='light pink')
        Password_Label.pack()

        self.Password_Entrybox = tk.Entry(Login_Frame, show="*")
        self.Password_Entrybox.pack()

        Login_Button=tk.Button(Login_Frame, bg='powder blue', text="Login", command=self.verify_login)
        Login_Button.pack(padx=10, pady=10)

        #Register label and input boxes
        Register_Button = tk.Button(Login_Frame, bg='powder blue', text="New User? Register Now!", command=lambda: controller.show_page("RegisterPage"))
        Register_Button.pack(padx=10, pady=10)

        Login_Frame.place (relx='0.375', rely='0.075')
    
    #Function to verify login creditials against those stored in SQL server
    def verify_login(self):
        username = self.Username_Entrybox.get()
        password = self.Password_Entrybox.get()
         
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Passwords WHERE Username = ? AND Password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                self.master.logged_in_user_id = user[0]
                messagebox.showinfo("Login Success", "Welcome to My Family Diary Manager!")
                self.controller.show_page("ChildrenPage")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.") 

# Register Page
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='light pink')

        tk.Label(self, text="Register as a New User", font=("Georgia", 16), fg= 'midnight blue', bg='light pink').place(relx=0.3, rely=0.1)

        tk.Label(self, text="Username:", bg='light pink').place(relx=0.3, rely=0.2, anchor='center')
        self.username_entry = tk.Entry(self)
        self.username_entry.place(relx=0.5, rely=0.2, anchor='center')

        tk.Label(self, text="Password:", bg='light pink').place(relx=0.3, rely=0.25, anchor='center')
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.place(relx=0.5, rely=0.25, anchor='center')

        tk.Button(self, bg='powder blue', text="Register", command=self.register).place(relx=0.5, rely=0.3, anchor='center')

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Both fields are required!")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Passwords (Username, Password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Registration Successful", "You can now log in!")
                self.controller.show_page("LoginPage")
            except pyodbc.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
            conn.close()

# Children Page
class ChildrenPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ChildrenPage.config(self, background='light pink')

        tk.Label(self, text="Your Children's Week", fg= 'midnight blue', bg='light pink', font=("Arial", 16)).pack(padx=10, pady=10)

        childbuttonframe = tk.Frame(self, bg='light pink')

        IdrisButton = tk.Button(childbuttonframe, text="Idris' Events This Week", bg='powder blue', command=self.show_Idris_events)
        IdrisButton.pack(side='left', expand=False, fill='both', padx=5, pady=5)

        LowriButton = tk.Button(childbuttonframe, text="Lowri's Events This Week", bg='powder blue', command=self.show_Lowri_events)
        LowriButton.pack(side='left', expand=False, fill='both', padx=5, pady=5)

        RhoslynButton = tk.Button(childbuttonframe, text="Rhoslyn's Events This Week", bg='powder blue', command=self.show_Rhoslyn_events)
        RhoslynButton.pack(side='left', expand=False, fill='both', padx=5, pady=5)

        childbuttonframe.pack()

        AllChildrenButton = tk.Button(self, text="Go to All Children's Activities Page", fg='midnight blue', bg='cyan', height=3, width=30, command=lambda: controller.show_page("EventPage"))
        AllChildrenButton.pack(expand=False, padx=5, pady=5)

        bottomframe = tk.Frame(self, background='light pink')

        # Add Child button to open toplevel window
        tk.Button(bottomframe, text="Add Child", bg='powder blue', command=self.add_child_window).pack(side = 'left', padx=5, pady=5)
        tk.Button(bottomframe, text="Child Left Home? Erase Child Record:", bg='powder blue', command=self.delete_child_window).pack(side='left', padx=5, pady=5)
        
        bottomframe.pack()

    def add_child(self, add_window, child_firstname_entry, child_surname_entry, school_year_entry, child_class_entry, allergies_entry):
        ChildFirstname = child_firstname_entry.get()
        ChildSurname = child_surname_entry.get()
        ChildYear = school_year_entry.get()
        ChildClass = child_class_entry.get()
        Allergies = allergies_entry.get()

        # Validate input
        if not ChildFirstname or not ChildSurname or not ChildYear or not ChildClass or not Allergies:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        # Insert child information into the database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO ChildDetails (ChildFirstName, ChildSurname, SchoolYear, SchoolClass, Allergies) VALUES (?, ?, ?, ?,?)", (ChildFirstname, ChildSurname, ChildYear, ChildClass, Allergies))
                conn.commit()
                messagebox.showinfo("New Child Added!", f"{ChildFirstname} has been added!")
                self.controller.show_page("EventsPage")
            except pyodbc.IntegrityError:
                messagebox.showerror("Error", "This child has already been added!")
            conn.close()

    # Function to delete a child record from SQL server
    def delete_child(self, listbox):    
        try:
        # Get the selected child from the listbox
            selected_index = listbox.curselection()[0]
            child = listbox.get(selected_index)
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ChildDetails WHERE ChildFirstName = ?", (child,))
                conn.commit()
                conn.close()
            # Remove the child from the listbox
                listbox.delete(selected_index)
                messagebox.showinfo("Success", f"'{child}' has been deleted!")
        except IndexError:
            messagebox.showwarning("Warning", "No child selected to delete.")        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {child}'s record could not be deleted.")

    def load_children(self, listbox):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ChildFirstName FROM ChildDetails")
            children = cursor.fetchall()
        
        # Clear the listbox and insert the children's first names
        listbox.delete(0, tk.END)
        for child in children:
            listbox.insert(tk.END, child[0])
        conn.close()

    # Show child 1's details
    def show_Idris_events(self):
        Idris_window = tk.Toplevel(self)
        Idris_window.title("Idris' window")
        Idris_window.geometry("400x400")
        Idris_window.config(bg='lawn green')
        tk.Button(Idris_window, text='Close window', bg='powder blue', command=Idris_window.destroy).pack(side= 'bottom', padx=5, pady=5)

        #Fetch information from the database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Weekday, EventName, EventTime FROM EventDetails WHERE Childfirstname = 'Idris'")
            IdrisEvents = cursor.fetchall()
            for event in IdrisEvents:
            # Format the events into a readable string
                print_events = f"{event[0]}: {event[1]} at {event[2]}"
                tk.Label(Idris_window, bg='lawn green', text=print_events).pack()
                conn.close()

    # Show child 2's details
    def show_Lowri_events(self):
        Lowri_window = tk.Toplevel(self)
        Lowri_window.title("Lowri's window")
        Lowri_window.geometry("400x400")
        Lowri_window.config(bg='MediumPurple1')
        tk.Button(Lowri_window, text='Close window', bg='powder blue', command=Lowri_window.destroy).pack(side= 'bottom', padx=5, pady=5)

        #Fetch information from the database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Weekday, EventName, EventTime FROM EventDetails WHERE Childfirstname = 'Lowri'")
            LowriEvents = cursor.fetchall()
            for event in LowriEvents:
            # Format the events into a readable string
                print_events = f"{event[0]}: {event[1]} at {event[2]}"
                tk.Label(Lowri_window, bg='MediumPurple1', text=print_events).pack()
            conn.close()

    # Show child 3's details
    def show_Rhoslyn_events(self):
        Rhoslyn_window = tk.Toplevel(self)
        Rhoslyn_window.title("Rhoslyn's window")
        Rhoslyn_window.geometry("400x400")
        Rhoslyn_window.config(bg='light pink')
        # Button to close the 'Add Child' window  
        tk.Button(Rhoslyn_window, text='Close window', bg='powder blue', command=Rhoslyn_window.destroy).pack(side= 'bottom', padx=5, pady=5)

        #Fetch information from the database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Weekday, EventName, EventTime FROM EventDetails WHERE Childfirstname = 'Rhoslyn'")
            RhoslynEvents = cursor.fetchall()
            for event in RhoslynEvents:
            # Format the events into a readable string
                print_events = f"{event[0]}: {event[1]} at {event[2]}"
                tk.Label(Rhoslyn_window, bg='light pink', text=print_events).pack()
            conn.close()  

    # Open new window to add new child detials
    def add_child_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Child")
        add_window.geometry("400x400")
        add_window.config(bg='light pink')

        # Labels and Entry boxes to add all child details
        tk.Label(add_window, fg='midnight blue', bg='light pink', text="Child First Name:").pack()
        child_firstname_entry = tk.Entry(add_window)
        child_firstname_entry.pack()
        tk.Label(add_window,fg='midnight blue', bg='light pink', text="Child Surname:").pack()
        child_surname_entry = tk.Entry(add_window)
        child_surname_entry.pack()
        tk.Label(add_window, text="School Year:", fg='midnight blue', bg='light pink').pack()
        school_year_entry = tk.Entry(add_window)
        school_year_entry.pack()
        tk.Label(add_window, text="School Class:", fg='midnight blue', bg='light pink').pack()
        child_class_entry = tk.Entry(add_window)
        child_class_entry.pack()
        tk.Label(add_window, fg='midnight blue', bg='light pink', text="Allergies:").pack()
        allergies_entry = tk.Entry(add_window)
        allergies_entry.pack()

        tk.Button(
            add_window, 
            text="Add child", bg='powder blue',
            command=lambda: self.add_child(
                add_window,
                child_firstname_entry,
                child_surname_entry,
                school_year_entry,
                child_class_entry,
                allergies_entry),
                ).pack()

        # Button to close the 'Add Child' window  
        tk.Button(add_window, text='Close window', bg='powder blue', command=add_window.destroy).pack(side= 'bottom', padx=5, pady=5)

    # Open a new window to amend child details
    def change_child_window(self):
        change_window = tk.Toplevel(self)
        change_window.title("Change Child Details")
        change_window.geometry("400x400")
        change_window.config(bg='light pink')

        # Create a Listbox to list all children's first names
        listbox = tk.Listbox(change_window, width=40, height=10)
        listbox.pack(padx=10, pady=10)

        # Load children into the listbox
        self.load_children(listbox)

        # Add Buttons
        tk.Button(change_window, text="Change Child Record").pack() 
        tk.Button(change_window, text='Close window', command=change_window.destroy).pack(side= 'bottom', padx=5, pady=5)
        
    # Open a new window to delete child details
    def delete_child_window(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Delete Child")
        delete_window.geometry("400x400")
        delete_window.config(bg='light pink')

        # A listbox to list all children's first names
        listbox = tk.Listbox(delete_window, width=40, height=10)
        listbox.pack(padx=10, pady=10)

        # Load children into the listbox
        self.load_children(listbox)

        # Add Buttons
        tk.Button(delete_window, text="Erase Child Record", command=lambda: self.delete_child(listbox)).pack()
        tk.Button(delete_window, text='Close window', command=delete_window.destroy).pack(side= 'bottom', padx=5, pady=5)

# Event Page to display all events in a listbox and buttons
class EventPage(tk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background= 'light pink')

        listbox = tk.Listbox(self, width=60, height=15)
        listbox.pack(padx=10, pady=10)

        # Load events into the listbox
        self.load_events(listbox)

        # Buttons to add, change and remove an event. 
        tk.Button(self, text="Highlight and click on an Event to Remove it", command=lambda:self.delete_event(listbox)).pack(padx=5, pady=5)
        tk.Button(self, text="Add an Event.", command=self.add_event_window).pack()
        tk.Button(self, text="Finish & Exit", command=lambda: controller.show_page("ThankYouPage")).pack(padx=5, pady=5)

    # Load all events from the database into the listbox
    def load_events(self, listbox):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ChildFirstName, EventName, EventVenue, Weekday, EventTime FROM EventDetails",)
            all_events = cursor.fetchall()
            for event in all_events:
                print_events = f"{event[0]}: {event[1]} at {event[2]} on {event[3]} at {event[4]}."
                listbox.insert(tk.END, print_events)
            conn.close()

    # Open a new window to add event details
    def add_event_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Event")
        add_window.geometry("400x500")
        add_window.config(bg='light pink')

        # Buttons, entry boxes etc. to add event details
        tk.Label(add_window, text="Add Event Details:", bg='light pink', fg='midnight blue').pack(side='left', padx=5,pady=5)
        tk.Label(add_window, text="Event Name:", bg='light pink', fg='midnight blue').pack()
        event_name_entry = tk.Entry(add_window, width=30)
        event_name_entry.pack()
        tk.Label(add_window, text='Event Type:', bg='light pink', fg='midnight blue').pack()
        optionslist = ["School", "Regular", "Social"]
        value_inside = tk.StringVar(add_window)
        value_inside.set("Select an Event Type:")
        Event_type_question = tk.OptionMenu(add_window, value_inside, *optionslist)
        Event_type_question.pack()
        submit_button = tk.Button(add_window, text="Submit", bg='powder blue').pack()
        tk.Label(add_window, text="Event Venue:", bg='light pink', fg='midnight blue').pack()
        event_venue_entry = tk.Entry(add_window, width=30)
        event_venue_entry.pack()
        tk.Label(add_window, text="Other Details:", bg='light pink', fg='midnight blue').pack()
        other_details_entry = tk.Entry(add_window, width=30)
        other_details_entry.pack()
        tk.Label(add_window, text="Child First Name", bg='light pink', fg='midnight blue').pack()
        child_name_entry = tk.Entry(add_window, width=30)
        child_name_entry.pack()
        tk.Label(add_window, text="Event Date in format YYYY-MM-DD", bg='light pink', fg='midnight blue').pack()
        event_date_entry = tk.Entry(add_window, width=30)
        event_date_entry.pack()
        tk.Label(add_window, text="Event Time in format HH:MM:SS", bg='light pink', fg='midnight blue').pack()
        event_time_entry = tk.Entry(add_window, width=30)
        event_time_entry.pack()
        tk.Label(add_window, text="Weekday", bg= 'light pink', fg='midnight blue').pack()
        weekday_entry = tk.Entry(add_window, width=30)
        weekday_entry.pack()
    
        tk.Button(add_window, text="Add event", bg='powder blue', command=lambda: self.add_event(event_name_entry, value_inside, event_venue_entry,
        other_details_entry, child_name_entry, event_date_entry,
        event_time_entry, weekday_entry
        )).pack()

        # Button and function to close the 'Add Event' window  
        tk.Button(add_window, text='Close window', bg='powder blue', command=add_window.destroy).pack(side= 'bottom', padx=5, pady=5)

    # function to add new event details to sequel server
    def add_event(self, event_name_entry, value_inside, event_venue_entry, other_details_entry, child_name_entry, event_date_entry, event_time_entry, weekday_entry):
        # Get the values from the entry boxes and dropdown
        EventName = event_name_entry.get()
        EventType = value_inside.get()
        EventVenue = event_venue_entry.get()
        OtherDetails = other_details_entry.get()
        ChildName = child_name_entry.get()
        EventDate = event_date_entry.get()
        EventTime = event_time_entry.get()
        Weekday = weekday_entry.get()

        # Validate input
        if not EventName or not EventType or not EventVenue or not OtherDetails or not ChildName or not EventDate or not EventTime or not Weekday:
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        
        # Ensure EventType is not the default value
        if EventType == "Select an Event Type:":
            messagebox.showwarning("Input Error", "Please select an Event Type.")
            return
        
        # Validate EventDate format (YYYY-MM-DD)
        try:
            datetime.strptime(EventDate, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Event Date must be in YYYY-MM-DD format.")

        # Validate EventTime format (HH:MM:SS)
        try:
            datetime.strptime(EventTime, "%H:%M:%S")
        except ValueError:
            messagebox.showwarning("Input Error", "Event Time must be in HH:MM:SS format.")

        # Insert event information into the database
        conn = get_db_connection()    
        if conn:
            cursor = conn.cursor()
        try:    
            cursor.execute("INSERT INTO EventDetails (EventName, EventType, EventVenue, OtherDetails, ChildFirstName, EventDate, EventTime, Weekday) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
            (EventName, EventType, EventVenue, OtherDetails, ChildName, EventDate, EventTime, Weekday))
            conn.commit()
            messagebox.showinfo("New Child Added!", f"'{EventName}' has been added!")
            self.controller.show_page("EventPage")
        except Exception as e:
            messagebox.showerror("Error", f"An error has occurred: {e}.")
        finally:
            conn.close()

    def delete_event(self, listbox):
        try:
            # Get the selected event from the listbox
            selected_index = listbox.curselection()[0]
            if not selected_index:
                messagebox.showwarning("Warning", "No event selected to delete.")
                return
            
            selected_event = listbox.get(selected_index)

            # Extract event details from the selected string
            event_parts = selected_event.split(":")
            if len(event_parts) < 2:
                messagebox.showerror("Error", "Invalid event format.")
                return
            
            child_name = event_parts[0].strip()
            event_details = event_parts[1].strip()
            event_name = event_details.split(" at ")[0].strip()

            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM EventDetails WHERE ChildFirstName = ? AND EventName = ?", (child_name, event_name))
                conn.commit()
                conn.close()

                # Remove the event from the listbox
                listbox.delete(selected_index)
                messagebox.showinfo("Success", f"'{event_name}' for {child_name} has been deleted!")
        except IndexError:
            messagebox.showwarning("Warning", "No event selected to delete.")        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}.")

# Thank You Page ----
class ThankYouPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ThankYouPage.config(self, background='light pink')

        tk.Label(self, text="Thank You!", font=("Arial", 20),fg = 'midnight blue', bg="light pink").pack(pady=20)
        tk.Label(self, text="Thank you for using the My Family Diary Manager App!", font=("Arial", 14), fg = "midnight blue", bg= 'light pink').pack(pady=10)

        tk.Button(self, text="Go back to Login Page", command=lambda: controller.show_page("LoginPage")).pack(pady=5)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=5)

# Run the application ----
if __name__ == "__main__":
    app = MyFamilyDiaryManager()
    app.mainloop()