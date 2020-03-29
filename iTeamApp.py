import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('iteam-3b0d1-firebase-adminsdk-o179z-d503c5a2a9.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

try:
    import Tkinter as tk
except:
    import tkinter as tk


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
        tk.Label(root, text='\nThis allow you to list your course\n(which allowes to be discovered by other learners)').grid(row=0)
        button = tk.Button(root, text='Add Course', width=25, command=lambda: master.switch_frame(AddCourse))
        button.grid(row=1)

        tk.Label(root,
                 text='\nThis allow you to list your course\n(which allowes to be discovered by other learners)').grid(
            row=2)
        button = tk.Button(root, text='Search Learners', width=25, command=lambda: master.switch_frame(SearchLearners))
        button.grid(row=3)

        tk.Label(root,
                 text='\nThis allow you to list your course\n(which allowes to be discovered by other learners)').grid(
            row=4)
        button = tk.Button(root, text='Search Course', width=25, command=lambda: master.switch_frame(SearchCourse))
        button.grid(row=5)
        # tk.Button(self, text="Go to page one",
        #           command=lambda: master.switch_frame(PageOne)).pack()
        # tk.Button(self, text="Go to page two",
        #           command=lambda: master.switch_frame(PageTwo)).pack()


class AddCourse(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='blue')

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

        root = self

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
        choices = ['Hindi', 'English']
        tkvar.set('English')  # set the default option

        popupMenu = tk.OptionMenu(root, tkvar, *choices)
        tk.Label(root, text="Preferred Language").grid(row=4, column=0)
        popupMenu.grid(row=4, column=1)

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

        button = tk.Button(root, text='Back to Main Menu', width=25, command=lambda: master.switch_frame(HomePage))
        button.grid(row=8, column=1)
        # tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        # tk.Button(self, text="Go back to start page",
        #           command=lambda: master.switch_frame(StartPage)).pack()


class SearchLearners(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='red')

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

        button = tk.Button(root, text='Back to Main Menu', width=25, command=lambda: master.switch_frame(HomePage))
        button.grid(row=6, column=1)
        # tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        # tk.Button(self, text="Go back to start page",
        #           command=lambda: master.switch_frame(StartPage)).pack()


class SearchCourse(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='red')

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

        root = self

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

        button = tk.Button(root, text='Back to Main Menu', width=25, command=lambda: master.switch_frame(HomePage))
        button.grid(row=6, column=1)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()