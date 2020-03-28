import tkinter as tk

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('iteam-3b0d1-firebase-adminsdk-o179z-d503c5a2a9.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def add_course(full_name, email_id, contact_number, course_url, language):
    # Use a service account
    doc_ref = db.collection(u'users_db').document(email_id)
    doc_ref.set({
        u'full_name': full_name,
        u'email_id': email_id,
        u'contact_number': contact_number,
        # u'course_url': course_url,
        u'language': language
    })

    def url_cleaner(course_url):
        ignore_char = ['https', 'www', '.in', 'http', '.com', ':', '//']  # Replaced with Nothing
        unwanted_char = ['/', '?', '.', '=']  # Replaced with Single Space
        clean_url = course_url
        for char in ignore_char:
            clean_url = clean_url.replace(char, '')
        for char in unwanted_char:
            clean_url = clean_url.replace(char, ' ')
        return clean_url

    clean_url = url_cleaner(course_url)
    tags = clean_url.split(' ')

    doc_ref.collection(u'course_url').document(clean_url).set({u'course_url': course_url}) # updating in users_db

    doc_ref = db.collection(u'urls_db').document(clean_url)
    doc_ref.set({
        u'course_url': course_url,
        u'tags': tags
    })
    doc_ref.collection(u'students_email').document(email_id).set({u'email_id': email_id})

root = tk.Tk()

root.wm_title('Add Course')
root.minsize(500, 700)

tk.Label(root, text='Full Name').grid(row=0)
tk.Label(root, text='Email').grid(row=1)
tk.Label(root, text='Contact No.').grid(row=2)
tk.Label(root, text='Course URL').grid(row=3)
e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)
e4 = tk.Entry(root)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

# Location Drop Down
# Create a Tkinter variable
tkvar = tk.StringVar(root)

# Dictionary with options
choices = ['Hindi','English']
tkvar.set('English') # set the default option

popupMenu = tk.OptionMenu(root, tkvar, *choices)
tk.Label(root, text="Preferred Language").grid(row = 4, column = 0)
popupMenu.grid(row = 4, column =1)

def change_dropdown(*args):
   return tkvar.get()

# link function to change dropdown
tkvar.trace('w', change_dropdown)

full_name, email_id, contact_number, course_url, language = '', '', '', '', ''
def update(*args):
   global full_name, email_id, contact_number, course_url, language
   full_name, email_id, contact_number, course_url, language = e1.get(), e2.get(), e3.get(), e4.get(), change_dropdown()
   add_course(full_name, email_id, contact_number, course_url, language)

button = tk.Button(root, text='Submit', width=25, command=update)
button.grid(row=7, column=1)

root.mainloop()