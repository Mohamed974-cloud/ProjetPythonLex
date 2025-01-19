from flask import Blueprint, render_template, request, send_from_directory, send_file
from app import bank_file_checker as check_transaction
main = Blueprint('main', __name__)
main.config = {'UPLOAD_FOLDER': 'uploads/'}
@main.route('/')
def upload_file():
    return render_template('upload.html',result=[])

@main.route('/upload', methods=['POST'])
def upload_transaction_file():
    if 'name' in request.form:
        name = request.form['name']
    if 'file' not in request.files:
        return render_template('upload.html', response="Aucun fichier sélectionné")
    file = request.files['file']
    return render_template('upload.html',result=[ {"result":check_transaction.calculate_balance(file)}, {"name": name}])
    
@main.route('/resultat_transactions.json', methods=['GET'])
def get_resultat_transactions():
    return send_from_directory(directory='.', path='data/resultat_transactions.json')

@main.route('/error_lex.json', methods=['GET'])
def get_success_transactions():
    return send_from_directory(directory='.', path='data/error_lex.json')


@main.route('/history_success_transaction.json', methods=['GET'])
def get_history_success_transactions():
    return send_from_directory(directory='.', path='data/history_success_transaction.json')


@main.route('/history_error_transaction.json', methods=['GET'])
def get_history_error_transactions():
    return send_from_directory(directory='.', path='data/history_error_transaction.json')


@main.route('/success-transaction', methods=['GET'])
def get_success_transaction():
    return render_template('success_transaction.html')

@main.route('/error-transaction', methods=['GET'])
def get_error_transaction():
    return render_template('error_transaction.html')

@main.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_file('Lexer_logo_teal.png')