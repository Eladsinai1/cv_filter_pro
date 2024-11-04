import os #ספריה שמטפלת בקבצים כלליים תיקיות וכו
import docx #ספריה שמטפלת בקבצי וורד
from nltk.stem import SnowballStemmer #ספריית הNLP שמטפלת במילים ותוכן
from nltk.tokenize import word_tokenize
import shutil #ספרייה שמטפלת בהעברת קבצים
import tkinter as tk #ספרייה שמטפלת בעיצוב גרפי
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk #ספריה שמטפלת בתמונות
import pkg_resources
import PyPDF2

def remove_duplicates(input_list):
    unique_list = []
    for element in input_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list

def browse_folder():#פונקציית כפתור החיפוש מופעלת למטה כאשר לוחצים על כפתור החיפוש וגורמת לפתיחת המחשב לעיון עבור בחירת תיקייה
    global folder_path
    folder_path = filedialog.askdirectory()
    folder_path_var.set(folder_path)

def browse_output_folder():#כמו פונקציית כפתור החיפוש רק של תיקיית היעד מופעל שלוחצים על כפתור תיקיית היעד
    global output_folder_path
    output_folder_path = filedialog.askdirectory()
    output_folder_path_var.set(output_folder_path)

def search_files():#בגדול כל האלגוריתם פה (פונקציית סינון הקבצים מופעלת בלחיצת כפתור החיפוש)
    result_text.configure(state='normal')
    num = int(num_req_entry.get())
    word = keywords_entry.get("1.0", tk.END).splitlines()
    new_word = []
    for w in word:
        new_word.append(stemmer.stem(w))
    temp = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                cv_var = []
                chek_list = []
                for page in pdf.pages:
                    text = page.extract_text()
                    cv_split_word = word_tokenize(text)
                    stemmed_words = [stemmer.stem(word) for word in cv_split_word]
                    for stem in stemmed_words:
                        cv_var.append(stem)
                for j in new_word:
                    flag = False
                    if j in cv_var:
                        flag = True
                    chek_list.append(flag)
                filterd_chek_list = remove_duplicates(chek_list)

                if len(filterd_chek_list) == 1 and filterd_chek_list[0] == True:
                    temp.append(file_path)
        if filename.endswith('.docx'):
            file_path = os.path.join(folder_path, filename)
            doc = docx.Document(file_path)
            chek_list = []
            cv_var=[]
            for para in doc.paragraphs:
                text = para.text
                cv_split_word = word_tokenize(text)
                stemmed_words = [stemmer.stem(word) for word in cv_split_word]
                for stem in stemmed_words:
                    cv_var.append(stem)
            for j in new_word:
                flag = False
                if j in cv_var:
                   flag=True
                chek_list.append(flag)
            filterd_chek_list=remove_duplicates(chek_list)

            if len(filterd_chek_list)==1 and filterd_chek_list[0]==True:
                temp.append(file_path)

    search_results = remove_duplicates(temp)
    result_text.delete("1.0", tk.END)
    if len(search_results)==0:
        result_text.insert(tk.END,"There is no results")
    else:
        messagebox.showinfo("Success", "Found "+str(len(search_results))+" results matching your search" )
        for path in search_results:
            result_text.insert(tk.END, os.path.splitext(os.path.basename(path))[0] + '\n')
            file_name = os.path.basename(path)
            output_file_path = os.path.join(output_folder_path, file_name)
            shutil.move(path, os.path.join(output_folder_path, os.path.splitext(os.path.basename(path))[0] + os.path.splitext(path)[1]))


def move_to_keywords(input_value):#בודק את תקינות התווים בתיבת מספר הדרישות
    if input_value.isdigit() or input_value == "":
        return True
    else:
        messagebox.showwarning("Invalid Input", "Please enter a number")
        return False

def move_focus_to_keywords(event):#בודק את תקינות התווים בתיבת מספר הדרישות ובנוסף מעביר את הפוקוס (הסמן של העכבר) לתיבה של מילות המפתח לאחר שהוזנה אות ונלחץ אנטר ובנוסף פותח את התיבה לעריכה
    if len(num_req_entry.get())==0:
        messagebox.showwarning("Invalid Input", "Please enter a number")
    else:
        keywords_entry.focus_set()
        num_req_entry.configure(state='disabled')
        keywords_entry.configure(state="normal")

def on_keywords_change(event):#פונקציה שבודקת מה קורה בתיבה של מילות המפתח (אם הוזנו מילים כמה הוזנו וכו) לאחר שהוזנו כל המילים הדרושות נועלת את התיבה לשינויים
    num_lines = int(keywords_entry.index(tk.END).split('.')[0])-1
    num_req = int(num_req_entry.get())
    if num_lines>0:
        num_req_entry.configure(state="disabled")
    if event.keysym == 'Return':
        num_lines+=1
    if num_lines > num_req:
        keywords_entry.configure(state='disabled')
        browse_button.focus_set()

def start_document_search():#פונקציה שעוברת ממסך הבית למסך החיפוש קבצים (בעת לחיצה על כפתור הSTART) יוצרת כפתור יציאה במסך החיפוש ומעביר פוקוס לתיבה של מספר דרישות
    root.withdraw()
    document_search_window.deiconify()
    document_search_window.focus_set()
    num_req_entry.focus_set()

def confirm_exit():#אחראי על הודעת היציאה בעת לחיצה על כפתור היציאה ואחראי על יציאה מהמסמך
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        login_window.destroy()

def login(event=None):
    username = username_entry.get()
    if not username:
        messagebox.showerror("Error", "Please enter a username.")
        return
    password_entry.focus_set()

def validate_login(event=None):
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "12345":
        login_window.withdraw()
        root.deiconify()
        root.focus_set()
    elif username == "admin":
        messagebox.showerror("Invalid Login", "Incorrect password.")
    else:
        messagebox.showerror("Invalid Login", "Incorrect username.")

def reset_fields():
    num_req_entry.configure(state="normal")
    num_req_entry.delete(0, tk.END)
    keywords_entry.configure(state="normal")
    keywords_entry.delete("1.0", tk.END)
    folder_path_var.set("")
    output_folder_path_var.set("")
    result_text.configure(state="normal")
    result_text.delete(1.0, tk.END)
    num_req_entry.focus_set()
    keywords_entry.configure(state="disabled")
    result_text.configure(state="disabled")

def minimize_root():
    root.iconify()

def minimize_serch():
    document_search_window.iconify()

login_window = tk.Tk()
login_window.title("Login")
login_window.attributes('-fullscreen', True)
login_window.configure(background='#%02x%02x%02x' % (212, 234, 255))
login_window.bind("<Return>", login)

login_label=tk.Label(login_window, text="Welcome to our application, \n"
" designed to streamline your recruitment process. We are excited to introduce you to a user-friendly platform that will make recruiting easier and more efficient. \n"
"To get started, log in with your username and password. Once logged in, you'll be directed to our home page.", font=("Helvetica", 14, "bold"), bd=1, relief="solid")
login_label.pack(side="top", padx=10, pady=45)
login_label.configure(background='#%02x%02x%02x' % (212, 234, 255))

image_front = pkg_resources.resource_filename(__name__, 'photos/photo5.jpg')
image_1 = Image.open(image_front)
image_1 = image_1.resize((600, 300))  # Adjust the size of the image as needed
tk_image_1 = ImageTk.PhotoImage(image_1)
image_label_1 = tk.Label(login_window, image=tk_image_1)
image_label_1.pack(pady=40)

username_label = tk.Label(login_window, text="Username:",font=font.Font(size=13),width=23)
username_label.configure(background='#%02x%02x%02x' % (124, 169, 209))
username_label.pack(pady=5)
username_entry = tk.Entry(login_window,font=font.Font(size=12),width=23)
username_entry.pack(pady=10)
username_entry.focus_set()

line_space_label = tk.Label(login_window, height=1)
line_space_label.pack()
line_space_label.configure(background='#%02x%02x%02x' % (212, 234, 255))

password_label = tk.Label(login_window, text="Password:",font=font.Font(size=13),width=23)
password_label.pack(pady=5)
password_label.configure(background='#%02x%02x%02x' % (124, 169, 209))
password_entry = tk.Entry(login_window, show="*",font=font.Font(size=12),width=23)
password_entry.pack(pady=10)
password_entry.bind("<Return>", validate_login)

exit_button = tk.Button(login_window, text="X", command=confirm_exit, width=3,fg="white", bg="red")
exit_button.place(x=0, y=0)

line_space_label = tk.Label(login_window, height=2)
line_space_label.pack()
line_space_label.configure(background='#%02x%02x%02x' % (212, 234, 255))

login_button = tk.Button(login_window,text="login", font=("Helvetica", 18), command=validate_login)
login_button.pack(pady=10)
login_button.configure(bg='#%02x%02x%02x' % (212, 216, 220))

root = tk.Toplevel(login_window)#הפעלת ויצירת המסך הראשי
root.attributes('-fullscreen', True)
root.title("REP")
root.protocol("WM_DELETE_WINDOW", confirm_exit)  # Confirm exit when the window is closed using the 'X' button
root.configure(background='#%02x%02x%02x' % (212, 234, 255))

# יצירת כיתוב הכותרת במסך הפתיחה
welcome_label = tk.Label(root, text="Welcome to REP - CV scanning", font=("Helvetica", 24, "bold"))
welcome_label.pack(pady=50)
welcome_label.configure(background='#%02x%02x%02x' % (212, 234, 255))
# העלאת תמונה (הנתיב לתמונה מהמחשב שלי אז אם מחליפים צריך להחליף נתיב)
image_path = pkg_resources.resource_filename(__name__, 'photos/home.jpg')
image = Image.open(image_path)
image = image.resize((500, 250))  # Adjust the size of the image as needed
tk_image = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=tk_image)
image_label.pack(pady=20)

instructions_label=tk.Label(root, text="Dear Employer, \n"
"On the next page please enter the number of requirements for this position and the talents or skills you are looking for (as single words)\n"
" Select the folder where the resume files are located and the destination folder for filtered resumes.",font=("Helvetica", 16,"bold"))
instructions_label.pack(side="top", padx=10, pady=40)
instructions_label.configure(background='#%02x%02x%02x' % (212, 234, 255))

# יצירת כפתור ההתחל
start_button = tk.Button(root, text="Start", font=("Helvetica", 18), command=start_document_search)
start_button.pack()
start_button.configure(bg='#%02x%02x%02x' % (212, 216, 220))

minimize_button = tk.Button(root, text="-", command=minimize_root, width=3)
minimize_button.place(x=30, y=0)
exit_button = tk.Button(root, text="X", command=confirm_exit, width=3,fg="white", bg="red")
exit_button.place(x=0, y=0)

#יצירת מסך החיפוש
document_search_window = tk.Toplevel(root)
document_search_window.title("Document Search")
document_search_window.attributes('-fullscreen', True)
document_search_window.protocol("WM_DELETE_WINDOW", confirm_exit)  # Confirm exit when the window is closed using the 'X' button
document_search_window.withdraw()
document_search_window.configure(background='#%02x%02x%02x' % (212, 234, 255))

minimize_button = tk.Button(document_search_window, text="-", command=minimize_serch, width=3)
minimize_button.place(x=30, y=0)
exit_button = tk.Button(document_search_window, text="X", command=confirm_exit, width=3,fg="white", bg="red")
exit_button.place(x=0, y=0)

#יצירת תיבת מספר הדרישות והפעלת הפונקציות הדרושות לתיבה זו (בדיקת תקינות הקלט)
line_space_label = tk.Label(document_search_window, height=3)
line_space_label.pack()
line_space_label.configure(background='#%02x%02x%02x' % (212, 234, 255))

num_req_label = tk.Label(document_search_window, text="Number of Requirements:",font=font.Font(size=12),width=23, bd=1)
num_req_label.pack(pady=5)
num_req_entry = tk.Entry(document_search_window, validate="key",font=("Helvetica", 12, "bold"),width=23)
num_req_entry.configure(validatecommand=(num_req_entry.register(move_to_keywords), '%P'))
num_req_entry.configure(validatecommand=(num_req_entry.register(move_to_keywords), '%P'))
num_req_entry.bind("<Return>", move_focus_to_keywords)
num_req_entry.pack(pady=5)
num_req_label.configure(bg='#%02x%02x%02x' % (212, 234, 255))
num_req_entry.configure(background='#%02x%02x%02x' % (240, 240, 236))

#יצירת תיבהת מילות הפתח והפעלת הפונקציות הדרושות לה (בדיקת השינויים בתיבה)
keywords_label = tk.Label(document_search_window, text="Keywords:",font=font.Font(size=12),width=23)
keywords_label.pack(pady=5)
keywords_entry = tk.Text(document_search_window, height=4,font=font.Font(size=12))
keywords_entry.pack(pady=5)
keywords_entry.configure(state='disabled')
keywords_entry.bind("<Key>", on_keywords_change)
keywords_label.configure(bg='#%02x%02x%02x' % (212, 234, 255))
keywords_entry.configure(background='#%02x%02x%02x' % (240, 240, 236))

line_space_label = tk.Label(document_search_window, height=1)
line_space_label.pack()
line_space_label.configure(background='#%02x%02x%02x' % (212, 234, 255))

#יצירת תיבת שדה החיפוש תכלס התיבה נעולה לעריכה היא מקבלת ערכים רק דרך כפתור החיפוש
folder_path_var = tk.StringVar()
folder_path_label = tk.Label(document_search_window, text="Folder Path:",font=font.Font(size=12),width=23, bd=1)
folder_path_label.pack(pady=5)
folder_path_entry = tk.Entry(document_search_window, textvariable=folder_path_var, state='disabled')
folder_path_entry.pack(pady=5)
folder_path_label.configure(bg='#%02x%02x%02x' % (212, 234, 255))

#יצירת כפתור החיפוש והפעלת הפונקציות שלו
browse_button = tk.Button(document_search_window, text="Browse CV Folder",font=font.Font(size=12), command=browse_folder,width=23)
browse_button.pack(pady=5)
browse_button.configure(bg='#%02x%02x%02x' % (124, 169, 209))

line_space_label = tk.Label(document_search_window, height=2)
line_space_label.pack()
line_space_label.configure(background='#%02x%02x%02x' % (212, 234, 255))

#יצירת תיבת תיקיית היעד גם היא נעולה ומקבלת קלט רק מכפתור החיפוש שלה
output_folder_path_var = tk.StringVar()
output_folder_path_label = tk.Label(document_search_window, text="Output Folder Path:",font=font.Font(size=12),width=23)
output_folder_path_label.pack(pady=5)
output_folder_path_entry = tk.Entry(document_search_window, textvariable=output_folder_path_var, state='disabled')
output_folder_path_entry.pack(pady=5)
output_folder_path_label.configure(bg='#%02x%02x%02x' % (212, 234, 255))

#כפתור חיפוש תיקיית היעד
browse_output_button = tk.Button(document_search_window, text="Browse Output Folder",font=font.Font(size=12), command=browse_output_folder,width=23)
browse_output_button.pack(pady=5)
browse_output_button.configure(bg='#%02x%02x%02x' % (124, 169, 209))

#כפתור החיפוש והפעלת הפונקציה שלו (האלגוריתם המסנן)
search_button = tk.Button(document_search_window, text="Search",font=("Helvetica", 15), command=search_files)
search_button.pack(pady=5)
search_button.configure(bg='#%02x%02x%02x' % (212, 216, 220))

line_space_label = tk.Label(document_search_window, height=2)
line_space_label.pack()
line_space_label.configure(background='#%02x%02x%02x' % (212, 234, 255))

#יצירת תיבת התוצאות מקבלת קלט רק מפונקציית החיפוש (התיקיות הרצויות או שאין תוצאות) לא מפעילה פונקציות משל עצמה
result_label = tk.Label(document_search_window, text="Search Result:",font=font.Font(size=12),width=23)
result_label.pack(pady=5)
result_text = tk.Text(document_search_window, height=4,font=("Helvetica", 12, "bold"))
result_text.pack(pady=5)
result_label.configure(bg='#%02x%02x%02x' % (212, 234, 255))
result_text.configure(bg='#%02x%02x%02x' % (240, 240, 236))
result_text.configure(state='disabled')

reset_button = tk.Button(document_search_window, text="Reset", font=("Helvetica", 15), command=reset_fields)
reset_button.pack(pady=10)
reset_button.configure(bg='#%02x%02x%02x' % (212, 216, 220))

stemmer = SnowballStemmer('english')

login_window.mainloop()










