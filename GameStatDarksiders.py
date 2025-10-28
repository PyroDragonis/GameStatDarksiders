
# GameStatDarksiders.py
"""
Main GUI application for GameStatDarksiders.
Provides Create, Read, Update, Delete (CRUD) for Character records using SQLAlchemy + SQLite,
and a Tkinter GUI with buttons for all operations.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from models import SessionLocal, Character

# Create a session factory (SQLAlchemy)
session = SessionLocal()

# ----------------- Helper DB functions -----------------
def add_character_db(name, weapon, level, realm):
    char = Character(name=name, weapon=weapon, level=level, realm=realm)
    session.add(char)
    session.commit()
    return char

def update_character_db(char_id, name, weapon, level, realm):
    char = session.get(Character, char_id)
    if char is None:
        return None
    char.name = name
    char.weapon = weapon
    char.level = level
    char.realm = realm
    session.commit()
    return char

def delete_character_db(char_id):
    char = session.get(Character, char_id)
    if char is None:
        return False
    session.delete(char)
    session.commit()
    return True

def get_all_characters():
    return session.query(Character).order_by(Character.id).all()

# ----------------- GUI callbacks -----------------
def load_characters():
    listbox.delete(0, tk.END)
    for c in get_all_characters():
        listbox.insert(tk.END, f"{c.id}: {c.name} - Lv {c.level} ({c.weapon}) [{c.realm}]")
    clear_selection_state()

def add_character():
    name = entry_name.get().strip()
    weapon = entry_weapon.get().strip()
    level_text = entry_level.get().strip()
    realm = entry_realm.get().strip()

    if not (name and weapon and level_text and realm):
        messagebox.showwarning("Missing fields", "All fields are required.")
        return

    try:
        level = int(level_text)
        if level < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid level", "Level must be a non-negative integer.")
        return

    add_character_db(name, weapon, level, realm)
    messagebox.showinfo("Added", f"{name} added.")
    clear_entries()
    load_characters()

def on_select(event=None):
    sel = listbox.curselection()
    if not sel:
        return
    idx = sel[0]
    text = listbox.get(idx)
    # parse "id: name - Lv X (weapon) [realm]"
    try:
        char_id = int(text.split(":", 1)[0])
    except Exception:
        return
    char = session.get(Character, char_id)
    if not char:
        return
    # populate entries
    entry_name.delete(0, tk.END); entry_name.insert(0, char.name)
    entry_weapon.delete(0, tk.END); entry_weapon.insert(0, char.weapon)
    entry_level.delete(0, tk.END); entry_level.insert(0, str(char.level))
    entry_realm.delete(0, tk.END); entry_realm.insert(0, char.realm)
    # store selected id in hidden label
    selected_id_var.set(str(char.id))

def update_character():
    selected = selected_id_var.get()
    if not selected:
        messagebox.showwarning("Select record", "Select a record from the list to update.")
        return
    try:
        char_id = int(selected)
    except ValueError:
        messagebox.showerror("Error", "Invalid selection.")
        return

    name = entry_name.get().strip()
    weapon = entry_weapon.get().strip()
    level_text = entry_level.get().strip()
    realm = entry_realm.get().strip()

    if not (name and weapon and level_text and realm):
        messagebox.showwarning("Missing fields", "All fields are required.")
        return

    try:
        level = int(level_text)
        if level < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid level", "Level must be a non-negative integer.")
        return

    updated = update_character_db(char_id, name, weapon, level, realm)
    if updated:
        messagebox.showinfo("Updated", f"Character {name} updated.")
        load_characters()
    else:
        messagebox.showerror("Not found", "Character not found in database.")

def delete_character():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select record", "Select a record from the list to delete.")
        return
    idx = sel[0]
    text = listbox.get(idx)
    try:
        char_id = int(text.split(":", 1)[0])
    except Exception:
        messagebox.showerror("Error", "Could not parse selected record.")
        return

    char = session.get(Character, char_id)
    if not char:
        messagebox.showerror("Error", "Record not found.")
        load_characters()
        return

    answer = messagebox.askyesno("Confirm delete", f"Delete {char.name} (ID {char.id})?")
    if not answer:
        return

    if delete_character_db(char_id):
        messagebox.showinfo("Deleted", f"{char.name} deleted.")
        load_characters()
    else:
        messagebox.showerror("Error", "Delete failed.")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_weapon.delete(0, tk.END)
    entry_level.delete(0, tk.END)
    entry_realm.delete(0, tk.END)
    clear_selection_state()

def clear_selection_state():
    selected_id_var.set("")
    listbox.selection_clear(0, tk.END)

# ----------------- Build GUI -----------------
root = tk.Tk()
root.title("GameStat Darksiders")
root.geometry("720x480")
root.minsize(660, 420)
root.configure(bg="#121212")

# Top frame for form
frame_form = tk.Frame(root, bg="#121212", padx=10, pady=10)
frame_form.pack(side=tk.TOP, fill=tk.X)

lbl_name = tk.Label(frame_form, text="Name:", fg="white", bg="#121212")
lbl_name.grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_name = tk.Entry(frame_form, width=30)
entry_name.grid(row=0, column=1, padx=4, pady=4)

lbl_weapon = tk.Label(frame_form, text="Weapon:", fg="white", bg="#121212")
lbl_weapon.grid(row=1, column=0, sticky="e", padx=4, pady=4)
entry_weapon = tk.Entry(frame_form, width=30)
entry_weapon.grid(row=1, column=1, padx=4, pady=4)

lbl_level = tk.Label(frame_form, text="Level:", fg="white", bg="#121212")
lbl_level.grid(row=0, column=2, sticky="e", padx=4, pady=4)
entry_level = tk.Entry(frame_form, width=10)
entry_level.grid(row=0, column=3, padx=4, pady=4)

lbl_realm = tk.Label(frame_form, text="Realm:", fg="white", bg="#121212")
lbl_realm.grid(row=1, column=2, sticky="e", padx=4, pady=4)
entry_realm = tk.Entry(frame_form, width=20)
entry_realm.grid(row=1, column=3, padx=4, pady=4)

# Hidden var to hold selected id
selected_id_var = tk.StringVar(value="")

# Buttons frame
frame_buttons = tk.Frame(root, bg="#121212", padx=10, pady=6)
frame_buttons.pack(side=tk.TOP, fill=tk.X)

btn_add = tk.Button(frame_buttons, text="Add", width=12, command=add_character)
btn_add.pack(side=tk.LEFT, padx=6, pady=6)

btn_update = tk.Button(frame_buttons, text="Update", width=12, command=update_character)
btn_update.pack(side=tk.LEFT, padx=6, pady=6)

btn_delete = tk.Button(frame_buttons, text="Delete", width=12, command=delete_character)
btn_delete.pack(side=tk.LEFT, padx=6, pady=6)

btn_refresh = tk.Button(frame_buttons, text="Refresh", width=12, command=load_characters)
btn_refresh.pack(side=tk.LEFT, padx=6, pady=6)

btn_clear = tk.Button(frame_buttons, text="Clear", width=12, command=clear_entries)
btn_clear.pack(side=tk.LEFT, padx=6, pady=6)

# Listbox + scrollbar
frame_list = tk.Frame(root, bg="#121212", padx=10, pady=8)
frame_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_list, orient=tk.VERTICAL)
listbox = tk.Listbox(frame_list, yscrollcommand=scrollbar.set, font=("Consolas", 10), selectmode=tk.SINGLE)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Bind selection event
listbox.bind("<<ListboxSelect>>", on_select)

# Footer / status
status = tk.Label(root, text="GameStatDarksiders - CRUD GUI (SQLite)", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side=tk.BOTTOM, fill=tk.X)

# Initial load
load_characters()

# Start main loop
if __name__ == "__main__":
    root.mainloop()
