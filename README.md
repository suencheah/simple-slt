# mmtcybai team's solution for FutureHack 2025!

### Go to: [Our Github Pages](https://suencheah.github.io/simple-slt/) to test out the deployed version!


# To reproduce in your local machine:

### 1. Clone the repo

### 2. HOST the backend:

in the terminal, run: 
```
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn tensorflow tensorflow-hub python-multipart opencv-python
uvicorn main:app --reload
```

### 3. HOST the frontend (index.html)
Navigate to the folder containing the index.html file in terminal

run:
`python -m http.server 5500`

then on your local browser, 
go to http://localhost:5500/index.html to play with the SLT tool!
