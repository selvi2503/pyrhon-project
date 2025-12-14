import tkinter as tk
from tkinter import messagebox
import random
import string

class HackerSimulationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("HACKER SIMULATION")
        self.root.geometry("900x1100")
        self.root.configure(bg='#0a0a0a')
        
        self.target_account = ""
        self.attempts = 8
        self.max_attempts = 8
        self.unlocked_hints = []
        self.game_state = "playing"
        
        # Character lists for random selection
        self.letters = list(string.ascii_uppercase)
        self.digits = list(string.digits)
        
        # Words to pick letters from
        self.hint_words = {
            0: ("APPLE", ['A', 'P', 'L', 'E']),
            1: ("PYTHON", ['P', 'Y', 'T', 'H', 'O', 'N']),
            2: ("BANANA", ['B', 'A', 'N']),
            3: ("COMPUTER", ['C', 'O', 'M', 'P', 'U', 'T', 'E', 'R']),
            4: ("DIGITAL", ['D', 'I', 'G', 'T', 'A', 'L']),
        }
        
        self.hints = []
        self.hint_chars = {}  # Store the random characters for hints
        
        self.setup_ui()
        self.generate_account()
        
    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg='#0a0a0a')
        header_frame.pack(pady=15)
        
        title_label = tk.Label(
            header_frame,
            text="=== HACKER SIMULATION ===",
            font=('Courier', 26, 'bold'),
            bg='#0a0a0a',
            fg='#00ff00'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="[ Breach the Security System ]",
            font=('Courier', 11),
            bg='#0a0a0a',
            fg='#00cc00'
        )
        subtitle_label.pack(pady=5)
        
        self.char_frame = tk.Frame(self.root, bg='#000000', highlightbackground='#00ff00', highlightthickness=3)
        self.char_frame.pack(pady=15, padx=40, fill='both')
        
        self.char_label = tk.Label(
            self.char_frame,
            text="[HACKER]",
            font=('Courier', 36, 'bold'),
            bg='#000000',
            fg='#00ff00'
        )
        self.char_label.pack(pady=35)
        
        self.char_status = tk.Label(
            self.char_frame,
            text=">> Initializing attack...",
            font=('Courier', 11),
            bg='#000000',
            fg='#00ff88'
        )
        self.char_status.pack(pady=10)
        
        self.game_frame = tk.Frame(self.root, bg='#1a1a1a', highlightbackground='#00ff00', highlightthickness=2)
        self.game_frame.pack(pady=15, padx=40, fill='both', expand=True)
        
        status_frame = tk.Frame(self.game_frame, bg='#1a1a1a')
        status_frame.pack(pady=10, padx=10, fill='x')
        
        self.status_label = tk.Label(
            status_frame,
            text="[TARGET: ENCRYPTED]",
            font=('Courier', 11, 'bold'),
            bg='#1a1a1a',
            fg='#ff0000'
        )
        self.status_label.pack(side='left')
        
        self.attempts_label = tk.Label(
            status_frame,
            text=f"[ATTEMPTS: {self.max_attempts}/{self.max_attempts}]",
            font=('Courier', 11, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        self.attempts_label.pack(side='right')
        
        hint_frame = tk.Frame(self.game_frame, bg='#000000', highlightbackground='#ffaa00', highlightthickness=2)
        hint_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        hint_title = tk.Label(
            hint_frame,
            text="[ INTELLIGENCE DATABASE ]",
            font=('Courier', 13, 'bold'),
            bg='#000000',
            fg='#ffaa00'
        )
        hint_title.pack(pady=8)
        
        self.hint_labels = []
        for i in range(6):
            hint_label = tk.Label(
                hint_frame,
                text="[LOCKED] ??? - Complete attempts to unlock",
                font=('Courier', 9),
                bg='#1a1a1a',
                fg='#555555',
                anchor='w',
                padx=15,
                pady=8,
                wraplength=700,
                justify='left'
            )
            hint_label.pack(pady=3, padx=10, fill='x')
            self.hint_labels.append(hint_label)
        
        input_frame = tk.Frame(self.game_frame, bg='#1a1a1a')
        input_frame.pack(pady=12, padx=10, fill='x')
        
        input_label = tk.Label(
            input_frame,
            text=">> ENTER TARGET ACCOUNT:",
            font=('Courier', 10, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        input_label.pack(anchor='w', pady=3)
        
        self.entry = tk.Entry(
            input_frame,
            font=('Courier', 18, 'bold'),
            bg='#000000',
            fg='#00ff00',
            insertbackground='#00ff00',
            highlightbackground='#00ff00',
            highlightthickness=2,
            justify='center'
        )
        self.entry.pack(pady=5, fill='x', ipady=8)
        self.entry.bind('<Return>', lambda e: self.handle_guess())
        self.entry.bind('<KeyRelease>', self.limit_input)
        
        self.message_label = tk.Label(
            input_frame,
            text="",
            font=('Courier', 10, 'bold'),
            bg='#1a1a1a',
            fg='#ff0000'
        )
        self.message_label.pack(pady=5)
        
        button_frame = tk.Frame(self.game_frame, bg='#1a1a1a')
        button_frame.pack(pady=12, padx=10, fill='x')
        
        self.hack_button = tk.Button(
            button_frame,
            text="[ ATTEMPT BREACH ]",
            font=('Courier', 11, 'bold'),
            bg='#00aa00',
            fg='white',
            command=self.handle_guess,
            cursor='hand2',
            relief='raised',
            bd=4,
            activebackground='#00ff00'
        )
        self.hack_button.pack(side='left', expand=True, fill='x', padx=5, ipady=5)
        
        self.reset_button = tk.Button(
            button_frame,
            text="[ NEW TARGET ]",
            font=('Courier', 11, 'bold'),
            bg='#555555',
            fg='white',
            command=self.reset_game,
            cursor='hand2',
            relief='raised',
            bd=4,
            activebackground='#777777'
        )
        self.reset_button.pack(side='right', expand=True, fill='x', padx=5, ipady=5)
        
    def limit_input(self, event):
        text = self.entry.get().upper()
        filtered = ''.join(c for c in text if c.isalnum())
        if len(filtered) > 6:
            filtered = filtered[:6]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, filtered)
        
    def generate_account(self):
        """Generate a random 6-character account and create hints"""
        # Generate random characters for each position
        char1 = random.choice(self.letters)
        char2 = random.choice(self.digits)
        char3 = random.choice(self.letters)
        char4 = random.choice(self.digits)
        char5 = random.choice(self.letters)
        char6 = random.choice(self.digits)
        
        self.target_account = char1 + char2 + char3 + char4 + char5 + char6
        
        # Store hint characters
        self.hint_chars = {
            0: char1,
            1: char2,
            2: char3,
            3: char4,
            4: char5,
            5: char6
        }
        
        # Create hints
        self.hints = [
            f"Hint 1: The 1st character is the letter '{char1}'",
            f"Hint 2: The 2nd character is the digit '{char2}'",
            f"Hint 3: The 3rd character is a letter from 'APPLE' → {char3}",
            f"Hint 4: The 4th character is a random digit → '{char4}'",
            f"Hint 5: The 5th character is a letter from 'PYTHON' → {char5}",
            f"Hint 6: The 6th character is the digit '{char6}'"
        ]
        
        print("=" * 50)
        print("DEBUG MODE - Target Account: " + self.target_account)
        print("=" * 50)
        
        self.animate_hacker()
        
    def animate_hacker(self):
        if self.game_state == "playing":
            current_text = self.char_status.cget("text")
            if "Initializing" in current_text:
                self.char_status.config(text=">> Scanning networks...")
            elif "Scanning" in current_text:
                self.char_status.config(text=">> Cracking encryption...")
            else:
                self.char_status.config(text=">> Initializing attack...")
            self.root.after(1500, self.animate_hacker)
            
    def unlock_hint(self, hint_index):
        if hint_index < len(self.hints) and hint_index not in self.unlocked_hints:
            self.unlocked_hints.append(hint_index)
            self.hint_labels[hint_index].config(
                text="[UNLOCKED] " + self.hints[hint_index],
                bg='#002200',
                fg='#00ff88'
            )
            
    def handle_guess(self):
        if self.game_state != "playing":
            return
            
        guess = self.entry.get().upper().strip()
        
        if len(guess) == 0:
            self.message_label.config(text=">> ERROR: Enter an account number!", fg='#ff6600')
            return
            
        if len(guess) != 6:
            self.message_label.config(text=">> ERROR: Account must be exactly 6 characters!", fg='#ff6600')
            return
        
        if guess == self.target_account:
            self.game_state = "success"
            self.char_label.config(text="[SUCCESS!]", fg='#00ff00')
            self.char_status.config(text=">> ACCESS GRANTED!")
            self.message_label.config(text=">> BREACH SUCCESSFUL! ACCOUNT COMPROMISED!", fg='#00ff00')
            self.hack_button.config(state='disabled', bg='#333333')
            self.entry.config(state='disabled')
            messagebox.showinfo("BREACH SUCCESSFUL!", "ACCESS GRANTED!\n\nYou successfully hacked the account!\n\nAccount: " + self.target_account)
        else:
            self.attempts -= 1
            self.attempts_label.config(text=f"[ATTEMPTS: {self.attempts}/{self.max_attempts}]")
            
            attempts_used = self.max_attempts - self.attempts
            if attempts_used <= len(self.hints):
                self.unlock_hint(attempts_used - 1)
            
            if self.attempts == 0:
                self.game_state = "failed"
                self.char_label.config(text="[DETECTED!]", fg='#ff0000')
                self.char_status.config(text=">> SECURITY BREACH DETECTED!")
                self.message_label.config(text=">> FAILED! AUTHORITIES ALERTED!", fg='#ff0000')
                self.hack_button.config(state='disabled', bg='#333333')
                self.entry.config(state='disabled')
                self.status_label.config(text="[SYSTEM LOCKED]", fg='#ff0000')
                
                self.root.after(2000, self.show_arrest)
            else:
                self.message_label.config(text=f">> WRONG! {self.attempts} attempts remaining. New hint unlocked!", fg='#ff4444')
        
        self.entry.delete(0, tk.END)
        
    def show_arrest(self):
        self.game_state = "arrested"
        self.char_label.config(text="[ARRESTED!]", fg='#ff0000')
        self.char_status.config(text=">> Taking you into custody...")
        
        messagebox.showinfo(
            "MISSION FAILED!",
            "FAILED TO COMPLETE THE TASK!\n\n" +
            "The authorities have been notified.\n" +
            "You are being taken into custody.\n\n" +
            "The correct account was: " + self.target_account + "\n\n" +
            "[GAME OVER]\n\n" +
            "Click OK to try again!"
        )
        self.reset_game()
        
    def reset_game(self):
        self.game_state = "playing"
        self.attempts = self.max_attempts
        self.unlocked_hints = []
        
        self.char_label.config(text="[HACKER]", fg='#00ff00')
        self.char_status.config(text=">> Initializing attack...")
        self.attempts_label.config(text=f"[ATTEMPTS: {self.max_attempts}/{self.max_attempts}]")
        self.status_label.config(text="[TARGET: ENCRYPTED]", fg='#ff0000')
        self.message_label.config(text="")
        self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.hack_button.config(state='normal', bg='#00aa00')
        
        for i in range(6):
            self.hint_labels[i].config(
                text="[LOCKED] ??? - Complete attempts to unlock",
                bg='#1a1a1a',
                fg='#555555'
            )
        
        self.generate_account()

if __name__ == "__main__":
    root = tk.Tk()
    game = HackerSimulationGame(root)
    root.mainloop()