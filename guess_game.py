import sys
import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
from playsound import playsound

import os
    
# 🎵 تشغيل الصوت في الخلفية
def resource_path(relative_path):
    try:
        # عند التشغيل من ملف تنفيذي
        base_path = sys._MEIPASS
    except Exception:
        # عند التشغيل من بايثون مباشرة
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def play_success():
    threading.Thread(target=lambda: playsound(resource_path("sounds/success.mp3"))).start()

def play_error():
    threading.Thread(target=lambda: playsound(resource_path("sounds/error.mp3"))).start()

# 🔁 بدء لعبة جديدة
def start_new_game():
    global secret_number, start_time, attempts_left
    secret_number = random.randint(1, 10)
    attempts_left = 5
    result_label.config(text="", fg="#333")
    entry.delete(0, tk.END)
    guess_button.config(state="normal")
    attempts_label.config(text=f"💡 المحاولات المتبقية: {attempts_left}")
    start_time = time.time()
    update_timer()
    main_frame.config(bg="#fdfdfd")
    entry.focus()

# ✅ التحقق من التخمين
def check_guess():
    global attempts_left
    try:
        guess = int(entry.get())
        attempts_left -= 1
        attempts_label.config(text=f"💡 المحاولات المتبقية: {attempts_left}")
        if guess == secret_number:
            play_success()
            elapsed = int(time.time() - start_time)
            result_label.config(text=f"🎉 أحسنت! الرقم الصحيح هو {secret_number}.\nاستغرقت {elapsed} ثانية.", fg="#2e7d32")
            guess_button.config(state="disabled")
            main_frame.config(bg="#e8f5e9")  # خلفية خضراء ناعمة
            messagebox.showinfo("🎉 فوز!", f"أحسنت! الرقم كان {secret_number}.\nالوقت: {elapsed} ثانية.")
        elif attempts_left == 0:
            play_error()
            result_label.config(text=f"😢 انتهت المحاولات. الرقم الصحيح هو {secret_number}.", fg="#c62828")
            guess_button.config(state="disabled")
            main_frame.config(bg="#ffebee")  # خلفية حمراء ناعمة
            messagebox.showwarning("😢 خسارة", f"انتهت المحاولات.\nالرقم الصحيح كان: {secret_number}")
        elif guess < secret_number:
            play_error()
            result_label.config(text="📉 الرقم أكبر من ذلك.", fg="#0277bd")
            entry.delete(0, tk.END)
        else:
            play_error()
            result_label.config(text="📈 الرقم أصغر من ذلك.", fg="#ef6c00")
            entry.delete(0, tk.END)
    except ValueError:
        play_error()
        result_label.config(text="❌ الرجاء إدخال رقم صحيح.", fg="#c62828")
        entry.delete(0, tk.END)

# ⏱️ تحديث المؤقت
def update_timer():
    if guess_button['state'] == "normal":
        elapsed = int(time.time() - start_time)
        timer_label.config(text=f"⏱ الوقت: {elapsed} ثانية")
        root.after(1000, update_timer)

# 🖼️ إعداد الواجهة
root = tk.Tk()
root.title("🎮 لعبة التخمين")
root.geometry("400x330")
root.configure(bg="#fdfdfd")

main_frame = tk.Frame(root, bg="#fdfdfd")
main_frame.pack(expand=True, fill="both")

welcome_label = tk.Label(main_frame, text="🎮 مرحبًا بك في لعبة التخمين!", font=("Segoe UI", 13, "bold"), bg="#fdfdfd", fg="#333")
welcome_label.pack(pady=10)

instruction_label = tk.Label(main_frame, text="اختر رقمًا بين 1 و 10", font=("Segoe UI", 11), bg="#fdfdfd", fg="#555")
instruction_label.pack()

#bd=3	عرض الحافة	يعطي الحقل إطارًا بسيطًا
#relief="groove"	شكل الحافة	يجعل الحافة تبدو محفورة قليلاً
#width=10	عرض الحقل	عدد الأحرف التي يمكن عرضها أفقيًا

entry = tk.Entry(main_frame, font=("Segoe UI", 12), justify="center", bd=3, relief="groove", width=10)
entry.pack(pady=8)
entry.bind("<Return>", lambda event: check_guess())  # ⏎ تنفيذ التخمين عند الضغط على Enter


guess_button = tk.Button(main_frame, text="تحقق", command=check_guess, font=("Segoe UI", 11, "bold"),
                         bg="#007acc", fg="white", activebackground="#005f99", cursor="hand2", width=15)
guess_button.pack(pady=5)

result_label = tk.Label(main_frame, text="", font=("Segoe UI", 11), bg="#fdfdfd", fg="#333")
result_label.pack(pady=10)

attempts_label = tk.Label(main_frame, text="💡 المحاولات المتبقية: 5", font=("Segoe UI", 10), bg="#fdfdfd", fg="#666")
attempts_label.pack()

timer_label = tk.Label(main_frame, text="⏱ الوقت: 0 ثانية", font=("Segoe UI", 10), bg="#fdfdfd", fg="#666")
timer_label.pack()

restart_button = tk.Button(main_frame, text="🔄 إعادة اللعب", command=start_new_game, font=("Segoe UI", 11, "bold"),
                           bg="#43a047", fg="white", activebackground="#388e3c", cursor="hand2", width=15)
restart_button.pack(pady=10)

# بدء اللعبة
# بدء اللعبة بعد عرض النافذة
def delayed_start():
    start_new_game()
    entry.focus()

root.after(500, delayed_start)
root.mainloop()

