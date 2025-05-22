from colorama import Fore, Back, Style
from tqdm import tqdm
from datetime import datetime
import colorama
colorama.init()
from requests import session
session = session()
import json
import sys
from dic import Theman
from Server import getAllUsers
basic_url = "http://127.0.0.1:5000"
def Login():
    while True:
        try:
            # הכנסה של שם כולל צביעה
            print(Fore.BLUE + "Enter your name: " + Style.RESET_ALL)
            name = input()
            # בדיקה שהכל אותיות
            if not name.isalpha():
                raise ValueError("Error: Name must contain only letters. Please enter a valid name.")
           # קליטת קוד
            print(Fore.BLUE + "Enter your password: " + Style.RESET_ALL)
            password = input()
            # שליחה לפונקציה בשרת שבודקת האם קיים עוגיה עם שם וסיסמא אלו
            obj = {'name': name, "password": password}
            response = session.post(f"{basic_url}/login", json=obj)
            # אם קיים נעבור למשחק
            if response.status_code == 200:
                print(response.text)
                start(password)
            else:
                print(f"Login failed with status code: {response.status_code}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Unexpected error: {e}")
# @isConnected
def start(password):
    number =value()
    obj = {'number': number}
    # שליחה של המספר לפונקציה ששולפת את המילה
    response = session.post(f"{basic_url}/getWord", json=obj)
    # אם הבקשה הצליחה
    if response.status_code == 200:
        # נשמור את המילה שהוגרלה
        theWord = response.text
        print(theWord)
        # ניצור מיקומים באורך המילה שהוגרלה
        str = '_' * len(theWord)
        print(Fore.BLUE + str + Style.RESET_ALL)
        p = 0  # שומר את מספר השגיאה
        x = 0  # צריך להחליף למשתנה יפה בוליאני
        theSignal=[] #שומר את התוים שהשחקן השתמש כבר
        # המשחק כל עוד לא היו 7 שגיאות או המילה עוד לא הושלמה
        while p < 7 and x == 0:
          # בכל שלב נבדוק האם העוגיה עדיים בתוקף
           if  session.post(f"{basic_url}/check_cookie").status_code == 404:
              # אם הסתיימה נשלח לפונקציה שתבדוק האם מעונין בהמשך משחק
                print("Your number was not put in.....")
                r = play_again(password)
                if r == 'no':  # אם מעונין לצאת
                    sys.exit()
           while True:
               signal = input("Enter a signal: ")  # קליטה של אות לנסיון
               # בדיקה האם לא השתמשנו באות זו
               if signal.lower() in theSignal or signal.upper() in theSignal:
                   print(Fore.RED + "You have already played this letter! Choose another letter!!" + Style.RESET_ALL)
               else: # אות חדשה-נכניס למערך
                   theSignal.append(signal)
                   break
          # יצירה של מערך של מיקומים שהאות מופיעה
           indices = [i for i in range(len(theWord)) if theWord[i] == signal.upper() or theWord[i]==signal.lower()]
           if not indices:# הכניס אות שגויה
               print(Theman[p]) #נדפיס את השלב בעץ
               p += 1# נקדם את המונה של הטעיויות
           else:
               for index in indices:# נעבור על מערך המיקומים
                   str = str[:index] + theWord[index] + str[index + 1:]#נחליף את התו
                   print( Fore.BLUE + str + Style.RESET_ALL) # נדפיס את המילה המעודכנת
               if '_' not in str:# המילה גמורה
                   x = 1;#נצא מהלולאה
        if p == 7:# יציאה בגלל מספר כשלונות
            print("Too bad you tried too many times 🥲")
            sys.exit()
        elif x == 1:#יציאה בגלל ניצחון
            obj={"word":theWord,"password":password}#נשלח לבדיקה האם העוגיה עדיין קימת
            if session.post(f"{basic_url}/win",json=obj).status_code ==401:
                #אם לא נשלח לפונקציה שמטפלת בהמשך משחק
                print(Fore.RED + "Your number was not put in....." + Style.RESET_ALL)
                r = play_again()
                if r == 'no':
                    sys.exit()
            else:
                #נדפיס הודעה מתאימה
                print(Fore.RED + "You did it!!!!!😋🤣😍" + Style.RESET_ALL)
                print(end(password))# נשלח לפונקצית סיום
                sys.exit()
    else:
        print(response.status_code)
def play_again(password):
    while True:
        qu = input("Do you want to join again? (yes/no) ").lower()
        if qu == 'yes':
            start(password)
            return
        elif qu == 'no':
            return 'no'
        else:
            print(Fore.RED + "The input you provided is not valid. Please enter 'yes' or 'no'." + Style.RESET_ALL)
def end(password):
    while True:
        try:
            numOptain = int(input("""Choose one of the following options:
              If you want to continue playing press 1,
              If you want to see your game history - press 2,
              To exit press 3  """))
            if numOptain == 1:
               start(password)# אם רוצה להמשיך לשחק נשלח לפונקצית התחלה
            elif numOptain == 2:#נחפש את השחקן ונחזיר את רשימת המילים שלו
                user = next((player for player in getAllUsers() if player['password'] == password), None)
                if user:
                    return user['word']
            elif numOptain == 3:#נצא
              sys.exit()
            else:#בדיקת תקינות האם הקלט 1,2,3
             print("Please enter a valid option: 1, 2, or 3.")
        except ValueError as er:
            print(f"Error! Invalid input: {er}. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def value():
    while True:
        try:
            return int(input("input a num"))
        except ValueError:
            print("Please enter a vailed number")
if __name__ == '__main__':
    Login()



