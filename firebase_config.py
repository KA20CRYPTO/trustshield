import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBB0Gu7rrzIn8Aj1kcnaMykQoly9jqfKXg",
    "authDomain": "trustield-ai.firebaseapp.com",
    "projectId": "trustield-ai",
    "storageBucket": "trustield-ai.firebasestorage.app",
    "messagingSenderId": "694387029780",
    "appId": "1:694387029780:web:131f2bc3dec01fc7f23401",
    "measurementId": "G-CZFNDVK8MZ",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

