from flask import Flask, render_template, request, redirect, url_for
from models import Article, Comment
from db import get_session
app = Flask(__name__)
app.secret_key = 'blog'


@app.route('/')
def index():
    with get_session() as session:
        articles = session.query(Article).all()
        return render_template('index.html', articles=articles)

@app.route('/create_article', methods=['POST'])
def create_article():
    with get_session() as session:
            title = request.form['title']
            content = request.form['content']
            article = Article(title=title, content=content)
            session.add(article)
            session.commit()
            return redirect(url_for('index'))

@app.route('/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    with get_session() as session:
        article = session.query(Article).filter_by(id=article_id).first()
        session.delete(article)
        session.commit()
        return redirect(url_for('index'))

@app.route('/update/<int:article_id>', methods=['POST'])
def update_article(article_id):
    with get_session() as session:
        title = request.form['title']
        content = request.form['content']
        article = session.query(Article).filter_by(id=article_id).first()
        article.title = title
        article.content = content
        session.commit()
        return redirect(url_for('index', article_id=article_id))

@app.route('/editing/<int:article_id>', methods=['GET','POST'])
def editing(article_id):
    with get_session() as session:
        article = session.query(Article).get(article_id)
        return render_template('editing.html', article=article)
@app.route('/articles/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    with get_session() as session:
        if request.method == 'GET':
            article = session.query(Article).filter_by(id=article_id).first()
            comments = session.query(Comment).filter_by(article_id=article_id).order_by(Comment.created_at.desc()).all()
            return render_template('article.html', article=article, comments=comments)
        if request.method == 'POST':
            author_name = request.form.get('author_name')
            content = request.form.get('content')
            if author_name and content:
                new_comment = Comment(article_id=article_id, content=content, author_name=author_name)
                session.add(new_comment)
                session.commit()
                return redirect(url_for('article', article_id=article_id))


if __name__ == '__main__':
    app.run(debug=True)