import json
import time


class User:
    def __init__(self, name, password, timeU=None, numberU=None, numPlay=0, word=None, numWin=0):
        self.name = name
        self.numberU = numberU
        self.password = password
        self.numPlay = numPlay
        self.word = word if word else []
        self.numWin = numWin
        self.timeU = timeU # הוספת מאפיין זמן התחברות
    def to_dict(self):
        return {
            'name': self.name,
            'numberU': self.numberU,
            'password': self.password,
            'numPlay': self.numPlay,
            "word":self.word,
            # 'word': list(self.word),  # המרה מ-set ל-list
            'numWin': self.numWin,
            'timeU': self.timeU  # הוספת זמן התחברות

        }



def __str__(self):
    # החזרת מיתאר של השחקן בצורה קריאה
    return (f"name: {self.name}\n"
            f"numberU: {self.numberU}\n"
            f"password: {self.password}\n"
            f"numPlay: {self.numPlay}\n"
            f"word: {', '.join(self.word)}\n"
            f"timeU: {self.timeU}\n"
            f"numWin: {self.numWin}"
            )
