from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager

import db

app = Flask(__name__)
app.secret_key = 'blog'

@app.route('/')
def base():
    return render_template(
        'base.html',
    articles = db.get_all_articles()
)


@app.route('/create_article', methods=['POST'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        db.add_article(title, content)
        return redirect(url_for('base'))

@app.route('/articles/<int:article_id>', methods=['GET', 'POST'])
def article(id):
    if request.method == 'GET':
        article = db.get_article_by_id(id)
        comments = db.get_comments_by_article_id(id)
        return redirect(url_for('article'))
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        content = request.form.get('content')
        if author_name and content:
            db.add_comment(id, author_name, content)
            return redirect(url_for('article', article_id=id))

@app.route('/editing/<int:article_id>', methods=['GET'])
def article_edit(article_id):
    article = db.get_article_by_id(article_id)
    return render_template('editing.html', article=article)
@app.route('/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    db.delete_article(article_id)
    flash('article was deleted', 'success')
    return redirect(url_for('base'))


@app.route('/update/<int:article_id>', methods=['POST'])
def article_update(article_id):
    title = request.form['title']
    content = request.form['content']
    db.update_article(article_id, title, content)
    return redirect(url_for('base'))


if __name__ == '__main__':
    app.run(debug=True)
