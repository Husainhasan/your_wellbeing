from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db = SQLAlchemy(app)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    def __repr__(self):
        return self.id


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        journal_content = request.form['content']
        new_entry = Entry(content=journal_content)

        db.session.add(new_entry)
        db.session.commit()
        return redirect('/')

    else:
        entries = Entry.query.order_by(Entry.date).all()

        return render_template('index.html', entries = entries)


@app.route('/delete/<int:id>')
def delete(id):
    entry_to_delete = Entry.query.get_or_404(id)

    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect('/')

 
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    entry = Entry.query.get(id)

    if request.method == "POST":
        entry.content = request.form['content']
        new_entry = Entry(content=entry.content)

        db.session.commit()
        return redirect('/')

    else:
        return render_template('update.html', entry = entry)


if __name__ == "__main__":
    app.run(debug = True)
