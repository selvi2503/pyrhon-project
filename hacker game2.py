import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import string

class HackerSimulationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("HACKER SIMULATION")
        self.root.geometry("1200x950")
        self.root.configure(bg='#0a0a0a')
        
        self.target_account = ""
        self.attempts = 6
        self.unlocked_hints = [0]
        self.game_state = "playing"
        self.hints = []
        self.chat_history = []
        
        self.setup_ui()
        self.generate_account()
        self.display_initial_hint()
        self.animate_hacker()
        self.add_welcome_message()
        
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#0a0a0a')
        main_container.pack(fill='both', expand=True)
        
        # Left side - Game
        game_container = tk.Frame(main_container, bg='#0a0a0a')
        game_container.pack(side='left', fill='both', expand=True, padx=(10, 5))
        
        # Right side - Chat Assistant
        chat_container = tk.Frame(main_container, bg='#0a0a0a')
        chat_container.pack(side='right', fill='both', expand=True, padx=(5, 10))
        
        # === GAME SIDE ===
        header_frame = tk.Frame(game_container, bg='#0a0a0a')
        header_frame.pack(pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="HACKER SIMULATION",
            font=('Courier', 22, 'bold'),
            bg='#0a0a0a',
            fg='#00ff00'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="[ Breach the Security System ]",
            font=('Courier', 9),
            bg='#0a0a0a',
            fg='#00cc00'
        )
        subtitle_label.pack(pady=3)
        
        self.char_frame = tk.Frame(game_container, bg='#000000', highlightbackground='#00ff00', highlightthickness=3)
        self.char_frame.pack(pady=10, padx=10, fill='both')
        
        self.char_label = tk.Label(
            self.char_frame,
            text="[HACKER]",
            font=('Courier', 28, 'bold'),
            bg='#000000',
            fg='#00ff00'
        )
        self.char_label.pack(pady=20)
        
        self.char_status = tk.Label(
            self.char_frame,
            text=">> Initializing attack...",
            font=('Courier', 9),
            bg='#000000',
            fg='#00ff88'
        )
        self.char_status.pack(pady=8)
        
        self.game_frame = tk.Frame(game_container, bg='#1a1a1a', highlightbackground='#00ff00', highlightthickness=2)
        self.game_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        status_frame = tk.Frame(self.game_frame, bg='#1a1a1a')
        status_frame.pack(pady=8, padx=8, fill='x')
        
        self.status_label = tk.Label(
            status_frame,
            text="[TARGET: ENCRYPTED]",
            font=('Courier', 9, 'bold'),
            bg='#1a1a1a',
            fg='#ff0000'
        )
        self.status_label.pack(side='left')
        
        self.attempts_label = tk.Label(
            status_frame,
            text="[ATTEMPTS: 6/6]",
            font=('Courier', 9, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        self.attempts_label.pack(side='right')
        
        hint_frame = tk.Frame(self.game_frame, bg='#000000', highlightbackground='#ffaa00', highlightthickness=2)
        hint_frame.pack(pady=8, padx=8, fill='both', expand=True)
        
        hint_title = tk.Label(
            hint_frame,
            text="[ INTELLIGENCE DATABASE ]",
            font=('Courier', 11, 'bold'),
            bg='#000000',
            fg='#ffaa00'
        )
        hint_title.pack(pady=5)
        
        self.hint_labels = []
        for i in range(6):
            hint_label = tk.Label(
                hint_frame,
                text="[LOCKED] ??? - Complete attempts to unlock",
                font=('Courier', 8),
                bg='#1a1a1a',
                fg='#555555',
                anchor='w',
                padx=10,
                pady=6,
                wraplength=450
            )
            hint_label.pack(pady=2, padx=8, fill='x')
            self.hint_labels.append(hint_label)
        
        input_frame = tk.Frame(self.game_frame, bg='#1a1a1a')
        input_frame.pack(pady=8, padx=8, fill='x')
        
        input_label = tk.Label(
            input_frame,
            text=">> ENTER TARGET ACCOUNT:",
            font=('Courier', 9, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        input_label.pack(anchor='w', pady=2)
        
        self.entry = tk.Entry(
            input_frame,
            font=('Courier', 16, 'bold'),
            bg='#000000',
            fg='#00ff00',
            insertbackground='#00ff00',
            highlightbackground='#00ff00',
            highlightthickness=2,
            justify='center'
        )
        self.entry.pack(pady=5, fill='x', ipady=6)
        self.entry.bind('<Return>', lambda e: self.handle_guess())
        self.entry.bind('<KeyRelease>', self.limit_input)
        
        self.message_label = tk.Label(
            input_frame,
            text="",
            font=('Courier', 9, 'bold'),
            bg='#1a1a1a',
            fg='#ff0000'
        )
        self.message_label.pack(pady=4)
        
        button_frame = tk.Frame(self.game_frame, bg='#1a1a1a')
        button_frame.pack(pady=8, padx=8, fill='x')
        
        self.hack_button = tk.Button(
            button_frame,
            text="[ ATTEMPT BREACH ]",
            font=('Courier', 10, 'bold'),
            bg='#00aa00',
            fg='white',
            command=self.handle_guess,
            cursor='hand2',
            relief='raised',
            bd=3,
            activebackground='#00ff00'
        )
        self.hack_button.pack(side='left', expand=True, fill='x', padx=3, ipady=4)
        
        self.reset_button = tk.Button(
            button_frame,
            text="[ NEW TARGET ]",
            font=('Courier', 10, 'bold'),
            bg='#555555',
            fg='white',
            command=self.reset_game,
            cursor='hand2',
            relief='raised',
            bd=3,
            activebackground='#777777'
        )
        self.reset_button.pack(side='right', expand=True, fill='x', padx=3, ipady=4)
        
        # === CHAT ASSISTANT SIDE ===
        chat_header = tk.Frame(chat_container, bg='#0a0a0a')
        chat_header.pack(pady=10)
        
        chat_title = tk.Label(
            chat_header,
            text="AI ASSISTANT",
            font=('Courier', 22, 'bold'),
            bg='#0a0a0a',
            fg='#00aaff'
        )
        chat_title.pack()
        
        chat_subtitle = tk.Label(
            chat_header,
            text="[ Ask me anything about hints or CTF concepts ]",
            font=('Courier', 9),
            bg='#0a0a0a',
            fg='#0088cc'
        )
        chat_subtitle.pack(pady=3)
        
        # Chat display area
        chat_frame = tk.Frame(chat_container, bg='#1a1a1a', highlightbackground='#00aaff', highlightthickness=2)
        chat_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            font=('Courier', 9),
            bg='#000000',
            fg='#00ff88',
            insertbackground='#00aaff',
            wrap=tk.WORD,
            state='disabled',
            highlightthickness=0
        )
        self.chat_display.pack(pady=8, padx=8, fill='both', expand=True)
        
        # Configure tags for different message types
        self.chat_display.tag_config('user', foreground='#00aaff')
        self.chat_display.tag_config('assistant', foreground='#00ff88')
        self.chat_display.tag_config('system', foreground='#ffaa00')
        
        # Chat input area
        chat_input_frame = tk.Frame(chat_container, bg='#1a1a1a', highlightbackground='#00aaff', highlightthickness=2)
        chat_input_frame.pack(pady=(0, 10), padx=10, fill='x')
        
        chat_input_label = tk.Label(
            chat_input_frame,
            text=">> YOUR QUESTION:",
            font=('Courier', 9, 'bold'),
            bg='#1a1a1a',
            fg='#00aaff'
        )
        chat_input_label.pack(anchor='w', padx=8, pady=(8, 2))
        
        self.chat_entry = tk.Entry(
            chat_input_frame,
            font=('Courier', 10),
            bg='#000000',
            fg='#00aaff',
            insertbackground='#00aaff',
            highlightbackground='#00aaff',
            highlightthickness=2
        )
        self.chat_entry.pack(pady=5, padx=8, fill='x', ipady=4)
        self.chat_entry.bind('<Return>', lambda e: self.handle_chat())
        
        chat_button = tk.Button(
            chat_input_frame,
            text="[ SEND ]",
            font=('Courier', 10, 'bold'),
            bg='#0088cc',
            fg='white',
            command=self.handle_chat,
            cursor='hand2',
            relief='raised',
            bd=3,
            activebackground='#00aaff'
        )
        chat_button.pack(pady=(0, 8), padx=8, ipady=3, fill='x')
        
    def add_welcome_message(self):
        welcome = (
            "Welcome to the AI Assistant!\n\n"
            "I can help you understand:\n"
            "- What is MD5 hash?\n"
            "- What is ASCII?\n"
            "- How to interpret hints\n"
            "- CTF concepts and strategies\n"
            "- Any other questions about the game!\n\n"
            "Just type your question below."
        )
        self.add_chat_message("SYSTEM", welcome, 'system')
        
    def add_chat_message(self, sender, message, tag):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"\n[{sender}]\n", tag)
        self.chat_display.insert(tk.END, f"{message}\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        
    def handle_chat(self):
        question = self.chat_entry.get().strip()
        if not question:
            return
            
        self.add_chat_message("YOU", question, 'user')
        self.chat_entry.delete(0, tk.END)
        
        # Generate response based on question
        response = self.generate_ai_response(question.lower())
        self.add_chat_message("AI", response, 'assistant')
        
    def generate_ai_response(self, question):
        # Simple keyword-based responses
        if 'md5' in question or 'hash' in question:
            return (
                "MD5 Hash is a cryptographic function that converts text into a unique "
                "fixed-length string. In this game, I show you the first 4 characters of "
                "a simulated hash to help identify the account. Each account has a unique "
                "hash signature!"
            )
        elif 'ascii' in question:
            return (
                "ASCII (American Standard Code for Information Interchange) assigns numbers "
                "to characters. For example: A=65, B=66, Z=90. The hint shows the ASCII "
                "value to help you identify which letter is in that position."
            )
        elif 'pattern' in question or 'structure' in question:
            return (
                "The account follows this pattern:\n"
                "Position 1: Letter (A-Z)\n"
                "Position 2: Number (0-9)\n"
                "Position 3: Letter or Number\n"
                "Position 4: Always '7'\n"
                "Position 5: Always 'X'\n"
                "Position 6: Letter (A-Z)\n\n"
                "Use other hints to narrow down the unknown positions!"
            )
        elif 'sum' in question or 'digit' in question:
            return (
                "The 'sum of digits' means adding up all the numbers in the account. "
                "For example, if the account is 'A2B7X3', the sum would be 2+7+3=12. "
                "This helps you verify if your guess has the right numbers!"
            )
        elif 'even' in question or 'odd' in question:
            return (
                "Even numbers are divisible by 2 (0,2,4,6,8) and odd numbers are not (1,3,5,7,9). "
                "This hint narrows down position 2 to only 5 possible digits instead of 10!"
            )
        elif 'alphabet' in question or 'after' in question or 'before' in question:
            return (
                "When I say 'comes after X in alphabet', I mean the next letter. "
                "For example, if it says 'comes after K', the answer is 'L'. "
                "The alphabet order is: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
            )
        elif 'hint' in question:
            return (
                "Hints unlock progressively:\n"
                "- Hint 1: Available at start (hash prefix)\n"
                "- Hints 2-6: Unlock after each wrong attempt\n\n"
                "Combine multiple hints to deduce the answer. Each hint gives you "
                "specific information about different positions in the 6-character account."
            )
        elif 'ctf' in question:
            return (
                "CTF (Capture The Flag) is a cybersecurity competition where you solve puzzles "
                "and challenges. This game simulates a CTF challenge where you use cryptographic "
                "clues and logical deduction to crack a code. Real CTFs use similar techniques!"
            )
        elif 'strategy' in question or 'how to win' in question or 'help' in question:
            return (
                "Strategy tips:\n"
                "1. Start with Hint 4 to understand the pattern\n"
                "2. Use Hint 2 to know the exact first character\n"
                "3. Use Hint 5 to narrow position 2 (even/odd)\n"
                "4. Use Hint 6 for the last character\n"
                "5. Use digit sum to verify your guess\n"
                "6. Check position feedback after each attempt!\n\n"
                "Combine all hints strategically!"
            )
        elif 'position' in question or 'correct' in question:
            return (
                "After each wrong guess, I show '[X/6 positions correct]'. This tells you "
                "how many characters in your guess are in the RIGHT position. Use this to "
                "narrow down which parts of your guess are correct!"
            )
        else:
            return (
                "I'm here to help! Try asking about:\n"
                "- MD5 hash or ASCII\n"
                "- How hints work\n"
                "- Game strategy\n"
                "- CTF concepts\n"
                "- Pattern interpretation\n"
                "- Or any specific term you don't understand!"
            )
        
    def limit_input(self, event):
        text = self.entry.get().upper()
        filtered = ''.join(c for c in text if c.isalnum())
        if len(filtered) > 6:
            filtered = filtered[:6]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, filtered)
        
    def generate_account(self):
        letters = string.ascii_uppercase
        numbers = string.digits
        
        first = random.choice(letters)
        second = random.choice(numbers)
        third = random.choice(letters + numbers)
        fourth = '7'
        fifth = 'X'
        sixth = random.choice(letters)
        
        self.target_account = first + second + third + fourth + fifth + sixth
        
        self.hints = [
            f"Hint 1: MD5 hash starts with '{self.get_md5_prefix(self.target_account)}' (first 4 chars)",
            f"Hint 2: Position 1 is '{chr(ord(first) + 0)}' (ASCII: {ord(first)})",
            f"Hint 3: Sum of all digits = {self.sum_digits(self.target_account)}",
            f"Hint 4: The pattern is: [LETTER][DIGIT][?][7][X][LETTER]",
            f"Hint 5: Position 2 is an even number" if int(second) % 2 == 0 else f"Hint 5: Position 2 is an odd number",
            f"Hint 6: Last character comes after '{chr(ord(sixth) - 1)}' in alphabet" if ord(sixth) > ord('A') else f"Hint 6: Last character is 'A'"
        ]
        
        print("=" * 50)
        print("DEBUG MODE - Target Account: " + self.target_account)
        print("=" * 50)
        
    def get_md5_prefix(self, text):
        hash_val = 0
        for char in text:
            hash_val = (hash_val * 31 + ord(char)) % 100000
        return format(hash_val, '05d')[:4]
    
    def sum_digits(self, text):
        total = 0
        for char in text:
            if char.isdigit():
                total += int(char)
        return total
    
    def display_initial_hint(self):
        if len(self.hints) > 0:
            self.hint_labels[0].config(
                text="[UNLOCKED] " + self.hints[0],
                bg='#002200',
                fg='#00ff88'
            )
        
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
            self.add_chat_message("SYSTEM", f"Congratulations! You cracked the code: {self.target_account}", 'system')
            messagebox.showinfo("BREACH SUCCESSFUL!", "ACCESS GRANTED!\n\nYou successfully hacked the account!\n\nAccount: " + self.target_account)
        else:
            self.attempts -= 1
            self.attempts_label.config(text="[ATTEMPTS: " + str(self.attempts) + "/6]")
            
            correct_positions = sum(1 for i in range(min(len(guess), len(self.target_account))) if guess[i] == self.target_account[i])
            closeness_msg = f" [{correct_positions}/6 positions correct]"
            
            attempts_used = 6 - self.attempts
            if attempts_used <= 6:
                self.unlock_hint(attempts_used - 1)
            
            if self.attempts == 0:
                self.game_state = "failed"
                self.char_label.config(text="[DETECTED!]", fg='#ff0000')
                self.char_status.config(text=">> SECURITY BREACH DETECTED!")
                self.message_label.config(text=">> FAILED! AUTHORITIES ALERTED!", fg='#ff0000')
                self.hack_button.config(state='disabled', bg='#333333')
                self.entry.config(state='disabled')
                self.status_label.config(text="[SYSTEM LOCKED]", fg='#ff0000')
                self.add_chat_message("SYSTEM", f"Mission failed! The correct account was: {self.target_account}", 'system')
                
                self.root.after(2000, self.show_arrest)
            else:
                self.message_label.config(text=f">> WRONG! {str(self.attempts)} attempts remaining{closeness_msg}", fg='#ff4444')
        
        self.entry.delete(0, tk.END)
        
    def show_arrest(self):
        self.game_state = "arrested"
        self.char_label.config(text="[ARRESTED!]", fg='#ff0000')
        self.char_status.config(text=">> Taking you into custody...")
        
        messagebox.showerror(
            "MISSION FAILED!",
            "FAILED TO COMPLETE THE TASK!\n\n" +
            "The authorities have been notified.\n" +
            "You are being taken into custody.\n\n" +
            "The correct account was: " + self.target_account + "\n\n" +
            "[GAME OVER]"
        )
        
    def reset_game(self):
        self.game_state = "playing"
        self.attempts = 6
        self.unlocked_hints = [0]
        
        self.char_label.config(text="[HACKER]", fg='#00ff00')
        self.char_status.config(text=">> Initializing attack...")
        self.attempts_label.config(text="[ATTEMPTS: 6/6]")
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
        self.display_initial_hint()
        self.animate_hacker()
        self.add_chat_message("SYSTEM", "New target generated! Good luck!", 'system')

if __name__ == "__main__":
    root = tk.Tk()
    game = HackerSimulationGame(root)
    root.mainloop()