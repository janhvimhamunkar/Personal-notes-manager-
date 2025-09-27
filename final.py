import tkinter as tk
from tkinter import messagebox
import os

class NotesManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Notes Manager")
        self.root.geometry("800x500")
        self.current_note_file = None  # Track the currently edited note file
        
        # Create notes directory if it doesn't exist
        os.makedirs("notes", exist_ok=True)
        
        # Create frames
        self.editor_frame = tk.Frame(root, padx=10, pady=10)
        self.editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.notes_frame = tk.Frame(root, padx=10, pady=10)
        self.notes_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Title entry
        tk.Label(self.editor_frame, text="Title:").pack(anchor=tk.W)
        self.title_entry = tk.Entry(self.editor_frame, width=40)
        self.title_entry.pack(fill=tk.X, pady=5)
        
        # Content text area
        tk.Label(self.editor_frame, text="Content:").pack(anchor=tk.W)
        self.content_text = tk.Text(self.editor_frame, width=40, height=15)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Button(self.button_frame, text="New Note", command=self.new_note).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Save Note", command=self.save_note).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Delete Note", command=self.delete_note).pack(side=tk.LEFT, padx=5)
        
        # Notes list
        tk.Label(self.notes_frame, text="Saved Notes:").pack(anchor=tk.W)
        self.notes_listbox = tk.Listbox(self.notes_frame, width=30)
        self.notes_listbox.pack(fill=tk.BOTH, expand=True)
        self.notes_listbox.bind('<<ListboxSelect>>', self.load_note)
        
        # Load existing notes
        self.load_notes_list()
    
    def new_note(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.current_note_file = None
    
    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter a title")
            return
        
        # Create safe filename
        filename = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in title)
        filename = filename.replace(' ', '_') + ".txt"
        filepath = os.path.join("notes", filename)
        
        # Check for duplicate title (unless editing the same note)
        if os.path.exists(filepath) and filename != self.current_note_file:
            messagebox.showwarning("Warning", "A note with this title already exists")
            return
        
        # Save note to file
        with open(filepath, 'w') as f:
            f.write(content)
        
        # If we renamed an existing note, delete the old file
        if self.current_note_file and self.current_note_file != filename:
            old_filepath = os.path.join("notes", self.current_note_file)
            if os.path.exists(old_filepath):
                os.remove(old_filepath)
        
        self.current_note_file = filename
        self.load_notes_list()
        messagebox.showinfo("Success", "Note saved successfully")
    
    def delete_note(self):
        if not self.current_note_file:
            messagebox.showwarning("Warning", "No note selected to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete this note?"):
            filepath = os.path.join("notes", self.current_note_file)
            os.remove(filepath)
            self.new_note()
            self.load_notes_list()
            messagebox.showinfo("Success", "Note deleted successfully")
    
    def load_note(self, event):
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        
        # Get filename from listbox selection
        filename = self.notes_listbox.get(selection[0]).replace(' ', '_') + ".txt"
        filepath = os.path.join("notes", filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Extract title from filename
            title = filename.replace('_', ' ').replace('.txt', '')
            
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, content)
            self.current_note_file = filename
    
    def load_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        
        if not os.path.exists("notes"):
            return
        
        for filename in os.listdir("notes"):
            if filename.endswith(".txt"):
                # Display filename without extension and with spaces
                display_name = filename.replace('_', ' ').replace('.txt', '')
                self.notes_listbox.insert(tk.END, display_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesManager(root)
    root.mainloop()