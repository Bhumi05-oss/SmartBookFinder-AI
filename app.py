from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock Databases
books = [{"id": 1, "name": "Sapiens", "author": "Yuval Noah Harari"}]
students = [{"id": 1, "name": "Bhumi", "roll": "321", "status": "Not Issued"}]
records = []
# Mock database for fines
fines = [
    {"id": 1, "student_name": "Bhumi", "book": "Sapiens", "amount": "50", "status": "Unpaid"},
    {"id": 2, "student_name": "Rahul", "book": "Physics Vol 1", "amount": "20", "status": "Paid"}
]

@app.route('/fines')
def fine_details():
    return render_template('fines.html', fines=fines)

@app.route('/pay_fine/<int:fine_id>')
def pay_fine(fine_id):
    for f in fines:
        if f['id'] == fine_id:
            f['status'] = "Paid"
    return redirect(url_for('fine_details'))

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    if request.method == 'POST':
        name = request.form.get('book_name')
        author = request.form.get('author')
        books.append({"id": len(books)+1, "name": name, "author": author})
    return render_template('books.html', books=books)



@app.route('/ai', methods=['GET', 'POST'])
def ai_features():
    recommendations = []
    summary_points = [] # Initialize as an empty list
    
    if request.method == 'POST':
        if 'recommend' in request.form:
            interest = request.form.get('interest', '').lower()
            if "history" in interest or "science" in interest:
                recommendations = ["Sapiens", "Guns, Germs, and Steel", "The Silk Roads"]
            else:
                recommendations = ["The Alchemist", "Atomic Habits"]
                
        if 'summarize' in request.form:
            text = request.form.get('text_to_summarize', '')
            
            # 1. Split the paragraph into sentences using the period
            # 2. Filter out any empty spaces or very short strings
            all_sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 5]
            
            # 3. Take only the first 3 sentences (or fewer if the text is short)
            summary_points = all_sentences[:3]
        
    return render_template('recommendations.html', recs=recommendations, summary=summary_points)

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    global books
    # Filter out the book with the matching ID
    books = [b for b in books if b['id'] != book_id]
    return redirect(url_for('manage_books'))

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        name = request.form.get('student_name')
        roll = request.form.get('roll')
        # Generate ID based on the last student's ID + 1, or 1 if list is empty
        new_id = students[-1]['id'] + 1 if students else 1
        students.append({"id": new_id, "name": name, "roll": roll, "status": "Not Issued"})
        return redirect(url_for('manage_students'))
    return render_template('students.html', students=students)

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    global students
    # Keep everyone EXCEPT the student with the matching ID
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('manage_students'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)