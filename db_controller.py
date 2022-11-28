import sqlite3
from conf import members
import random

class DataBase:
    def __init__(self, dbname: str):
        self.connection = sqlite3.connect(dbname,
                                          check_same_thread=False)
        
    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS members(id int, name text, have_pair bool)')
        for i in members:
            i = (members.index(i)+1, i, False)
            cursor.execute(f'INSERT INTO members(id, name, have_pair) VALUES (?, ?, ?)', i)
        self.connection.commit() #У меня не завелось без этого. Наверное, надо везде такое)

    def get_members_list(self):
        cursor = self.connection.cursor()
        db_list = cursor.execute('SELECT id, name FROM members where have_pair = false')
        return 'Номер участника | Имя \n\n'+'\n'.join(['. '.join(map(str, i)) for i in db_list])
    
    def assign_a_couple(self, player: int):
        cursor = self.connection.cursor()
        members = cursor.execute(f'SELECT * FROM members WHERE have_pair = false AND id!={player}').fetchall()
        if members:
            pair_for_player = random.choice(members)
            cursor.execute(f'UPDATE members SET have_pair = true WHERE id={pair_for_player[0]}')
            return pair_for_player[1]
        else:
            print('***ВСЕ ПАРЫ СОБРАНЫ, ВЫКЛЮЧИ МЕНЯ <3***')
