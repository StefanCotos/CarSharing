import tkinter as tk
from time import sleep
from tkinter import messagebox
import requests
import ttkbootstrap as tb
import subprocess
import sys

BACKEND_URL = "http://127.0.0.1:5000"


class CarSharingApp:
    def __init__(self, root):
        self.created_subprocess = None
        self.state_label = None
        self.cars_listbox = None
        self.password_entry = None
        self.username_entry = None
        self.root = root
        self.root.title("CarSharing App")
        self.root.geometry("550x750")
        self.root.resizable(False, False)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.phone = tk.StringVar()
        self.driver_license = tk.StringVar()
        self.location = tk.StringVar()
        self.is_logged_in = False
        self.current_car_id = None

        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Initial screen with login/register options"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tb.Label(self.root, text="Welcome to CarSharing", font=("Arial", 20)).pack(pady=120)

        login_button = tb.Button(self.root, text="Login", command=self.show_login_screen,
                                 style="primary", width=20)
        login_button.pack(pady=10)

        register_button = tb.Button(self.root, text="Register", command=self.show_register_screen,
                                    style="success", width=20)
        register_button.pack(pady=10)

    def show_login_screen(self):
        """Login screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tb.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=100)

        tb.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tb.Entry(self.root, textvariable=self.username, width=30)
        self.username_entry.pack(pady=5)

        tb.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tb.Entry(self.root, textvariable=self.password, show="*", width=30)
        self.password_entry.pack(pady=5)

        button_frame = tb.Frame(self.root)
        button_frame.pack(pady=15)

        login_button = tb.Button(button_frame, text="Login", command=self.login, style="primary")
        login_button.pack(side=tk.LEFT, padx=5)

        back_button = tb.Button(button_frame, text="Back", command=self.create_welcome_screen, style="secondary")
        back_button.pack(side=tk.LEFT, padx=5)

    def show_register_screen(self):
        """Register screen with additional fields"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tb.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=80)

        tb.Label(self.root, text="Username:").pack(pady=2)
        tb.Entry(self.root, textvariable=self.username, width=30).pack(pady=2)

        tb.Label(self.root, text="Password:").pack(pady=2)
        tb.Entry(self.root, textvariable=self.password, show="*", width=30).pack(pady=2)

        tb.Label(self.root, text="Phone Number:").pack(pady=2)
        tb.Entry(self.root, textvariable=self.phone, width=30).pack(pady=2)

        tb.Label(self.root, text="Driver License:").pack(pady=2)
        tb.Entry(self.root, textvariable=self.driver_license, width=30).pack(pady=2)

        button_frame = tb.Frame(self.root)
        button_frame.pack(pady=15)

        register_button = tb.Button(button_frame, text="Register", command=self.register, style="success")
        register_button.pack(side=tk.LEFT, padx=5)

        back_button = tb.Button(button_frame, text="Back", command=self.create_welcome_screen, style="secondary")
        back_button.pack(side=tk.LEFT, padx=5)

    def create_location_screen(self):
        """Screen to enter location"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tb.Label(self.root, text="Enter Your Location", font=("Arial", 18)).pack(pady=100)

        tb.Label(self.root, text="City:").pack(pady=5)
        tb.Entry(self.root, textvariable=self.location, width=30).pack(pady=5)

        find_cars_button = tb.Button(self.root, text="Find Available Cars", command=self.create_cars_screen,
                                     style="primary", width=20)
        find_cars_button.pack(pady=15)

        logout_button = tb.Button(self.root, text="Logout", command=self.logout, style="secondary", width=20)
        logout_button.pack(pady=5)

    def create_cars_screen(self):
        """Screen displaying available cars"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tb.Label(self.root, text=f"Available Cars in {self.location.get()}",
                 font=("Arial", 18)).pack(pady=10)

        cars_frame = tb.Frame(self.root)
        cars_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.cars_listbox = tk.Listbox(cars_frame, height=10, width=30, font=("Arial", 12))
        self.cars_listbox.pack(side=tk.LEFT, expand=True, fill="both")
        scrollbar = tk.Scrollbar(cars_frame, orient=tk.VERTICAL, command=self.cars_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cars_listbox.config(yscrollcommand=scrollbar.set)

        button_frame = tb.Frame(self.root)
        button_frame.pack(pady=10)

        refresh_button = tb.Button(button_frame, text="Refresh Cars", command=self.get_cars, style="info")
        refresh_button.pack(side=tk.LEFT, padx=5)

        rent_button = tb.Button(button_frame, text="Rent Selected Car", command=self.start_rental, style="warning")
        rent_button.pack(side=tk.LEFT, padx=5)

        back_button = tb.Button(button_frame, text="Change Location", command=self.create_location_screen,
                                style="secondary")
        back_button.pack(side=tk.LEFT, padx=5)

        logout_button = tb.Button(self.root, text="Logout", command=self.logout, style="secondary")
        logout_button.pack(pady=5)

        self.get_cars()

    def create_car_control_screen(self):
        """Screen to control the rented car"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tb.Label(self.root, text="Car Control Panel", font=("Arial", 18)).pack(pady=30)

        state_frame = tb.Frame(self.root)
        state_frame.pack(pady=10, fill="x", padx=20)

        self.state_label = tb.Label(state_frame, text="Loading car state...", font=("Arial", 12))
        self.state_label.pack()

        control_frame = tb.Frame(self.root)
        control_frame.pack(pady=10)

        lock_button = tb.Button(control_frame, text="Lock Car", command=lambda: self.send_car_command("lock"),
                                style="primary", width=20)
        lock_button.pack(side=tk.LEFT, padx=5, pady=5)

        unlock_button = tb.Button(control_frame, text="Unlock Car", command=lambda: self.send_car_command("unlock"),
                                  style="primary", width=20)
        unlock_button.pack(side=tk.LEFT, padx=5, pady=5)

        control_frame2 = tb.Frame(self.root)
        control_frame2.pack(pady=5)

        open_doors_button = tb.Button(control_frame2, text="Open Doors",
                                      command=lambda: self.send_car_command("open_doors"), style="warning", width=20)
        open_doors_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_doors_button = tb.Button(control_frame2, text="Close Doors",
                                       command=lambda: self.send_car_command("close_doors"), style="warning", width=20)
        close_doors_button.pack(side=tk.LEFT, padx=5, pady=5)

        control_frame3 = tb.Frame(self.root)
        control_frame3.pack(pady=5)

        lights_on_button = tb.Button(control_frame3, text="Lights On",
                                     command=lambda: self.send_car_command("lights_on"), style="info", width=20)
        lights_on_button.pack(side=tk.LEFT, padx=5, pady=5)

        lights_off_button = tb.Button(control_frame3, text="Lights Off",
                                      command=lambda: self.send_car_command("lights_off"), style="info", width=20)
        lights_off_button.pack(side=tk.LEFT, padx=5, pady=5)

        control_frame4 = tb.Frame(self.root)
        control_frame4.pack(pady=5)

        start_button = tb.Button(control_frame4, text="Start Engine",
                                 command=lambda: self.send_car_command("start_engine"), style="success", width=20)
        start_button.pack(side=tk.LEFT, padx=5, pady=5)

        stop_button = tb.Button(control_frame4, text="Stop Engine",
                                command=lambda: self.send_car_command("stop_engine"), style="danger", width=20)
        stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        return_button = tb.Button(self.root, text="Return Car", command=self.end_rental, style="danger", width=20)
        return_button.pack(pady=15)

        refresh_button = tb.Button(self.root, text="Refresh Car State", command=self.update_car_state,
                                   style="secondary")
        refresh_button.pack(pady=5)

        self.update_car_state()

    def login(self):
        response = requests.post(BACKEND_URL + "/login",
                                 json={"name": self.username.get(), "password": self.password.get()})
        if response.json()["success"]:
            self.is_logged_in = True
            self.create_location_screen()
        else:
            messagebox.showerror("Login", "Invalid credentials!")

    def register(self):
        response = requests.post(BACKEND_URL + "/register",
                                 json={
                                     "name": self.username.get(),
                                     "password": self.password.get(),
                                     "phoneNumber": self.phone.get(),
                                     "driverLicense": self.driver_license.get()
                                 })
        if response.status_code == 200 and response.content and response.json().get("success", False):
            messagebox.showinfo("Register", "Registration successful! Please login.")
            self.show_login_screen()
        else:
            messagebox.showerror("Register", response.json()["message"])

    def logout(self):
        self.is_logged_in = False
        self.username.set("")
        self.password.set("")
        self.phone.set("")
        self.driver_license.set("")
        self.location.set("")
        self.current_car_id = None
        self.create_welcome_screen()

    def get_cars(self):
        self.cars_listbox.delete(0, tk.END)
        try:
            response = requests.get(BACKEND_URL + f"/cars?location={self.location.get()}")
            cars = response.json()["cars"]

            if not cars:
                self.cars_listbox.insert(tk.END, "No cars available in this location")
                return

            for car in cars:
                if not car.get('rented', False):  # Only show available cars
                    self.cars_listbox.insert(tk.END, f"{car['id']} - {car['vin']} ({car['location']})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch cars: {str(e)}")

    def start_rental(self):
        selected = self.cars_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a car first!")
            return

        # Check if user has a valid driver license
        try:
            response = requests.get(BACKEND_URL + f"/check_license?username={self.username.get()}")
            user_data = response.json()

            if not user_data.get("driverLicense"):
                messagebox.showerror("Error", "You must have a valid driver license to rent a car!")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Could not verify driver license: {str(e)}")
            return

        car_id = int(self.cars_listbox.get(selected[0]).split(" - ")[0])

        response = requests.post(BACKEND_URL + "/rent_car",
                                 json={"car_id": car_id, "user": self.username.get()})

        if response.json().get("success", False):
            self.current_car_id = car_id
            requests.post(BACKEND_URL + "/send_command", json={"car_id": car_id, "command": "unlock"})
            messagebox.showinfo("Rental", "Car unlocked! You can now control the car.")

            self.created_subprocess = subprocess.Popen([sys.executable, "car.py", str(car_id)])

            self.create_car_control_screen()
        else:
            messagebox.showerror("Error", response.json().get("message", "Failed to rent car"))

    def end_rental(self):
        if not self.current_car_id:
            messagebox.showerror("Error", "No car is currently rented!")
            return

        response = requests.get(BACKEND_URL + f"/get_state/{self.current_car_id}")
        car_state = response.json().get("state", {})

        if not car_state.get("doors_closed", False):
            messagebox.showerror("Error", "Please close all doors before returning the car!")
            return

        if not car_state.get("lights_off", False):
            messagebox.showerror("Error", "Please turn off the lights before returning the car!")
            return

        if not car_state.get("engine_off", True):  # Assume engine is off by default
            messagebox.showerror("Error", "Please turn off the engine before returning the car!")
            return

        self.show_payment_screen()

    def show_payment_screen(self):
        """Display payment simulation screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Calculate a random rental cost
        import random
        rental_cost = round(random.uniform(15.0, 50.0), 2)

        tb.Label(self.root, text="Payment Required", font=("Arial", 20)).pack(pady=50)
        tb.Label(self.root, text=f"Total Cost: ${rental_cost}", font=("Arial", 16)).pack(pady=20)

        payment_frame = tb.Frame(self.root)
        payment_frame.pack(pady=20)

        tb.Label(payment_frame, text="Card Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        card_entry = tb.Entry(payment_frame, width=20)
        card_entry.grid(row=0, column=1, padx=5, pady=5)
        card_entry.insert(0, "4111 1111 1111 1111")

        tb.Label(payment_frame, text="Expiry Date:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        exp_entry = tb.Entry(payment_frame, width=20)
        exp_entry.grid(row=1, column=1, padx=5, pady=5)
        exp_entry.insert(0, "12/25")

        tb.Label(payment_frame, text="CVV:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        cvv_entry = tb.Entry(payment_frame, width=20)
        cvv_entry.grid(row=2, column=1, padx=5, pady=5)
        cvv_entry.insert(0, "123")

        button_frame = tb.Frame(self.root)
        button_frame.pack(pady=20)

        pay_button = tb.Button(button_frame, text="Pay Now",
                               command=lambda: self.process_payment(rental_cost),
                               style="success", width=15)
        pay_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tb.Button(button_frame, text="Cancel",
                                  command=self.create_car_control_screen,
                                  style="danger", width=15)
        cancel_button.pack(side=tk.LEFT, padx=10)

    def process_payment(self, amount):
        """Simulate payment processing"""
        # Show processing animation/message
        messagebox.showinfo("Processing", f"Processing payment of ${amount}...")

        # Lock the car before completing rental
        requests.post(BACKEND_URL + "/send_command", json={"car_id": self.current_car_id, "command": "lock"})

        # Complete the rental return
        response = requests.post(BACKEND_URL + "/stop_rent",
                                 json={"car_id": self.current_car_id, "user": self.username.get()})

        if response.json().get("success", False):
            messagebox.showinfo("Payment", f"Payment of ${amount} successful!\n"
                                           f"Thank you for using our service.")
            self.created_subprocess.terminate()
            self.current_car_id = None
            self.create_location_screen()
        else:
            messagebox.showerror("Error", response.json().get("message", "Failed to process payment"))

    def send_car_command(self, command):
        if not self.current_car_id:
            messagebox.showerror("Error", "No car is currently rented!")
            return

        response = requests.post(BACKEND_URL + "/send_command",
                                 json={"car_id": self.current_car_id, "command": command})

        if response.json().get("success", False):
            messagebox.showinfo("Success", f"Command '{command}' sent successfully!")
            sleep(2)
            self.update_car_state()
        else:
            messagebox.showerror("Error", f"Failed to send command '{command}'")

    def update_car_state(self):
        if not self.current_car_id:
            self.state_label.config(text="No car is currently rented!")
            return

        response = requests.get(BACKEND_URL + f"/get_state/{self.current_car_id}")
        car_state = response.json().get("state", {})

        state_text = f"Locked: {car_state.get('locked')}\n" \
                     f"Doors Closed: {car_state.get('doors_closed')}\n" \
                     f"Lights Off: {car_state.get('lights_off')}\n" \
                     f"Engine Off: {car_state.get('engine_off')}"

        self.state_label.config(text=state_text)

        
if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = CarSharingApp(root)
    root.mainloop()
