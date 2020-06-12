import json
import sys
import os
import sqlite3

if len(sys.argv) != 2:
    raise Exception("Invalid arguments. Missing Telegramp json dump filename")

def mkdir(chat_id):
    path = 'dataset/' + str(chat_id)
    try:
        os.mkdir(path)
    except Exception as e:
        print('Cannot create dir ' + path + '. Maybe it already exists?', e)

def write_msg(chat_id, from_id, text):
    path = 'dataset/' + str(chat_id) + '/' + str(from_id) + '.txt'
    with open(path, 'a+') as outfile:
        outfile.write(text + '\n')

def flatten_msg(text):
    if isinstance(text, str):
        return text.strip()
    else:
        chunks = list(filter(lambda t: len(t.strip()) > 0, 
            [msg.strip() if isinstance(msg, str) else msg['text'] for msg in text]))
        return ' '.join(chunks).strip()

try:
    db = sqlite3.connect('refs.db')
    create_table = '''
    CREATE TABLE IF NOT EXISTS chat_refs (
        source_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        bot_id INTEGER UNIQUE
    );
    '''
    insert = "INSERT INTO chat_refs (source_id, name) VALUES ('{source_id}', '{name}')"
    cursor = db.cursor()
    cursor.execute(create_table)

    with open(sys.argv[1]) as dump:
        data = json.load(dump)
        for chat in data['chats']['list']:
            chat_id = chat['id']
            chat_name = chat['name']
            cursor.execute(insert.format(source_id = chat_id, name = chat_name))
            mkdir(chat_id)
            print('Scraping chat', chat_name)
            for msg in chat['messages']:
                text = flatten_msg(msg['text'])
                if msg['type'] == 'message' and len(text) > 0 and text[0] != '/':
                    print('Writing message ', msg['id'], ' from ', msg['from'], ' in ', chat_name)
                    write_msg(chat_id, msg['from_id'], text)
            print('Chat ', chat_name, ' complete!')    

    db.commit()
    cursor.close()
except Exception as e:
    print("Something went wrong. ", e)
finally:
    if db:
        db.close()

