import tkinter as tk
import Initialised
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('iteam-3b0d1-firebase-adminsdk-o179z-d503c5a2a9.json')
if not Initialised.isInitialised():
    firebase_admin.initialize_app(cred)
    Initialised.setInitialised()
db = firestore.client()


def url_cleaner(course_url):
    ignore_char = ['https', 'www', '.in', 'http', '.com', ':', '//']  # Replaced with Nothing
    unwanted_char = ['/', '?', '.', '=', '-']  # Replaced with Single Space
    clean_url = course_url
    for char in ignore_char:
        clean_url = clean_url.replace(char, '')
    for char in unwanted_char:
        clean_url = clean_url.replace(char, ' ')
    return clean_url


learners_details = list()


def find_learners(course_url, language):
    global learners_details

    clean_url = url_cleaner(course_url)
    doc_ref = db.collection(u'urls_db').document(clean_url)

    docs = doc_ref.collection(u'students_email').stream()

    learners = list()

    for doc in docs:
        learners.append(doc.id)

    for learner in learners:
        doc_ref = db.collection(u'users_db').document(learner)
        doc = doc_ref.get()
        learners_details.append(doc.to_dict())


root = tk.Tk()

root.wm_title('Search Learners by URL')
root.minsize(500, 700)

tk.Label(root, text='Course URL').grid(row=0)
e1 = tk.Entry(root)
e1.grid(row=0, column=1)

# Location Drop Down
# Create a Tkinter variable
tkvar = tk.StringVar(root)

# Dictionary with options
choices = ['Hindi', 'English']
tkvar.set('English')  # set the default option

popupMenu = tk.OptionMenu(root, tkvar, *choices)
tk.Label(root, text="Preferred Language").grid(row=1, column=0)
popupMenu.grid(row=1, column=1)


def change_dropdown(*args):
    return tkvar.get()


# link function to change dropdown
tkvar.trace('w', change_dropdown)

course_url, language = '', ''


def update(*args):
    global course_url, language, learners_details
    learners_details = list()
    print('clicked')
    course_url, language = e1.get(), change_dropdown()
    find_learners(course_url, language)
    results = 'Full Name\t\tContact Number\t\tEmail ID\t\tLanguage'
    for learner in learners_details:
        results = results + '\n' + learner['full_name'] + '\t' + learner['contact_number'] + '\t' + learner[
            'email_id'] + '\t' + learner['language']
    print(results)
    tk.Label(root, text=results).grid(row=5)


button = tk.Button(root, text='Find Learners', width=25, command=update)
button.grid(row=2, column=1)

tk.Label(root, text='').grid(row=3)
tk.Label(root, text='Search Results').grid(row=4)
tk.Label(root, text='').grid(row=5)


def back():
    root.destroy()


button = tk.Button(root, text='Back to Main Menu', width=25, command=back)
button.grid(row=6, column=1)

root.mainloop()
