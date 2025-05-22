import json
import time
from functools import wraps
import random
from flask import Flask, request, jsonify, abort, make_response
from flask_cors import CORS
from user import User
# export FLASK_ENV=development
# flask run
app = Flask(__name__)  # יצירת מופע מהשרת
CORS(app, supports_credentials=True)  # supports_credentials=True- מאפשר עוגיות
users=['']
# decorator is conected:
def isConnected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = request.cookies.get('user')
        if name:
            return func(*args, **kwargs)  # אם יש עוגיה, ממשיך לפונקציה
        else:
            return abort(401)  # מחזיר שגיאת 401 אם אין עוגיה
    return wrapper
@app.route('/getWord',methods=['POST'])
def getWord():
    obj = request.json # פונקציה שמקבלת מספר
    number=obj['number']
    content = ''
    with open('Word.txt', 'r', encoding='utf-8') as file:
        content = file.read().splitlines()
    random.shuffle(content)
    theWord = content[(number%len(content))-1]
    return theWord
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    u = getAllUsers()
    currentPlayer = next((player for player in u if player['name'] == name and player['password'] == password), None)
    if currentPlayer is not None:
     response = make_response(f"Wellcome {name}!!!", 200)
     response.set_cookie("user", name, max_age=600, httponly=True, secure=False, samesite='None')
     return response
    new_user = User(name,password,len(u)+1,time.time())
    try:
        u.append(new_user.to_dict())
        with open('./data.json', 'w') as file:
            json.dump(u, file)
    except Exception as e:
        return make_response(f"Error saving user: {str(e)}", 500)
    response = make_response("Welcome - for your first time!")
    response.set_cookie("user", name, max_age=600, httponly=True, secure=False, samesite='None')
    return response
@app.route('/win',methods=['POST'])
@isConnected
def win():
    # שליפה מהגיסון שהתקבל המילה ששחיקו והסיסמא
    data = request.json
    word = data.get('word')
    password = data.get('password')
    # שליפת כל המשתמשים
    u = getAllUsers()
    # חיפוש השחקן
    player = next((p for p in u if p['password'] == password), None)
    if player:
        # הוספת ניצחון
        player['numWin'] =player['numWin']+1
        # בדיקה ההאם שיחק כבר במילה זו
        if word not in player['word']:
            # הוספה למערך
         player['word'].append(word)
         # נעדכן בקובץ הגיסון
        with open('data.json', 'w') as file:
            json.dump(u, file)
def getAllUsers():
    # פונקציה ששולפת את הנתונים מהגיסון ומחזירה אותם
    try:
        with open('./data.json', 'r') as file:
            u = json.load(file)
    except FileNotFoundError:
        u = []
    except json.JSONDecodeError:
        u = []
    return u
@app.route('/check_cookie', methods=['POST'])
def check_cookie():
    name = request.cookies.get('user')
    if name:
        return jsonify({"cookie_status": "Cookie is present", "user": name})
    else:
        return jsonify({"cookie_status": "Cookie is not present"}), 404
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)




