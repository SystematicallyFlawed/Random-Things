import tkinter as tk

cat_art = r"""
          ____
         ／＞　  ＞
       | 　_　 _|
    ／` ミ＿xノ
／　　　     |   
    　　　                        / 　 ヽ　     ﾉ                                ,---'  '---.
    　 　                            │　　|　|　|                               /                \
----------------------------------------------------／￣|　　 |　|　|-------------------------|      |     |      |----------------------
    　                          | (￣ヽ＿ヽ)__)__)                             \       w       /
                                ＼二つ                                                 `--..__..--'
              
"""

def ascii_art():
    root = tk.Tk()
    root.title("Cat with a pumpkin")
    label = tk.Label(root,text=cat_art,fg="black", font=("",30))
    label.pack(pady=10)
    root.mainloop()

ascii_art()