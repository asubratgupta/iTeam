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
    unwanted_char = ['/', '?', '.', '=']  # Replaced with Single Space
    clean_url = course_url
    for char in ignore_char:
        clean_url = clean_url.replace(char, '')
    for char in unwanted_char:
        clean_url = clean_url.replace(char, ' ')
    return clean_url


def find_courses(tags_list):
    course_urls = list()
    print(tags_list)
    docs = db.collection(u'urls_db').where(u'tags', u'array_contains_any', tags_list).stream()

    for doc in docs:
        course_urls.append(db.collection(u'urls_db').document(doc.id).get().to_dict()['course_url'])
    print(course_urls)
    return course_urls


root = tk.Tk()

root.wm_title('Search Course by TAG')
root.minsize(500, 700)

tk.Label(root, text='Enter TAGs (Space Seprated)').grid(row=0)
e1 = tk.Entry(root)
e1.grid(row=0, column=1)


def search_course(*args):
    tags = url_cleaner(e1.get())
    tags_list = tags.split(' ')
    courses = find_courses(tags_list)
    results = 'URLs\n'
    for course in courses:
        results = results + '\n' + course
    tk.Label(root, text=results).grid(row=5)


button = tk.Button(root, text='Search Course', width=25, command=search_course)
button.grid(row=2, column=1)

tk.Label(root, text='').grid(row=3)
tk.Label(root, text='Search Results').grid(row=4)
tk.Label(root, text='').grid(row=5)


def back():
    root.destroy()


button = tk.Button(root, text='Back to Main Menu', width=25, command=back)
button.grid(row=6, column=1)

root.mainloop()
