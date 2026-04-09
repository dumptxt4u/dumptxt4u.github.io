from flask import Flask, render_template, jsonify, request, send_file, send_from_directory
import csv
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/covers'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CSV_FILE = 'library_books.csv'

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Author', 'Shelf', 'Subject', 'Topics',
                           'Type', 'Extra Fields', 'OCR Content', 'Cover', 'Status', 'Last Updated'])

def read_books():
    books = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['Extra Fields'] = json.loads(row.get('Extra Fields', '{}')) if row.get('Extra Fields') else {}
                row['OCR Content'] = row.get('OCR Content', '')
                row['Cover'] = row.get('Cover', '')
                books.append(row)
    return books

def write_books(books):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['ID','Title','Author','Shelf','Subject','Topics',
                                               'Type','Extra Fields','OCR Content','Cover','Status','Last Updated'])
        writer.writeheader()
        for book in books:
            book_copy = book.copy()
            book_copy['Extra Fields'] = json.dumps(book_copy.get('Extra Fields', {}))
            writer.writerow(book_copy)

init_csv()

@app.route('/covers/<filename>')
def get_cover(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(read_books())

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.form
    books = read_books()
    
    cover_filename = ''
    if 'cover' in request.files:
        file = request.files['cover']
        if file.filename:
            cover_filename = f"{uuid.uuid4().hex}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))

    new_book = {
        'ID': str(len(books) + 1),
        'Title': data.get('title'),
        'Author': data.get('author'),
        'Shelf': data.get('shelf', 'Unknown'),
        'Subject': data.get('subject', 'General'),
        'Topics': data.get('topics', ''),
        'Type': data.get('type', 'Text'),
        'Extra Fields': json.loads(data.get('extra_fields', '{}')),
        'OCR Content': data.get('ocr_content', ''),
        'Cover': cover_filename,
        'Status': data.get('status', 'On Shelf'),
        'Last Updated': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    books.insert(0, new_book)
    write_books(books)
    return jsonify({"message": "Book added successfully"})

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    # Similar logic as before (kept short)
    data = request.form
    books = read_books()
    for book in books:
        if int(book['ID']) == book_id:
            if 'cover' in request.files and request.files['cover'].filename:
                file = request.files['cover']
                if book.get('Cover'):
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], book['Cover'])
                    if os.path.exists(old_path): os.remove(old_path)
                cover_filename = f"{uuid.uuid4().hex}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
                book['Cover'] = cover_filename

            book.update({
                'Title': data.get('title', book['Title']),
                'Author': data.get('author', book['Author']),
                'Shelf': data.get('shelf', book['Shelf']),
                'Subject': data.get('subject', book['Subject']),
                'Topics': data.get('topics', book['Topics']),
                'Type': data.get('type', book['Type']),
                'Extra Fields': json.loads(data.get('extra_fields', '{}')),
                'OCR Content': data.get('ocr_content', book.get('OCR Content', '')),
                'Status': data.get('status', book['Status']),
                'Last Updated': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            write_books(books)
            return jsonify({"message": "Book updated"})
    return jsonify({"error": "Book not found"}), 404

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = read_books()
    book_to_delete = next((b for b in books if int(b['ID']) == book_id), None)
    if book_to_delete and book_to_delete.get('Cover'):
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], book_to_delete['Cover'])
        if os.path.exists(old_path):
            os.remove(old_path)
    
    books = [b for b in books if int(b['ID']) != book_id]
    for i, b in enumerate(books):
        b['ID'] = str(i + 1)
    write_books(books)
    return jsonify({"message": "Book deleted"})

@app.route('/api/books/<int:book_id>/toggle', methods=['PUT'])
def toggle_shelf(book_id):
    books = read_books()
    for book in books:
        if int(book['ID']) == book_id:
            book['Status'] = 'Off Shelf' if book['Status'] == 'On Shelf' else 'On Shelf'
            book['Last Updated'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            write_books(books)
            return jsonify({"message": "Status toggled", "status": book['Status']})
    return jsonify({"error": "Book not found"}), 404

@app.route('/api/export', methods=['GET'])
def export_csv():
    return send_file(CSV_FILE, as_attachment=True, download_name='library_books.csv')

@app.route('/api/import', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    file.save(CSV_FILE)
    return jsonify({"message": "CSV imported successfully"})

if __name__ == '__main__':
    print("="*60)
    print("🚀 BookShelf App Started Successfully!")
    print("="*60)
    app.run(host='0.0.0.0', debug=True, port=5005)
