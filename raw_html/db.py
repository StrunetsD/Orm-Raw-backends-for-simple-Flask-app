from const import DB_CONNECTION
from db_conn import DBConnect

db  = DBConnect(**DB_CONNECTION)

def get_all_articles():
    connection = db.get_connection()
    with connection.cursor() as cur:
        cur.execute('''
            SELECT id, title, content, created_at FROM articles
            ORDER BY created_at DESC
        ''')
        results = cur.fetchall()
        return results if results else []

def get_comments_for_article(__cur, article_id):
    with db.get_connection().cursor() as __cur:
        __cur.execute( '''
            SELECT * 
            FROM comments 
            WHERE article_id = %s
            ORDER BY created_at ASC;
            ''',
         (article_id,))
    return __cur.fetchall()

def add_article( title, content):
    connection = db.get_connection()
    with connection.cursor() as __cur:
        __cur.execute('''
            INSERT INTO articles (title, content, created_at, updated_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (title, content, ))

def delete_article(id):
    connection = db.get_connection()
    with connection.cursor() as cur:
        cur.execute(''' 
        DELETE FROM articles
        WHERE id= %s
        ''', (id,))

def add_comment(article_id, content, author_name):
    connection = db.get_connection()
    with connection.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO comments (article_id, content, author_name)
            VALUES (%s, %s, %s)
            ''',
            (article_id, content, author_name)
        )

def get_article_by_id(article_id):
    connection = db.get_connection()
    with connection.cursor() as cur:
        cur.execute('''SELECT id, title, content, created_at FROM articles WHERE id = %s''', (article_id,))
        return cur.fetchone()

def get_comments_by_article_id(article_id):
    connection = db.get_connection()
    with connection.cursor() as cur:
        cur.execute('''
                    SELECT id, author_name, content, created_at FROM comments 
                    WHERE article_id = %s ORDER BY created_at DESC
                    ''',(article_id,))
        return cur.fetchall()

def update_article(article_id, title, content):
    connection = db.get_connection()
    with connection.cursor() as cur:
        cur.execute('''
        UPDATE articles 
        SET title = %s, content = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        ''', (title, content, article_id))



