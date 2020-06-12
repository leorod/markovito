from os import path
import sqlite3

def fetch_refs():
    refs = []
    db = sqlite3.connect('refs.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM chat_refs')
    records = cursor.fetchall()
    for row in records:
        refs.append({
            'source_id': row[0],
            'name': row[1],
            'bot_id': row[2]
        })
    cursor.close()
    db.close()
    return refs

def update_ref(bot_id, source_id):
    db = sqlite3.connect('refs.db')
    cursor = db.cursor()
    sql = "UPDATE chat_refs SET bot_id={bot_id} where source_id={source_id}"
    cursor.execute(sql.format(bot_id = bot_id, source_id = source_id))
    db.commit()
    cursor.close()
    db.close()

class ChatResolver:
    def __init__(self):
        self.ref_cache = {}
        self.all_refs = fetch_refs()
        for ref in self.all_refs:
            if ref['bot_id']:
                self.ref_cache[ref['bot_id']] = ref['source_id']
    
    def get_chat_id(self, bot_id, chat_name):
        if bot_id in self.ref_cache:
            return self.ref_cache[bot_id]
        else:
            source_id = next(filter(lambda ref: ref['name'] == chat_name, self.all_refs))['source_id']
            self.ref_cache[bot_id] = source_id
            update_ref(bot_id, source_id)
            return source_id