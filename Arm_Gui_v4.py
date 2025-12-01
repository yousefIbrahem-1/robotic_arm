import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sv_ttk
import pywinstyles
import sys
import ctypes
import time
import threading
import pyaudio
import speech_recognition 
import os
import serial
import tempfile
import wave
import io
from vosk import Model, KaldiRecognizer

port = 'COM5' 
baudrate = 9600
voice_model_location ="C:\\robotic_arm" # غيرو مكان الموديل عندكم

serial_connection = None
serial_lock = threading.Lock()

def send_to_arduino(data):
    global serial_connection
    if serial_connection and serial_connection.is_open:
        print("sending data to arduino")
        with serial_lock:
            serial_connection.write(data.encode())
            serial_connection.flush()
    else:
        raise Exception("Arduino is not connected.")

def receive_from_arduino():
    global serial_connection
    if serial_connection and serial_connection.is_open:
        with serial_lock:
            return serial_connection.readline().decode().strip()
    else:
        raise Exception("Arduino is not connected.")

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', ' ': ' ',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'
}

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()
    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

class MainPage:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.is_connected = False

    def setup_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width * 0.5)
        height = int(screen_height * 0.6)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.title("Multi-Functional Humanoid Arm")

        self.main_frame = ttk.Frame(self.root, padding="40")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X)

        self.connection_frame = ttk.Frame(self.top_frame)
        self.connection_frame.pack(side=tk.LEFT)

        self.connect_btn = ttk.Button(self.connection_frame, text="Connect to Arduino", command=self.attempt_connection)
        self.connect_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.status_canvas = tk.Canvas(self.connection_frame, width=20, height=20)
        self.status_indicator = self.status_canvas.create_oval(2, 2, 18, 18, fill="red")
        self.status_canvas.pack(side=tk.LEFT)

        self.center_frame = ttk.Frame(self.main_frame)
        self.center_frame.pack(expand=True)

        self.title_label = ttk.Label(self.center_frame, text="Welcome", font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=30)

        self.morse_btn = ttk.Button(self.center_frame, text="Morse Code Converter", command=self.open_morse_gui, style='Accent.TButton', padding=(20, 10))
        self.morse_btn.pack(pady=20)

        self.poses_btn = ttk.Button(self.center_frame, text="Hand Poses Control", command=self.open_poses, style='Accent.TButton', padding=(20, 10))
        self.poses_btn.pack(pady=20)

        self.games_btn = ttk.Button(self.center_frame, text="Games", command=self.open_games, style='Accent.TButton', padding=(20, 10))
        self.games_btn.pack(pady=20)

    def attempt_connection(self):
        global serial_connection
        if not self.is_connected:
            self.connect_btn.configure(state='disabled')
            threading.Thread(target=self.connect_to_arduino, daemon=True).start()
        else:
            serial_connection.close()
            self.is_connected = False
            self.status_canvas.itemconfig(self.status_indicator, fill="red")
            self.connect_btn.configure(text="Connect to Arduino")

    def connect_to_arduino(self):
        global serial_connection
        try:
            serial_connection = serial.Serial(port, baudrate, timeout=2)
            for i in range(3, 0, -1):
                self.connect_btn.configure(text=f"Connecting... ({i})")
                time.sleep(1)

            self.is_connected = True
            self.status_canvas.itemconfig(self.status_indicator, fill="green")
            self.connect_btn.configure(text="Disconnect", state='normal')
            messagebox.showinfo("Success", "Successfully connected to Arduino!")
        except serial.SerialException as e:
            messagebox.showerror("Connection Error", f"Failed to connect to Arduino:\n{e}")
            self.connect_btn.configure(text="Connect to Arduino", state='normal')
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error occurred:\n{e}")
            self.connect_btn.configure(text="Connect to Arduino", state='normal')

    def open_morse_gui(self):
        self.root.withdraw()
        Morse(self)

    def open_poses(self):
        self.root.withdraw()
        Poses(self)
    
    def open_games(self):
        self.root.withdraw()
        Games(self)

    def show(self):
        self.root.deiconify()

    def run(self):
        sv_ttk.set_theme("dark")
        apply_theme_to_titlebar(self.root)
        self.root.mainloop()

class Morse:
    def __init__(self, main_page):
        self.main_page = main_page
        self.root = tk.Toplevel()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width * 0.5)
        height = int(screen_height * 0.6)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.title("Morse Code Converter")

        style = ttk.Style()
        style.configure("Record.TButton",relief="flat", background="#FF6347", foreground="#FFFFFF", font=("Arial", 12, "bold"), padding=10)

        self.main_frame = ttk.Frame(self.root, padding="40")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.center_frame = ttk.Frame(self.main_frame)
        self.center_frame.pack(expand=True)

        self.title_label = ttk.Label(self.center_frame, text="Text to Morse Code Converter", font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=30)

        self.input_label = ttk.Label(self.center_frame, text="Enter text:", font=("Helvetica", 16))
        self.input_label.pack(pady=10)

        self.input_text = ttk.Entry(self.center_frame, width=40, font=("Helvetica", 14))
        self.input_text.pack(pady=10)
        self.input_text.bind('<Return>', lambda e: self.convert_to_morse())

        self.output_label = ttk.Label(self.center_frame, text="Morse code:", font=("Helvetica", 16))
        self.output_label.pack(pady=10)

        self.output_text = ttk.Entry(self.center_frame, width=40, font=("Helvetica", 14), state='readonly')
        self.output_text.pack(pady=10)

        self.button_frame = ttk.Frame(self.center_frame)
        self.button_frame.pack(pady=30)

        self.convert_button = ttk.Button(self.button_frame, text="Convert", command=self.convert_to_morse, style='Accent.TButton', padding=(20, 10))
        self.convert_button.pack(side=tk.LEFT, padx=10)

        self.record_button = ttk.Button(self.button_frame, text="Record", command=self.record_txt, style='Danger.TButton', padding=(20, 10))
        self.record_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = ttk.Button(self.button_frame, text="Clear", command=self.clear_fields, padding=(20, 10))
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.return_btn = ttk.Button(self.center_frame, text="Return to Main Page", command=self.return_to_main)
        self.return_btn.pack(pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.return_to_main)
        sv_ttk.set_theme("dark")
        apply_theme_to_titlebar(self.root)

    def convert_to_morse(self):
        text = self.input_text.get().upper()
        morse = ' '.join(MORSE_CODE[x] if x in MORSE_CODE else '' for x in text).replace('  ', ' / ')
        send_to_arduino(morse + '\n')
        
        self.output_text.configure(state='normal')
        self.output_text.delete(0, tk.END)
        self.output_text.insert(0, morse.strip())
        self.output_text.configure(state='readonly')

    def record_txt(self):
        model_path = voice_model_location
        if not os.path.exists(model_path):
            messagebox.showerror("Error", "Vosk model not found! Please check the path.")
            return

        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)

        self.record_button.configure(state='disabled', text="Recording...")
        threading.Thread(target=self.rp_audio, args=(recognizer,), daemon=True).start()

    def rp_audio(self, recognizer):
        try:
            sr_recognizer = sr.Recognizer()
            with sr.Microphone(sample_rate=16000) as source:
                sr_recognizer.adjust_for_ambient_noise(source, duration=1)
                sr_recognizer.dynamic_energy_threshold = True
                audio = sr_recognizer.listen(source, timeout=5, phrase_time_limit=10)

            audio_data = audio.get_wav_data()
        
            self._process_audio(audio_data, recognizer)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.record_button.configure(state='normal', text="Record")

    def _process_audio(self, audio_data, recognizer):
        with wave.open(io.BytesIO(audio_data), "rb") as wf:
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    break

        result = recognizer.Result()
        text = eval(result).get("text", "").capitalize()

        self.input_text.delete(0, "end")
        self.input_text.insert(0, text)
        self.convert_to_morse()


    def clear_fields(self):
        self.input_text.delete(0, tk.END)
        self.output_text.configure(state='normal')
        self.output_text.delete(0, tk.END)
        self.output_text.configure(state='readonly')

    def return_to_main(self):
        self.root.destroy()
        self.main_page.show()

class Poses:
    def __init__(self, main_page):
        self.main_page = main_page
        self.root = tk.Toplevel()
        self.root.tk.call('tk', 'scaling', self.root.winfo_fpixels('1i') / 72.0)
        self.default_pose = "Touch & Hold"
        self.current_pose = self.default_pose
        self.setup_window()

    def setup_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width * 0.5)
        height = int(screen_height * 0.6)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.title("Hand Poses Control")

        self.main_frame = ttk.Frame(self.root, padding="40")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.title_label = ttk.Label(self.header_frame, text="Select Hand Pose",font=("Helvetica", 28, "bold"))
        self.title_label.pack()

        self.pose_frame = ttk.LabelFrame(self.main_frame, text="Available Poses", padding=15)
        self.pose_frame.pack(fill=tk.X, pady=(0, 20))

        self.pose_frame.configure(text="Poses")
        ttk.Style().configure('TLabelframe.Label', font=("Helvetica", 12))

        self.poses = [
            "Touch & Hold",
            "Peace Pose",
            "Thumbs Up Pose",
            "Gun Pose",
        ]

        self.poses_angles = {"Touch & Hold": "180,0,0,0,0,0",
                             "Peace Pose": "90,90,0,0,160,90",
                             "Thumbs Up Pose": "180,0,160,160,160,90",
                             "Gun Pose": "180,0,0,0,160,90"}
        
        self.pose_var = tk.StringVar(value=self.current_pose)
        self.pose_dropdown = ttk.Combobox(self.pose_frame, textvariable=self.pose_var,values=self.poses,state='readonly',font=("Helvetica", 12),width=30)
        self.pose_dropdown.pack(pady=10)

        self.current_pose_frame = ttk.LabelFrame(self.main_frame, text="Current Pose", padding=15)
        self.current_pose_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.current_pose_label = ttk.Label(self.current_pose_frame,text=self.current_pose,font=("Helvetica", 12))
        self.current_pose_label.pack(pady=10)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=20)

        self.select_button = ttk.Button(self.button_frame,text="Select Pose",command=self.select_pose,style='Accent.TButton',padding=(20, 10))
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(self.button_frame,text="Reset to Default",command=self.reset_pose,padding=(20, 10))
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        self.return_btn = ttk.Button(self.nav_frame,text="Return to Main Page",command=self.return_to_main,padding=(20, 10))
        self.return_btn.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.return_to_main)

        sv_ttk.set_theme("dark")
        apply_theme_to_titlebar(self.root)

    def select_pose(self):
        selected = self.pose_var.get()
        self.current_pose = selected
        self.current_pose_label.config(text=selected)
        messagebox.showinfo("Success", f"Pose changed to: {selected}")
        
    def reset_pose(self):
        self.pose_var.set(self.default_pose)
        self.current_pose = self.default_pose
        self.current_pose_label.config(text=self.default_pose)
        messagebox.showinfo("Success", "Pose reset to default: Touch & Hold")
        
    def return_to_main(self):
        self.root.destroy()
        self.main_page.show()

    def run(self):
        self.root.mainloop()

class Games:
    def __init__(self, main_page):
        self.main_page = main_page
        self.root = tk.Toplevel()
        self.root.tk.call('tk', 'scaling', self.root.winfo_fpixels('1i') / 72.0)
        self.setup_window()

    def setup_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width * 0.5)
        height = int(screen_height * 0.6)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.title("Games")

        self.main_frame = ttk.Frame(self.root, padding="40")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(self.main_frame, text="Games", font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=30)

        

        self.return_btn = ttk.Button(self.main_frame, text="Return to Main Page", command=self.return_to_main)
        self.return_btn.pack(pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.return_to_main)
        sv_ttk.set_theme("dark")
        apply_theme_to_titlebar(self.root)

    def return_to_main(self):
        self.root.destroy()
        self.main_page.show()        


if __name__ == '__main__':
    MainPage().run()
