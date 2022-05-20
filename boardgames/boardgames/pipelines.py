# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class BoardgamesPipeline:
    def __init__(self):
        self.con = sqlite3.connect('boardgames.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS games(
        rank REAL PRIMARY KEY,
        name VARCHAR(100),
        url VARCHAR(255),
        rating FLOAT
        )""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO games VALUES (?,?,?,?)""",
                         (item['rank'], item['name'], item['url'], item['rating']))
        self.con.commit()
        return item
