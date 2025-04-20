import os
import webbrowser
import threading

def open_browser():
    webbrowser.open_new("http://localhost:8501")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()  # يفتح المتصفح بعد ثانية ونص تلقائياً
    os.system("streamlit run goldenhunt.py")  # اسم الملف الأساسي

