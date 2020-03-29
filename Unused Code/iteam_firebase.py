import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('iteam-3b0d1-firebase-adminsdk-o179z-d503c5a2a9.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# updating users_db
contact = '9456908427'
email_id = 'subrat.iiit@gmail.com'
name = 'subrat'
language = 'hindi'

doc_ref = db.collection(u'users_db').document(email_id)
doc_ref.set({
    u'contact': contact,
    u'email_id': email_id,
    u'name': name,
    u'language': language
})

# updating urls_db
url = 'https://firebase.google.com/docs/firestore/quickstart?authuser=0'

def url_cleaner(url):
    ignore_char = ['https', 'http', '.com', ':', '//'] # Replaced with Nothing
    unwanted_char = ['/', '?', '.', '='] # Replaced with Single Space
    clean_url = url
    for char in ignore_char:
        clean_url = clean_url.replace(char, '')
    for char in unwanted_char:
        clean_url = clean_url.replace(char, ' ')
    return clean_url

clean_url = url_cleaner(url)
tags = clean_url.split(' ')

doc_ref = db.collection(u'urls_db').document(clean_url)
doc_ref.set({
    u'url': url,
    u'tags': tags
})

doc_ref.collection(u'students_email').add({u'email':'@gmail.com'})