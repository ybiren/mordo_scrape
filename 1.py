import requests
from bs4 import BeautifulSoup
import psycopg2
import re

def insert_quest(url,quest,ans):
    sql = """INSERT INTO tbldata(url,quest,ans) VALUES(%s,%s,%s) """
    print("AAAA")
    print(quest)  
    try:
        pg_conn = psycopg2.connect(
        host="192.168.1.140",
        database="mordo",
        user="postgres",
        password="a1b2c3d5")

        # create a new cursor
        cur = pg_conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (url,quest,ans))
        # get the generated id back
        # commit the changes to the database
        pg_conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if pg_conn is not None:
            pg_conn.close()


for num in range(1, 2000):
  url = f'https://pitaronfree.blogspot.com/2014/10/blog-post_{num}.html'
  page = requests.get(url)  
  soup = BeautifulSoup(page.content, "html.parser")
  result = soup.find(class_="post-title")
  if(result != None):
    quest = result.text.strip()
    if "|" in quest:
      quest = quest.split("|")[0];    
    ansArr = []
        
    # answers = soup.find_all("span", style=re.compile("font-family: Georgia, Times New Roman, serif;"))
    answers = soup.find_all("b")
    for ans in answers:
      #if "פתרון" in ans.text and "אותיות" in ans.text:
        #bs = ans.find_all("b")   
        #for b in bs:
      if quest not in ans.text and  "מורדו" not in ans.text and "מודעות" not in ans.text and "פתרון" not in ans.text and "אותיות" not in ans.text and "מחפשים תשובות" not in ans.text:
        ansArr.append(ans.text.strip())
    
    #print(quest, url, 'XXXXXXXXX'.join(ansArr))
    insert_quest(url, quest, 'XXXXXXXXX'.join(ansArr))
