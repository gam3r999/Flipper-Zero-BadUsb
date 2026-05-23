try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import random
    import pyttsx3
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Installing pyttsx3...")
    import subprocess
    import sys
    
    # Note: tkinter comes with Python and cannot be installed via pip
    # If tkinter is missing, you need to install it through your system package manager
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3"])
        import pyttsx3
        import tkinter as tk
        import tkinter.ttk as ttk
        import random
    except Exception as install_error:
        print(f"Failed to install dependencies: {install_error}")
        print("Please install tkinter through your system package manager:")
        print("  Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  Fedora: sudo dnf install python3-tkinter")
        print("  macOS: tkinter should come with Python")
        sys.exit(1)


# Messages for the popup
messages = ["Catch me!", "I'm here!", "Where are you clicking?", "Ooooh, come on!", "It's too easy!"]

# Initialize text-to-speech engine
try:
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)  # Set a reasonable speech rate
    tts_available = True
except Exception as e:
    print(f"Text-to-speech not available: {e}")
    tts_available = False


class CatchMeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Catch Me Game")
        self.master.geometry("300x200")
        
        # Track score
        self.attempts = 0
        self.catches = 0
        
        # Create main frame
        main_frame = ttk.Frame(master, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="Catch Me Game!", 
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Score label
        self.score_label = ttk.Label(
            main_frame,
            text="Score: 0 / 0",
            font=("Helvetica", 12)
        )
        self.score_label.pack(pady=5)
        
        # Start button
        self.start_button = ttk.Button(
            main_frame,
            text="Start Game",
            command=self.spawn_popup
        )
        self.start_button.pack(pady=10)
        
        # Quit button
        quit_button = ttk.Button(
            main_frame,
            text="Quit",
            command=self.master.quit
        )
        quit_button.pack(pady=5)
        
        self.current_popup = None
    
    def speak(self, text):
        """Speak text using text-to-speech if available"""
        if tts_available:
            try:
                # Run in a non-blocking way
                tts_engine.say(text)
                tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def update_score(self):
        """Update the score display"""
        self.score_label.config(text=f"Score: {self.catches} / {self.attempts}")
    
    def spawn_popup(self):
        """Create a new popup window"""
        if self.current_popup:
            return  # Don't spawn multiple popups
        
        self.current_popup = tk.Toplevel(self.master)
        self.current_popup.title("Try to catch me!")
        
        # Random position on screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = random.randint(0, max(0, screen_width - 300))
        y = random.randint(0, max(0, screen_height - 150))
        
        self.current_popup.geometry(f"250x120+{x}+{y}")
        
        # Configure popup appearance
        self.current_popup.configure(bg="black")
        
        # Message label
        message = random.choice(messages)
        message_label = tk.Label(
            self.current_popup,
            text=message,
            font=("Helvetica", 14, "bold"),
            fg="white",
            bg="black"
        )
        message_label.pack(pady=15)
        
        # Catch button
        catch_button = ttk.Button(
            self.current_popup,
            text="Catch!",
            command=self.catch_popup
        )
        catch_button.pack(pady=10)
        
        # Make popup stay on top
        self.current_popup.attributes('-topmost', True)
        
        # Bind close button to missed catch
        self.current_popup.protocol("WM_DELETE_WINDOW", self.miss_popup)
    
    def catch_popup(self):
        """Handle successful catch"""
        self.attempts += 1
        self.catches += 1
        self.update_score()
        
        success_messages = ["Got me!", "You win this round!", "Nice catch!"]
        self.speak(random.choice(success_messages))
        
        if self.current_popup:
            self.current_popup.destroy()
            self.current_popup = None
    
    def miss_popup(self):
        """Handle missed catch (closing window without clicking button)"""
        self.attempts += 1
        self.update_score()
        
        self.speak(random.choice(messages))
        
        if self.current_popup:
            self.current_popup.destroy()
            self.current_popup = None


if __name__ == "__main__":
    root = tk.Tk()
    game = CatchMeGame(root)
    root.mainloop()
