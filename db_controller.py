import sqlite3
from conf import members
import random

class DataBase:
    def __init__(self, dbname: str):
        self.connection = sqlite3.connect(dbname,
                                          check_same_thread=False)
        
    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS members(id int, name text, have_pair bool, santa_id int default 0)')
        cursor.execute('CREATE TABLE IF NOT EXISTS chat(id int)')
        for i in members:
            i = (members.index(i)+1, i, False)
            cursor.execute(f'INSERT INTO members(id, name, have_pair) VALUES (?, ?, ?)', i)
        self.connection.commit()
        cursor.close()

    def get_members_list(self):
        cursor = self.connection.cursor()
        db_list = cursor.execute('SELECT id, name FROM members')
        msg = 'Номер участника | Имя \n\n'+'\n'.join(['. '.join(map(str, i)) for i in db_list])
        cursor.close()
        return msg
    
    def assign_a_couple(self, player: int, chat_id: int):
        cursor = self.connection.cursor()
        members = cursor.execute(f'SELECT * FROM members WHERE have_pair = false AND id!={player}').fetchall()
        if members:
            pair_for_player = random.choice(members)
            cursor.execute(f'UPDATE members SET have_pair = true, santa_id = {player} WHERE id={pair_for_player[0]}')
            cursor.execute(f'INSERT INTO chat(id) VALUES ({chat_id})')
            self.connection.commit()
            cursor.close()
            return pair_for_player[1]
        else:
            print('***ВСЕ ПАРЫ СОБРАНЫ, ВЫКЛЮЧИ МЕНЯ <3***')
            
    def cheque_chat(self, chat_id: int) -> bool:
        cursor = self.connection.cursor()
        chat = cursor.execute(f'SELECT * FROM chat where id={chat_id}').fetchone()
        cursor.close()
        if chat:
            return True
        return False
            
    def read_tables(self):
        cursor = self.connection.cursor()
        table1 = cursor.execute('SELECT * FROM members').fetchall()
        table2 = cursor.execute('SELECT * FROM chat').fetchall()
        print('*'*10)
        print(table1)
        print('*'*10)
        print(table2)
        print('*'*10)
        cursor.close()
        return table1, table2
    
    def get_santas(self):
        cursor = self.connection.cursor()
        members = cursor.execute('SELECT * FROM members').fetchall()
        santas = list()
        for member in members:
            santa = cursor.execute(f'SELECT name from members WHERE id={member[3]}').fetchone()
            if santa:
                santas.append(f'{santa[0]} дарит подарок для {member[1]}')
        cursor.close()
        msg = ''.join('\n'.join(i for i in santas))
        return msg
