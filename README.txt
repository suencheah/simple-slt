To reproduce in your local machine:

1. clone the repo

2. HOST the backend:

python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn tensorflow tensorflow-hub python-multipart opencv-python
uvicorn main:app --reload

3. HOST the frontend (index.html)

- navigate to the folder containing the index.html file in terminal

run:
python -m http.server 5500

go to http://localhost:5500/index.html to play with the SLT tool!
