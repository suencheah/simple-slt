for main.py (BACKEND)

python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn tensorflow tensorflow-hub python-multipart opencv-python
uvicorn main:app --reload
---------------------------------
for html (FRONTEND)

- open the folder contianing the frontend code in terminal

python -m http.server 5500
---------------------------------

go to http://localhost:5500/sign_language_speech.html to play with the thing
