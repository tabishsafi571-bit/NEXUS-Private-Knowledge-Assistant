
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from core.document_loader import load_documents
from core.search_engine import search_documents
from core.ai_engine import generate_answer


class NexusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS | Private Knowledge Assistant")
        self.root.geometry("1000x720")
        self.root.minsize(760, 560)

        self.documents = []
        self.folder = tk.StringVar()
        self.status = tk.StringVar(value="Choose a folder to begin.")

        self.build_ui()

    def build_ui(self):
        self.root.configure(bg="#101827")

        header = tk.Frame(self.root, bg="#101827", padx=22, pady=18)
        header.pack(fill="x")

        tk.Label(
            header, text="NEXUS", font=("Segoe UI", 25, "bold"),
            fg="#7dd3fc", bg="#101827"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="PRIVATE KNOWLEDGE ASSISTANT  |  YOUR FILES, YOUR SEARCH",
            font=("Segoe UI", 9), fg="#cbd5e1", bg="#101827"
        ).pack(anchor="w", pady=(3, 0))

        controls = tk.Frame(self.root, bg="#172235", padx=16, pady=14)
        controls.pack(fill="x", padx=18, pady=(0, 12))

        tk.Button(
            controls, text="Choose Folder", command=self.choose_folder,
            bg="#0284c7", fg="white", relief="flat", padx=14, pady=7
        ).pack(side="left")

        tk.Label(
            controls, textvariable=self.folder, bg="#172235",
            fg="#e2e8f0", anchor="w", wraplength=650
        ).pack(side="left", padx=12, fill="x", expand=True)

        tk.Label(
            self.root, text="Ask a question about your documents",
            font=("Segoe UI", 12, "bold"), bg="#101827", fg="white"
        ).pack(anchor="w", padx=20, pady=(4, 8))

        query_row = tk.Frame(self.root, bg="#101827")
        query_row.pack(fill="x", padx=18)

        self.question = tk.StringVar()
        self.question_entry = tk.Entry(
            query_row, textvariable=self.question, font=("Segoe UI", 12),
            bg="#f8fafc", fg="#0f172a", relief="flat"
        )
        self.question_entry.pack(side="left", fill="x", expand=True, ipady=10)
        self.question_entry.bind("<Return>", lambda event: self.ask())

        tk.Button(
            query_row, text="Ask NEXUS", command=self.ask,
            bg="#0f766e", fg="white", relief="flat", padx=18, pady=9
        ).pack(side="left", padx=(8, 0))

        tk.Label(
            self.root, text="Answer and matching source excerpts",
            font=("Segoe UI", 11, "bold"), bg="#101827", fg="white"
        ).pack(anchor="w", padx=20, pady=(16, 7))

        output_frame = tk.Frame(self.root, bg="#101827")
        output_frame.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        self.output = tk.Text(
            output_frame, wrap="word", font=("Consolas", 10),
            bg="#172235", fg="#e2e8f0", insertbackground="white",
            relief="flat", padx=14, pady=12
        )
        scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=self.output.yview
        )
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.output.insert(
            "1.0",
            "Welcome to NEXUS.\n\n"
            "1. Choose a folder containing .txt or .md files.\n"
            "2. Type a question about your notes.\n"
            "3. Review the answer and its source excerpts.\n\n"
            "Your documents are searched locally by this application."
        )
        self.output.configure(state="disabled")

        tk.Label(
            self.root, textvariable=self.status, bg="#0b1220",
            fg="#93c5fd", anchor="w", padx=18, pady=9
        ).pack(fill="x", side="bottom")

    def show_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def choose_folder(self):
        folder = filedialog.askdirectory(title="Select your notes folder")
        if not folder:
            return

        try:
            documents, skipped = load_documents(folder)
        except (ValueError, OSError) as error:
            messagebox.showerror("Folder Error", str(error))
            return

        self.folder.set(folder)
        self.documents = documents
        self.status.set(
            f"Indexed {len(documents)} documents locally. "
            f"Skipped: {skipped}"
        )

        if not documents:
            self.show_output(
                "No readable .txt or .md files were found.\n\n"
                "Add a text file or Markdown file to this folder, "
                "then choose the folder again."
            )
        else:
            self.show_output(
                f"Folder loaded successfully.\n\n"
                f"Documents indexed: {len(documents)}\n"
                f"Skipped files: {skipped}\n\n"
                "Type a question above to search your notes."
            )

    def ask(self):
        question = self.question.get().strip()

        if not question:
            messagebox.showinfo("NEXUS", "Please enter a question.")
            return

        if not self.documents:
            messagebox.showinfo(
                "NEXUS", "Choose a folder containing TXT or MD files first."
            )
            return

        self.status.set("Searching your documents...")
        self.root.update_idletasks()

        try:
            results = search_documents(question, self.documents)
            answer, mode = generate_answer(question, results)

            output = (
                f"QUESTION\n{question}\n\n"
                f"MODE: {mode}\n\n"
                f"ANSWER / SEARCH RESULTS\n{answer}\n\n"
                "MATCHING SOURCES\n"
            )

            if results:
                for index, item in enumerate(results, start=1):
                    output += (
                        f"\n{index}. {item['name']}\n"
                        f"Path: {item['path']}\n"
                        f"Match score: {item['score']}\n"
                        f"{item['excerpt']}\n"
                    )
            else:
                output += "No matching sources found.\n"

            self.show_output(output)
            self.status.set(
                f"Search complete. {len(results)} matching source(s)."
            )

        except Exception as error:
            messagebox.showerror("NEXUS Error", str(error))
            self.status.set("An error occurred. Check the error message.")


def run_app():
    root = tk.Tk()
    NexusApp(root)
    root.mainloop()
