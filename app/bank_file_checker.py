import ply.lex as lex
from flask import Flask, render_template, request, session
import os
from werkzeug.datastructures import FileStorage
import json

# Liste des tokens
tokens = (
    'SOLDE',
    'CREDIT',
    'DEBIT',
    'COMMENT',
    'SEPARATOR'
)

# Expressions régulières pour les tokens
t_SOLDE = r':\d+,\d{2}'
t_CREDIT = r'\+\d+,\d{2}'
t_DEBIT = r'-\d+,\d{2}'
t_COMMENT = r'\#.*'
t_SEPARATOR = r'[-]{17}'

# Ignorer les espaces et les retours a la ligne
t_ignore = ' \t\n'

def find_column(input_text, token):
    line_start = input_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
     # Calculer la colonne de l'erreur
    column = find_column(t.lexer.lexdata, t)
    
    # Trouver les limites de la ligne contenant l'erreur
    line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
    line_end = t.lexer.lexdata.find('\n', t.lexpos)
    if line_end == -1:  # Si l'erreur est à la dernière ligne
        line_end = len(t.lexer.lexdata)
    
    # Extraire la ligne
    error_line = t.lexer.lexdata[line_start:line_end]
    error = {
    "lineNumber": t.lineno,
    "value": t.value[0],
    "line": error_line.strip(),
    }
    
    # Afficher le message d'erreur avec la ligne et la colonne
    print(f"Erreur lexicale à la ligne {t.lineno}, colonne {column}: {t.value[0]}")
    print(f"Ligne contenant l'erreur : {error_line.strip()}")
    with open('data/history_error_transaction.json', 'r') as error_file:
        history_error = json.load(error_file)
    history_error['data'].append(error)
    with open('data/history_error_transaction.json', 'w') as error_file:
        json.dump(history_error, error_file, indent=4)
    
    with open('data/error_lex.json', 'w') as error_file:
        json.dump(error, error_file, indent=4)
        
    raise Exception(f"Erreur lexicale à la ligne {t.lineno}, colonne {column}: {t.value[0]}")


# Construire le lexer
lexer = lex.lex()



# Fonction pour lire le fichier et calculer le solde
def process_bank_data(filename):
    if isinstance(filename, FileStorage):
        content = filename.read().decode('utf-8')
    else:
        with open(filename, 'r') as f:
            content = f.read()
    lexer.input(content)
    
    balance = 0.0
    transactions = []
    result = {
        "solde_initial": 0.0,
        "transactions": {}
    }
    print("Transactions :")
    transaction_count = 1
    try:
        for tok in lexer:
            if tok.type == 'SOLDE':
                print(f"SOLDE TROUVE", tok.value)
                balance = float(tok.value[1:].replace(',', '.'))
                result['solde_initial'] = balance
                print(f"Solde initial : {balance:.2f}")
            elif tok.type == 'CREDIT':
                print(f"CREDIT TROUVE", tok.value)
                credit_value = float(tok.value.replace(',', '.'))
                balance += credit_value
                transactions.append({'transaction': tok.value, 'type': 'credit', 'solde_restant': balance})
                print(f"{tok.value} {tok.value[0]}")  # Affiche le crédit
            elif tok.type == 'DEBIT':
                print(f"DEBIT TROUVE", tok.value)
                debit_value = float(tok.value.replace(',', '.'))
                balance += debit_value
                transactions.append({'transaction': tok.value, 'type': 'debit', 'solde_restant': balance})
                print(f"{tok.value} {tok.value[0]}")  # Affiche le débit
            elif tok.type == 'SEPARATOR':
                print(f"SEPARATOR TROUVE", tok.value)
                result['transactions'][f"transaction{transaction_count}"] = transactions
                transactions = []
                transaction_count += 1
                print("-----------------")
                print(f"= {balance:.2f}")
            else: print(f'COMMENT TROUVE', tok.value)
            if balance < 0:
                message = {"message": f"Incoherence detectee : le solde est negatif apres la transaction {tok.value}"}
                with open('data/error_lex.json', 'w') as error_file:
                    json.dump(message, error_file, indent=4)
                with open('data/history_error_transaction.json', 'r') as error_file:
                    history_error = json.load(error_file)
                history_error['data'].append(message)
                with open('data/history_error_transaction.json', 'w') as error_file:
                    json.dump(history_error, error_file, indent=4)
                raise Exception(f"Incohérence détectée : le solde est négatif après la transaction {tok.value}")
        # Enregistrer le résultat dans un fichier JSON
        #Lire le fichier json    
        with open('data/resultat_transactions.json', 'w') as json_file:
            json.dump(result, json_file, indent=4)
        
        with open('data/history_success_transaction.json', 'r') as json_file:
            history_data = json.load(json_file)
        history_data['data'].append(result)
            
        with open('data/history_success_transaction.json', 'w') as json_file:
            json.dump(history_data, json_file, indent=4)
       
        
        ##stocker le contenu dans du fichier json dans la session
        return "success"
    except Exception as e:
        return "error"

