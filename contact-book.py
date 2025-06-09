import tkinter as tk
from tkinter import messagebox
import pandas as pd

contacts = []

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#f2f2f2")
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="📒 Contact Book", font=("Helvetica", 24, "bold"), fg="#333", bg="#f2f2f2")
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self.root, text="Search by Name:", font=("Helvetica", 12), bg="#f2f2f2").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.search_entry = tk.Entry(self.root, font=("Helvetica", 12), width=25)
        self.search_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

        button_frame = tk.Frame(self.root, bg="#f2f2f2")
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        btn_style = {
            "font": ("Helvetica", 10, "bold"),
            "bg": "#4CAF50",
            "fg": "white",
            "padx": 10,
            "pady": 5,
            "bd": 0,
            "activebackground": "#45a049"
        }

        tk.Button(button_frame, text="➕ Add", command=self.add_contact, **btn_style).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="✏️ Edit", command=self.edit_contact, **btn_style).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="❌ Delete", command=self.delete_contact, **btn_style).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="🔍 Search", command=self.search_contact, **btn_style).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="📃 View All", command=self.view_contacts_list, **btn_style).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="🚪 Exit", command=self.root.destroy, **btn_style).grid(row=1, column=2, padx=5, pady=5)

        list_frame = tk.Frame(self.root)
        list_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.contact_listbox = tk.Listbox(list_frame, font=("Helvetica", 11), yscrollcommand=self.scrollbar.set, width=50, height=10)
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.contact_listbox.yview)

    def add_contact(self):
        win, name_entry, number_entry, email_entry, address_entry = self.create_input_window("New Contact")

        def save():
            name = name_entry.get()
            number = number_entry.get()
            email = email_entry.get()
            address = address_entry.get()
            if not name or not number or not email or not address:
                messagebox.showwarning("Missing Fields", "All fields are required")
                return
            try:
                contacts.append({'Name': name, 'Number': int(number), 'Email': email, 'Address': address})
                self.contact_listbox.insert(tk.END, name)
                win.destroy()
                messagebox.showinfo("Success", "Contact added successfully")
            except:
                messagebox.showwarning("Error", "Invalid phone number")

        self.add_save_button(win, save)

    def edit_contact(self):
        name = self.search_entry.get()
        for idx, contact in enumerate(contacts):
            if contact["Name"] == name:
                win, name_entry, number_entry, email_entry, address_entry = self.create_input_window("Edit Contact", contact)

                def save_edit():
                    new_name = name_entry.get()
                    new_number = number_entry.get()
                    new_email = email_entry.get()
                    new_address = address_entry.get()
                    if not new_name or not new_number or not new_email or not new_address:
                        messagebox.showwarning("Missing Fields", "All fields are required")
                        return
                    try:
                        contacts[idx] = {
                            'Name': new_name,
                            'Number': int(new_number),
                            'Email': new_email,
                            'Address': new_address
                        }
                        for i in range(self.contact_listbox.size()):
                            if self.contact_listbox.get(i) == name:
                                self.contact_listbox.delete(i)
                                self.contact_listbox.insert(tk.END, new_name)
                                break
                        win.destroy()
                        messagebox.showinfo("Success", "Contact updated successfully")
                    except:
                        messagebox.showwarning("Error", "Invalid phone number")

                self.add_save_button(win, save_edit)
                return
        messagebox.showwarning("Not Found", "Contact not found")

    def delete_contact(self):
        name = self.search_entry.get()
        for idx, contact in enumerate(contacts):
            if contact["Name"] == name:
                del contacts[idx]
                for i in range(self.contact_listbox.size()):
                    if self.contact_listbox.get(i) == name:
                        self.contact_listbox.delete(i)
                        break
                messagebox.showinfo("Deleted", "Contact deleted")
                return
        messagebox.showwarning("Not Found", "Contact not found")

    def search_contact(self):
        name = self.search_entry.get()
        for contact in contacts:
            if contact["Name"] == name:
                details = pd.DataFrame([contact]).to_string(index=False)
                self.show_text_window("Contact Details", details)
                return
        messagebox.showwarning("Not Found", "Contact not found")

    def view_contacts_list(self):
        if not contacts:
            messagebox.showinfo("Empty", "No contacts to display")
            return
        df = pd.DataFrame(contacts)
        self.show_text_window("All Contacts", df.to_string(index=False))

    def create_input_window(self, title, contact=None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("400x350")
        win.configure(bg="#f9f9f9")

        def create_field(label_text, row, default=""):
            tk.Label(win, text=label_text, font=("Helvetica", 11), bg="#f9f9f9").grid(row=row, column=0, sticky="w", padx=15, pady=5)
            entry = tk.Entry(win, width=40)
            entry.grid(row=row+1, column=0, columnspan=2, padx=15, pady=5)
            entry.insert(0, default)
            return entry

        name_entry = create_field("Name", 0, contact["Name"] if contact else "")
        number_entry = create_field("Phone Number", 2, str(contact["Number"]) if contact else "")
        email_entry = create_field("Email", 4, contact["Email"] if contact else "")
        address_entry = create_field("Address", 6, contact["Address"] if contact else "")

        return win, name_entry, number_entry, email_entry, address_entry

    def add_save_button(self, win, command):
        tk.Button(win, text="💾 Save", font=("Helvetica", 11, "bold"), bg="#2196F3", fg="white",
                  command=command, padx=10, pady=5, bd=0, activebackground="#1976D2").grid(row=8, column=0, pady=20)

    def show_text_window(self, title, text):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("450x400")
        win.configure(bg="#fdfdfd")
        text_box = tk.Text(win, wrap="word", font=("Courier", 10), bg="#f7f7f7")
        text_box.pack(expand=True, fill="both", padx=10, pady=10)
        text_box.insert(tk.END, text)
        text_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Contact Book")
    root.geometry("700x450")
    root.resizable(False, False)
    app = ContactBook(root)
    root.mainloop()