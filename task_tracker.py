import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TASKS_FILE = "tasks.json"

class TaskTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Daily Task Tracker")
        self.root.geometry("950x500") 


        self.tasks = self.load_tasks()

        
        # input area
        self.entry = tk.Entry(root, width=40,bg="lightyellow")
        self.entry.insert(0, "Type your task here...")
        self.entry.grid(row=0, column=0, padx=10, pady=10)

        self.priority_var = tk.StringVar()
        self.priority_var.set("medium")
        tk.OptionMenu(root, self.priority_var, "low", "medium", "high").grid(row=0, column=1)

        tk.Button(root, text="Add Task", command=self.add_task).grid(row=0, column=2, padx=10)

        # Listboxes and labels
        tk.Label(root, text="🟡 Checklist").grid(row=1, column=0)
        self.checklist_box = tk.Listbox(root, selectmode=tk.SINGLE, width=40)
        self.checklist_box.grid(row=2, column=0, padx=10)

        tk.Label(root, text="✅ Completed").grid(row=1, column=1)
        self.completed_box = tk.Listbox(root, width=40)
        self.completed_box.grid(row=2, column=1, padx=10)

        tk.Label(root, text="❌ Incomplete").grid(row=1, column=2)
        self.incomplete_box = tk.Listbox(root, width=40)
        self.incomplete_box.grid(row=2, column=2, padx=10)

        # Buttons
        tk.Button(root, text="Mark Completed", command=self.mark_completed).grid(row=3, column=0, pady=10)
        tk.Button(root, text="Mark Incomplete", command=self.mark_incomplete).grid(row=3, column=1)
        tk.Button(root, text="Save Tasks", command=self.save_tasks).grid(row=3, column=2)

        tk.Button(root,text="🗑 Delete Task",command=self.delete_task).grid(row=4,column=0,pady=5)
        tk.Button(root,text="✏️ Edit Task",command=self.edit_task).grid(row=4,column=1)
        
        self.refresh_lists()

    def add_task(self):
        task = self.entry.get().strip()
        priority = self.priority_var.get()
        print("DEBUG ➤ You typed:", task, "with priority:", priority)
        if task:
            self.tasks["checklist"].append({"name": task, "priority": priority})
            self.entry.delete(0, tk.END)
            self.refresh_lists()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def mark_completed(self):
        index = self.checklist_box.curselection()
        if index:
            task = self.tasks["checklist"].pop(index[0])
            self.tasks["completed_tasks"].append(task)
            self.refresh_lists()

    def mark_incomplete(self):
        index = self.checklist_box.curselection()
        if index:
            task = self.tasks["checklist"].pop(index[0])
            self.tasks["incomplete_tasks"].append(task)
            self.refresh_lists()
    
    def delete_task(self):
        index=self.checklist_box.curselection()
        if index:
            self.tasks["checklist"].pop(index[0])
            self.refresh_lists()
            return
        
        index=self.completed_box.curselection()
        if index:
            self.tasks["completed_tasks"].pop(index[0])
            self.refresh_lists()
            return
        
        index=self.incomplete_box.curselection()
        if index:
            self.tasks["incomplete_tasks"].pop(index[0])
            self.refresh_lists()
            return
   
        messagebox.showwarning("Delete Error","Please select a task to delete.")

    
    def edit_task(self):
        index=self.checklist_box.curselection()
        if not index:
            messagebox.showwarning("Edit Error", "Please select a task to edit.")
            return

        task=self.tasks["checklist"][index[0]]

        new_name=simpledialog.askstring("Edit Task", "Enter new task name:", initialvalue=task["name"])
        if new_name:
            task["name"]=new_name

        new_priority=simpledialog.askstring("Edit Priority(low/medium/high)", "Edit task priority:",initialvalue=["priority"])
        if new_priority and new_priority.lower() in ["low", "medium", "high"]:
            task["priority"]=new_priority.lower()

        else:
            messagebox.showwarning("Edit Error", "Invalid priority. Please enter low, medium, or high.")    

        self.refresh_lists()    
    
    
    def refresh_lists(self):
        self.checklist_box.delete(0, tk.END)
        for task in self.tasks["checklist"]:
            self.checklist_box.insert(tk.END, f"{task['name']} ({task['priority']})")

        self.completed_box.delete(0, tk.END)
        for task in self.tasks["completed_tasks"]:
            self.completed_box.insert(tk.END, f"{task['name']} ({task['priority']})")

        self.incomplete_box.delete(0, tk.END)
        for task in self.tasks["incomplete_tasks"]:
            self.incomplete_box.insert(tk.END, f"{task['name']} ({task['priority']})")

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)
        messagebox.showinfo("Success", "Tasks saved successfully!")

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        else:
            return {"checklist": [], "completed_tasks": [], "incomplete_tasks": []}


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()

