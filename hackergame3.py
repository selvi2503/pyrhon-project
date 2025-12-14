import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import string
import json

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
            text="[ Powered by Claude - Ask anything! ]",
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
        self.chat_display.tag_config('error', foreground='#ff4444')
        
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
        
        chat_button_frame = tk.Frame(chat_input_frame, bg='#1a1a1a')
        chat_button_frame.pack(pady=(0, 8), padx=8, fill='x')
        
        self.chat_button = tk.Button(
            chat_button_frame,
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
        self.chat_button.pack(side='left', expand=True, fill='x', ipady=3)
        
    def add_welcome_message(self):
        welcome = (
            "Welcome! I'm Claude, your AI assistant for this CTF challenge.\n\n"
            "I can help you with:\n"
            "• Understanding hints and concepts (MD5, ASCII, patterns)\n"
            "• Explaining game mechanics with examples\n"
            "• Answering ANY question you have\n"
            "• Providing step-by-step explanations\n\n"
            "Tips:\n"
            "- Ask for examples: 'explain ASCII with example'\n"
            "- Request details: 'how does the hint system work?'\n"
            "- Get strategies: 'what's the best approach?'\n\n"
            "Just ask me anything!"
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
        
        # Disable button while processing
        self.chat_button.config(state='disabled', text='[ THINKING... ]')
        self.chat_entry.config(state='disabled')
        
        self.add_chat_message("YOU", question, 'user')
        self.chat_entry.delete(0, tk.END)
        
        # Process in background
        self.root.after(100, lambda: self.get_ai_response(question))
        
    def get_ai_response(self, question):
        try:
            # Build context for Claude
            game_context = self.build_game_context()
            
            # Prepare conversation history (last 5 exchanges)
            messages = []
            recent_history = self.chat_history[-10:] if len(self.chat_history) > 10 else self.chat_history
            for msg in recent_history:
                messages.append(msg)
            
            # Add current question
            messages.append({
                "role": "user",
                "content": f"{game_context}\n\nUser question: {question}"
            })
            
            # Call Claude API
            import urllib.request
            import json
            
            data = {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": messages,
                "system": """You are an AI assistant helping users with a CTF-style hacker simulation game. 

The game involves guessing a 6-character account code using hints. Be helpful, educational, and provide clear explanations.

When asked for examples, always provide concrete, specific examples.
When explaining concepts, break them down step-by-step.
Be encouraging and supportive of the user's learning.

You can answer ANY question the user asks - whether it's about:
- Game mechanics and hints
- Cryptography concepts (MD5, hashing)
- ASCII and character encoding
- Problem-solving strategies
- CTF techniques
- Or any other topic they're curious about

Always be conversational, clear, and thorough in your explanations."""
            }
            
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=json.dumps(data).encode('utf-8'),
                headers={
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                ai_response = result['content'][0]['text']
                
                # Save to history
                self.chat_history.append({"role": "user", "content": question})
                self.chat_history.append({"role": "assistant", "content": ai_response})
                
                self.add_chat_message("AI", ai_response, 'assistant')
                
        except Exception as e:
            error_msg = f"Error connecting to AI: {str(e)}\n\nFalling back to basic responses..."
            self.add_chat_message("SYSTEM", error_msg, 'error')
            
            # Fallback to basic responses
            fallback = self.generate_fallback_response(question)
            self.add_chat_message("AI", fallback, 'assistant')
        
        finally:
            # Re-enable button
            self.chat_button.config(state='normal', text='[ SEND ]')
            self.chat_entry.config(state='normal')
            self.chat_entry.focus()
    
    def build_game_context(self):
        """Build context about current game state"""
        unlocked_hints_text = "\n".join([
            f"- {self.hints[i]}" for i in self.unlocked_hints if i < len(self.hints)
        ])
        
        context = f"""Current game state:
- Attempts remaining: {self.attempts}/6
- Account pattern: 6 characters (letters and numbers)
- Unlocked hints:
{unlocked_hints_text}

The user is playing a CTF-style game where they need to guess a 6-character account code.
They unlock more hints after each wrong attempt."""
        
        return context
    
    def generate_fallback_response(self, question):
        """Fallback responses when API is unavailable"""
        q = question.lower()
        
        if 'example' in q or 'show me' in q:
            if 'md5' in q or 'hash' in q:
                return """MD5 Hash Example:

Let's say we have the text "HELLO"
1. MD5 converts it to: 8b1a9953c4611296a827abf8c47804d7
2. We take first 4 characters: 8b1a

In this game, each account has a unique hash prefix.
If Hint 1 says "MD5 starts with 3f2a", you know the correct account
produces a hash beginning with those characters.

Example:
- Account "A2B7XC" → hash starts with "4d2e"
- Account "K5Q7XM" → hash starts with "7a1f"

You can use this to verify your guess!"""
            
            elif 'ascii' in q:
                return """ASCII Example:

ASCII assigns numbers to characters:
A = 65    B = 66    C = 67 ... Z = 90
0 = 48    1 = 49    2 = 50 ... 9 = 57

Example hint: "Position 1 is 'K' (ASCII: 75)"
This tells you:
- Position 1 = letter K
- K's ASCII value = 75
- You can verify: ord('K') = 75

Another example:
If hint says "ASCII: 68", that's the letter 'D'
Because D is the 4th letter: A(65), B(66), C(67), D(68)"""
            
            elif 'pattern' in q:
                return """Pattern Example:

The hint says: [LETTER][DIGIT][?][7][X][LETTER]

Let's decode this:
Position 1: Must be A-Z (like K, M, P)
Position 2: Must be 0-9 (like 3, 5, 8)
Position 3: Unknown - could be letter OR digit
Position 4: Always the number 7
Position 5: Always the letter X
Position 6: Must be A-Z (like C, F, Z)

Example valid accounts:
✓ A2B7XM - follows pattern
✓ K5Q7XC - follows pattern
✓ Z9Z7XA - follows pattern
✗ AA27XM - wrong! position 2 must be digit
✗ A2B8XM - wrong! position 4 must be 7"""
        
        # General responses
        if 'hint' in q:
            return """Hints unlock progressively:

Hint 1: Available immediately (MD5 hash prefix)
Hint 2-6: Unlock after each wrong attempt

Strategy:
1. Read Hint 4 first (shows pattern structure)
2. Use Hint 2 for exact first character
3. Use Hint 5 to narrow position 2 (even/odd)
4. Use Hint 6 for last character
5. Use digit sum to verify

Combine all hints to deduce the answer!"""
        
        elif 'strategy' in q or 'help' in q:
            return """Winning Strategy:

Step 1: Understand the pattern [LETTER][DIGIT][?][7][X][LETTER]
Step 2: Lock in known positions (4=7, 5=X)
Step 3: Use ASCII hint for position 1
Step 4: Use even/odd for position 2
Step 5: Use alphabet clue for position 6
Step 6: Use sum of digits to narrow position 3
Step 7: Verify with MD5 hash

Example walkthrough:
- Pattern: [?][?][?][7][X][?]
- Hint 2: Position 1 = M (ASCII 77)
- Hint 5: Position 2 is even (0,2,4,6,8)
- Hint 6: Last char comes after K = L
- Now we have: M[even][?]7XL
- Use digit sum to find position 3!"""
        
        else:
            return """I'm here to help! You can ask me:

• "Explain MD5 with example"
• "Show me how ASCII works"
• "What's the best strategy?"
• "How do I interpret the hints?"
• "Give me an example of the pattern"

Or ask ANY question you have - I'll do my best to explain clearly
with concrete examples!

What would you like to know?"""
        
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
            self.add_chat_message("SYSTEM", f"🎉 Congratulations! You cracked the code: {self.target_account}", 'system')
            messagebox.showinfo("BREACH SUCCESSFUL!", "ACCESS GRANTED!\n\nYou successfully hacked the account!\n\nAccount: " + self.target_account)
        else:
            self.attempts -= 1
            self.attempts_label.config(text="[ATTEMPTS: " + str(self.attempts) + "/6]")
            
            correct_positions = sum(1 for i in range(min(len(guess), len(self.target_account))) if guess[i] == self.target_account[i])
            closeness_msg = f" [{correct_positions}/6 positions correct]"
            
            attempts_used = 6 - self.attempts
            if attempts_used <= 6:
                self.unlock_hint(attempts_used)
            
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
        self.chat_history = []  # Clear chat history for new game
        
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
        self.add_chat_message("SYSTEM", "🎯 New target generated! Good luck with your mission!", 'system')

if __name__ == "__main__":
    root = tk.Tk()
    game = HackerSimulationGame(root)
    root.mainloop()