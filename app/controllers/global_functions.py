from datetime import datetime
import re


class GlobalFunctions:
    def current_datetime(self):
        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return current_datetime

    def clean_text(self, text):
        text = text.replace('"', '')
        text = text.replace("'", '')
        text = re.sub(' +', ' ', text)
        text = re.sub('\n+', ' ', text)
        text = text.strip()
        text = text.strip('\n')
        return text

    def dict_to_insert_query(self, table, dictionary):
        sql = "INSERT INTO %s (%s) VALUES('%s')" % (
            table, ",".join(list(dictionary.keys())), "','".join(list(dictionary.values())))
        return sql
