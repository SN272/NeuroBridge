import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import time # Still useful for simulating a brief delay if desired, though less critical for GUI

class StudyAgentApp:
    def __init__(self, master):
        self.master = master
        master.title("Personal Study Agent")
        master.geometry("800x600") # Set a default window size
        master.resizable(True, True) # Allow window resizing
        master.configure(bg="#e0f7fa") # Light blue background

        self.subjects = []

        # --- Header ---
        self.header_frame = tk.Frame(master, bg="#00796b", pady=10)
        self.header_frame.pack(fill="x")
        self.header_label = tk.Label(self.header_frame, text="📚 Your Personal Study Planner! 🚀",
                                     font=("Arial", 20, "bold"), fg="white", bg="#00796b")
        self.header_label.pack()

        # --- Subject Input Section ---
        self.input_frame = tk.Frame(master, bg="#b2dfdb", padx=15, pady=15, bd=2, relief="groove")
        self.input_frame.pack(pady=15, padx=20, fill="x")

        self.subject_label = tk.Label(self.input_frame, text="Enter Subject:", font=("Arial", 12), bg="#b2dfdb")
        self.subject_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.subject_entry = tk.Entry(self.input_frame, width=40, font=("Arial", 12), bd=2, relief="solid")
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.subject_entry.bind("<Return>", self.add_subject_from_entry) # Allow adding with Enter key

        self.add_button = tk.Button(self.input_frame, text="Add Subject", command=self.add_subject,
                                    font=("Arial", 10, "bold"), bg="#4caf50", fg="white",
                                    activebackground="#66bb6a", activeforeground="white",
                                    relief="raised", bd=3, cursor="hand2")
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        self.clear_subjects_button = tk.Button(self.input_frame, text="Clear All Subjects", command=self.clear_subjects,
                                               font=("Arial", 10), bg="#ff7043", fg="white",
                                               activebackground="#ff8a65", activeforeground="white",
                                               relief="raised", bd=3, cursor="hand2")
        self.clear_subjects_button.grid(row=0, column=3, padx=5, pady=5)

        self.subjects_list_label = tk.Label(self.input_frame, text="Subjects to Study:", font=("Arial", 12, "bold"), bg="#b2dfdb")
        self.subjects_list_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        self.subjects_display = scrolledtext.ScrolledText(self.input_frame, width=60, height=4, font=("Arial", 10), bd=2, relief="solid", state="disabled")
        self.subjects_display.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        self.input_frame.grid_columnconfigure(1, weight=1) # Allow subject entry to expand

        # --- Plan Generation Button ---
        self.generate_button = tk.Button(master, text="Generate My 1-Week Plan!", command=self.generate_and_display_plan,
                                         font=("Arial", 14, "bold"), bg="#2196f3", fg="white",
                                         activebackground="#42a5f5", activeforeground="white",
                                         relief="raised", bd=5, cursor="hand2")
        self.generate_button.pack(pady=20)

        # --- Study Plan Output Section ---
        self.plan_frame = tk.Frame(master, bg="#e0f2f7", padx=15, pady=15, bd=2, relief="sunken")
        self.plan_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.plan_label = tk.Label(self.plan_frame, text="Your 1-Week Study Master Plan:",
                                   font=("Arial", 16, "bold"), fg="#004d40", bg="#e0f2f7")
        self.plan_label.pack(pady=5)

        self.plan_display = scrolledtext.ScrolledText(self.plan_frame, wrap=tk.WORD, font=("Consolas", 11),
                                                      bg="#ffffff", fg="#333333", bd=2, relief="solid",
                                                      padx=10, pady=10, state="disabled")
        self.plan_display.pack(fill="both", expand=True)

        self.update_subjects_display() # Initial update

    def add_subject_from_entry(self, event=None):
        self.add_subject()

    def add_subject(self):
        subject = self.subject_entry.get().strip()
        if subject:
            if subject.capitalize() not in self.subjects:
                self.subjects.append(subject.capitalize())
                self.subject_entry.delete(0, tk.END)
                self.update_subjects_display()
            else:
                messagebox.showwarning("Duplicate Subject", f"'{subject.capitalize()}' is already in your list.")
        else:
            messagebox.showwarning("Empty Subject", "Please enter a subject name.")

    def clear_subjects(self):
        if messagebox.askyesno("Clear Subjects", "Are you sure you want to clear all subjects?"):
            self.subjects = []
            self.update_subjects_display()
            self.plan_display.config(state="normal")
            self.plan_display.delete(1.0, tk.END)
            self.plan_display.config(state="disabled")

    def update_subjects_display(self):
        self.subjects_display.config(state="normal")
        self.subjects_display.delete(1.0, tk.END)
        if self.subjects:
            for i, subject in enumerate(self.subjects):
                self.subjects_display.insert(tk.END, f"• {subject}\n")
        else:
            self.subjects_display.insert(tk.END, "No subjects added yet.")
        self.subjects_display.config(state="disabled")

    def generate_study_plan(self):
        """
        Generates a 1-week study plan including subjects, math, and playtime.
        """
        if not self.subjects:
            messagebox.showerror("No Subjects", "Please add at least one subject before generating the plan.")
            return None

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        plan = {}
        subject_index = 0

        # Create a copy of subjects to shuffle for better distribution
        shuffled_subjects = self.subjects[:]
        random.shuffle(shuffled_subjects)

        for day in days_of_week:
            daily_plan = []

            # Always include Mathematics
            daily_plan.append("🧠 Mathematics (1.5 hours)")

            # Distribute other subjects
            # Aim for 2-3 subjects per day if possible, cycling through them
            num_subjects_today = random.randint(2, min(3, len(shuffled_subjects)))
            for _ in range(num_subjects_today):
                if subject_index >= len(shuffled_subjects):
                    subject_index = 0 # Loop back to the start if all subjects have been covered
                    random.shuffle(shuffled_subjects) # Reshuffle for variety
                daily_plan.append(f"📖 {shuffled_subjects[subject_index]} (1.5-2 hours)")
                subject_index += 1

            # Always include Playtime
            daily_plan.append("🎮 Playtime / Break (1 hour)")

            # Add a little extra flexibility for the weekend
            if day in ["Saturday", "Sunday"]:
                daily_plan.append("🧘 Free Study / Hobby Time (flexible)")

            plan[day] = daily_plan
        return plan

    def generate_and_display_plan(self):
        self.plan_display.config(state="normal")
        self.plan_display.delete(1.0, tk.END)
        self.plan_display.insert(tk.END, "⏳ Generating your personalized study plan...\n\n")
        self.plan_display.config(state="disabled")
        self.master.update_idletasks() # Update GUI to show loading message

        # Simulate a small delay for user experience
        time.sleep(1)

        study_plan = self.generate_study_plan()
        if study_plan:
            self.plan_display.config(state="normal")
            self.plan_display.delete(1.0, tk.END) # Clear loading message

            self.plan_display.insert(tk.END, "✨ Your 1-Week Study Master Plan! ✨\n")
            self.plan_display.insert(tk.END, "------------------------------------\n\n")

            for day, activities in study_plan.items():
                self.plan_display.insert(tk.END, f"🗓️ {day}:\n")
                for activity in activities:
                    self.plan_display.insert(tk.END, f"  - {activity}\n")
                self.plan_display.insert(tk.END, "-" * 20 + "\n\n")

            self.plan_display.insert(tk.END, "Good luck with your studies! Remember to stay consistent and take breaks! 🚀\n")
            self.plan_display.insert(tk.END, "------------------------------------\n")
            self.plan_display.config(state="disabled")
        else:
            # If generate_study_plan returned None (due to no subjects),
            # the messagebox already handled the error. Just clear any loading text.
            self.plan_display.config(state="normal")
            self.plan_display.delete(1.0, tk.END)
            self.plan_display.config(state="disabled")


def main():
    root = tk.Tk()
    app = StudyAgentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()