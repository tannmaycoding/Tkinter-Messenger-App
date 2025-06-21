import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, font

# Server details
HOST = 'IPv4 address'
PORT = 12345

# Socket setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Themes
LIGHT_THEME = {
    "bg": "#f2f2f2",
    "fg": "#000000",
    "chat_bg": "#ffffff",
    "entry_bg": "#ffffff",
    "button_bg": "#4CAF50",
    "button_fg": "#ffffff"
}

DARK_THEME = {
    "bg": "#2e2e2e",
    "fg": "#ffffff",
    "chat_bg": "#3e3e3e",
    "entry_bg": "#4a4a4a",
    "button_bg": "#00b894",
    "button_fg": "#ffffff"
}

# GUI Class
class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("🖥️ Real-Time Chat Client")
        self.master.geometry("700x500")
        self.master.resizable(False, False)
        self.dark_mode = tk.BooleanVar(value=False)

        # Set default theme
        self.theme = LIGHT_THEME
        self.set_theme()

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.msg_font = font.Font(family="Consolas", size=11)

        # Header
        self.header = tk.Label(master, text="🔗 Socket Chat Client", font=self.title_font,
                               bg=self.theme["bg"], fg=self.theme["fg"])
        self.header.pack(pady=(10, 5))

        # Dark mode toggle
        self.toggle_btn = tk.Checkbutton(master, text="Dark Mode", variable=self.dark_mode,
                                         command=self.toggle_theme, bg=self.theme["bg"], fg=self.theme["fg"])
        self.toggle_btn.pack()

        # Chat box
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, font=self.msg_font,
                                                   bg=self.theme["chat_bg"], fg=self.theme["fg"],
                                                   state='disabled', width=80, height=20)
        self.chat_area.pack(padx=10, pady=10)

        # Entry field + Send button frame
        self.input_frame = tk.Frame(master, bg=self.theme["bg"])
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.entry = tk.Entry(self.input_frame, width=60, bg=self.theme["entry_bg"], fg=self.theme["fg"],
                              font=self.msg_font, insertbackground=self.theme["fg"])
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.input_frame, text="Send", bg=self.theme["button_bg"],
                                     fg=self.theme["button_fg"], font=self.msg_font, command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        # Ask for nickname and connect
        self.nickname = simpledialog.askstring("Nickname", "Choose your nickname", parent=self.master)
        try:
            client.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server:\n{e}")
            self.master.destroy()
            return

        # Start listening thread
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def set_theme(self):
        self.master.configure(bg=self.theme["bg"])

    def toggle_theme(self):
        self.theme = DARK_THEME if self.dark_mode.get() else LIGHT_THEME
        self.set_theme()
        self.header.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.toggle_btn.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.chat_area.config(bg=self.theme["chat_bg"], fg=self.theme["fg"])
        self.entry.config(bg=self.theme["entry_bg"], fg=self.theme["fg"], insertbackground=self.theme["fg"])
        self.send_button.config(bg=self.theme["button_bg"], fg=self.theme["button_fg"])
        self.input_frame.config(bg=self.theme["bg"])

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "NICKNAME":
                    client.send(self.nickname.encode('utf-8'))
                else:
                    self.display_message(message)
            except:
                break

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            full_msg = f"{self.nickname}: {message}"
            try:
                client.send(full_msg.encode('utf-8'))
                self.entry.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Message sending failed.")
                self.master.destroy()

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
