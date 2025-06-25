import tkinter as tk
from gui import BibliothequeGUI  

def main():
    root = tk.Tk()
    app = BibliothequeGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()