try:
    import Tkinter as tk
except:
    import tkinter as tk

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import webbrowser

import tkinter as tk
# from PyQt5 import QtGui    # or PySide

def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    # # PyQt way to find the screen resolution
    # app = QtGui.QApplication([])
    # screen_width = app.desktop().screenGeometry().width()
    # screen_height = app.desktop().screenGeometry().height()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))
    # toplevel.title("Centered!")

def open_url(url):
    webbrowser.open(url, new=2)

cred = credentials.Certificate('iteam-3b0d1-firebase-adminsdk-o179z-d503c5a2a9.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

LARGE_FONT= ("Verdana", 14)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

clicked_url = ''

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Notification!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    center(popup)
    popup.mainloop()


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        root = self
        root.configure(bg='#90CAF9')
        tk.Label(root, text='\n\nRegister, what are you learning.)', font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=0)
        button = tk.Button(root, text='Add Course', font=("Arial", 20),  width=15, fg="red", command=lambda: master.switch_frame(AddCourse))
        button.grid(row=1)

        tk.Label(root,
                 text='\n\nFind buddies pursuing the same course.', font=LARGE_FONT, bg='#90CAF9', padx=25, pady=10).grid(
            row=2)
        button = tk.Button(root, text='Search Learners', font=("Arial", 20), width=15, fg="green", command=lambda: master.switch_frame(SearchLearners))
        button.grid(row=3)

        tk.Label(root,
                 text='\n\nDiscover courses using TAGs', font=LARGE_FONT, bg='#90CAF9', anchor='center',  padx=25, pady=10).grid(
            row=4)
        button = tk.Button(root, text='Search Course', font=("Arial", 20), width=15, fg="blue", command=lambda: master.switch_frame(SearchCourse))
        button.grid(row=5)
        tk.Label(root, text='\n\niTeam is the one, Together we learn', bg='#90CAF9',  padx=25, pady=10).grid(row=6)


class AddCourse(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='#90CAF9')

        def add_course(full_name, email_id, contact_number, course_url, language):
            # Use a service account
            res = False
            try:
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
                    unwanted_char = ['/', '?', '.', '=', '-']  # Replaced with Single Space
                    clean_url = course_url
                    for char in ignore_char:
                        clean_url = clean_url.replace(char, '')
                    for char in unwanted_char:
                        clean_url = clean_url.replace(char, ' ')
                    return clean_url

                clean_url = url_cleaner(course_url)
                tags = clean_url.split(' ')

                doc_ref.collection(u'course_url').document(clean_url).set(
                    {u'course_url': course_url})  # updating in users_db

                doc_ref = db.collection(u'urls_db').document(clean_url)
                doc_ref.set({
                    u'course_url': course_url,
                    u'tags': tags
                })
                doc_ref.collection(u'students_email').document(email_id).set({u'email_id': email_id})
                res = True
            except:
                res = False
            return res

        root = self

        tk.Label(root, text='Full Name', font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=0)
        tk.Label(root, text='Email', font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=1)
        tk.Label(root, text='Contact No.', font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=2)
        tk.Label(root, text='Course URL', font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=3)
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
        choices = ['Hindi', 'English']
        tkvar.set('English')  # set the default option

        popupMenu = tk.OptionMenu(root, tkvar, *choices)
        tk.Label(root, text="Preferred Language", font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=4, column=0)
        popupMenu.grid(row=4, column=1)

        def change_dropdown(*args):
            return tkvar.get()

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)

        full_name, email_id, contact_number, course_url, language = '', '', '', '', ''

        def update(*args):
            global full_name, email_id, contact_number, course_url, language
            full_name, email_id, contact_number, course_url, language = e1.get(), e2.get(), e3.get(), e4.get(), change_dropdown()
            res = add_course(full_name, email_id, contact_number, course_url, language)
            if res:
                popupmsg('Successffully Submitted.')
            else:
                popupmsg('All details are mandatory. Try Again!')

        button = tk.Button(root, text='Submit', font=("Arial", 20), width=15, command=update)
        button.grid(row=7, column=1, padx=30, pady=10)

        button = tk.Button(root, text='Back to Main Menu', width=15, command=lambda: master.switch_frame(HomePage))
        button.grid(row=8, column=1, padx=30, pady=10)


class SearchLearners(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='#90CAF9')

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

        root = self
        # Create a Tkinter variable
        tkvar = tk.StringVar(root)

        def change_dropdown(*args):
            return tkvar.get()

        def update(*args):
            global course_url, language, learners_details, clicked_url
            learners_details = list()
            # print('clicked')
            course_url, language = e1.get(), change_dropdown()
            find_learners(course_url, language)
            results = ''
            tk.Label(root, text='Search Results').grid(row=4, padx=10)
            tk.Label(root, text='Full Name', font=LARGE_FONT, bg='#90CAF9', fg='#263238').grid(row=5, column=0, padx=5, pady=5)
            tk.Label(root, text='Contact Number', font=LARGE_FONT, bg='#90CAF9', fg='#263238').grid(row=5, column=1, padx=5, pady=5)
            tk.Label(root, text='Email ID', font=LARGE_FONT, bg='#90CAF9', fg='#263238').grid(row=5, column=2, padx=5, pady=5)
            tk.Label(root, text='Language', font=LARGE_FONT, bg='#90CAF9', fg='#263238').grid(row=5, column=3, padx=5, pady=5)
            for idx, learner in enumerate(learners_details):
                # results = results + '\n' + learner['full_name'] + '\t' + learner['contact_number'] + '\t' + learner['email_id'] + '\t' + learner['language']
                # print(results)
                # tk.Label(root, text=learner['full_name'].ljust(10)  + '\t\t' + learner['contact_number'].ljust(10)  + '\t\t' + learner[
                #     'email_id'].ljust(10) + '\t\t' + learner['language'].ljust(10) ).grid(row=6+idx, padx=5, pady=5)
                tk.Label(root, text=learner['full_name'], bg='#90CAF9', fg='#1A237E').grid(row=6+idx, column=0, padx=5, pady=5)
                tk.Label(root, text=learner['contact_number'], bg='#90CAF9', fg='#1A237E').grid(row=6+idx, column=1, padx=5, pady=5)
                tk.Label(root, text=learner['email_id'], bg='#90CAF9', fg='#1A237E').grid(row=6+idx, column=2, padx=5, pady=5)
                tk.Label(root, text=learner['language'], bg='#90CAF9', fg='#1A237E').grid(row=6+idx, column=3, padx=5, pady=5)
            clicked_url = ''

        tk.Label(root, text='Course URL', font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=0)
        v = tk.StringVar(root, value=clicked_url)
        e1 = tk.Entry(root, textvariable=v)
        if len(clicked_url)>0:
            update()
        e1.grid(row=0, column=1)

        # Location Drop Down

        # Dictionary with options
        choices = ['Hindi', 'English']
        tkvar.set('English')  # set the default option

        popupMenu = tk.OptionMenu(root, tkvar, *choices)
        tk.Label(root, text="Preferred Language", font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=1, column=0)
        popupMenu.grid(row=1, column=1)

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)

        course_url, language = '', ''

        button = tk.Button(root, text='Find Learners', font=("Arial", 20), width=15, command=update)
        button.grid(row=2, column=1, padx=30, pady=10)

        button = tk.Button(root, text='Refresh', width=10, command=lambda: master.switch_frame(SearchLearners))
        button.grid(row=2, column=0, padx=30, pady=10)

        button = tk.Button(root, text='Back to Main Menu', width=15, command=lambda: master.switch_frame(HomePage))
        button.grid(row=3, column=1, padx=30, pady=10)


class SearchCourse(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='#90CAF9')

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
            # print(tags_list)
            docs = db.collection(u'urls_db').where(u'tags', u'array_contains_any', tags_list).stream()

            for doc in docs:
                course_urls.append(db.collection(u'urls_db').document(doc.id).get().to_dict()['course_url'])
            # print(course_urls)
            return course_urls

        root = self

        tk.Label(root, text='Enter TAGs (Space Seprated)', font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=0)
        e1 = tk.Entry(root)
        e1.grid(row=0, column=1)

        def search_course(*args):
            tags = url_cleaner(e1.get())
            tags_list = tags.split(' ')
            courses = find_courses(tags_list)
            # tk.Label(root, text='URLs').grid(row=5, padx=25, pady=10)
            results=''
            for idx, course in enumerate(courses):
                # results = results + '\n' + course
                # tk.Label(root, text=str(idx+1)+'.').grid(row=6+idx, column='0')
                label = tk.Label(root, text='  '+str(idx+1)+'.\t'+course[:60]+'... ', width=55, anchor='w')
                label.grid(row=6+idx, column='0')
                label.bind("<Button-1>", lambda e, url=course: open_url(url))
                def click_helper(url):
                    global clicked_url
                    clicked_url = url
                    master.switch_frame(SearchLearners)
                button = tk.Button(root, text='View Learners', width=15,command=lambda: click_helper(course))
                button.grid(row=6+idx, column=1, padx=30, pady=10)

        button = tk.Button(root, text='Search Course', font=("Arial", 20), width=15, command=search_course)
        button.grid(row=2, column=1, padx=30, pady=10)

        tk.Label(root, text='Search Results', font=LARGE_FONT, bg='#90CAF9',  padx=25, pady=10).grid(row=3)

        button = tk.Button(root, text='Back to Main Menu', width=15, command=lambda: master.switch_frame(HomePage))
        button.grid(row=4, column=1, padx=30, pady=10)


if __name__ == "__main__":
    app = SampleApp()
    app.wm_title('iTeam')
    app.minsize(300, 380)
    app.configure(bg='#90CAF9')
    center(app)
    app.mainloop()