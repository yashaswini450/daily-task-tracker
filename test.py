import tkinter as tk

root = tk.Tk()
root.title("Input Test")
root.geometry("500x150")

# Entry field
entry = tk.Entry(root, width=40, bg="lightyellow")
entry.grid(row=0, column=0, padx=10, pady=10)
entry.insert(0, "Type something here...")

# Priority dropdown
priority_var = tk.StringVar(value="medium")
priority_menu = tk.OptionMenu(root, priority_var, "low", "medium", "high")
priority_menu.grid(row=0, column=1)

# Add button
def on_add():
    print("Task:", entry.get(), "Priority:", priority_var.get())

tk.Button(root, text="Add Task", command=on_add).grid(row=0, column=2, padx=10)

root.mainloop()
