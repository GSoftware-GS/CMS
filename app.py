from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///words.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_phrase = db.Column(db.String(255), nullable=False)
    translation = db.Column(db.String(255), nullable=True)
    example_sentence = db.Column(db.Text, nullable=True)

# Function to load initial JSON data using the provided structure
def load_initial_data():
    url = "https://pecto-content-f2egcwgbcvbkbye6.z03.azurefd.net/language-data/language-data/russian-finnish/cards/curated_platform_cards/sm1_new_kap1.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            count = 0
            for entry in data:
                word_text = entry.get('wordFirstLang', '')
                translation = entry.get('wordSecondLang', '')
                example_sentence = entry.get('sentenceFirstLang', '')
                if word_text and not Word.query.filter_by(word_phrase=word_text).first():
                    new_word = Word(word_phrase=word_text,
                                    translation=translation,
                                    example_sentence=example_sentence)
                    db.session.add(new_word)
                    count += 1
            db.session.commit()
            print(f"Initial data loaded successfully. {count} entries added.")
        else:
            print("Failed to load data. Status code:", response.status_code)
    except Exception as e:
        print("Error loading initial data:", e)


# Create tables and load data on first request
# @app.before_first_request
# def initialize():
#     db.create_all()
#     load_initial_data()

# Route: List and search words/phrases (paginated)
@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    if search_query:
        pagination = Word.query.filter(Word.word_phrase.contains(search_query)).paginate(page=page, per_page=10)
    else:
        pagination = Word.query.paginate(page=page, per_page=10)
    return render_template('index.html', words=pagination, search_query=search_query)

# Route: Edit an entry
@app.route('/edit/<int:word_id>', methods=['GET', 'POST'])
def edit(word_id):
    word_entry = Word.query.get_or_404(word_id)
    if request.method == 'POST':
        word_entry.word_phrase = request.form['word_phrase']
        word_entry.translation = request.form['translation']
        word_entry.example_sentence = request.form['example_sentence']
        db.session.commit()
        flash('Entry updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', word=word_entry)

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_initial_data()
    app.run(debug=True)
