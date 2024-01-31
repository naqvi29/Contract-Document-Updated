import sys
import os
from os.path import abspath, dirname
from flask import Blueprint, redirect, render_template, request, url_for

# Add the parent directory to the sys.path
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from services.autofill_pdfs import nome_pdf, form_filler_for_contract
from services.send_email import send_email_with_attachments

# Create a Flask Blueprint for views
views = Blueprint(__name__, "views")


# Route to redirect to the main Home page
@views.route("/", methods=['GET', 'POST'])
def index():
    return redirect(url_for("views.Home"))

# Main Home route for form processing
@views.route("/Home", methods=['GET', 'POST'])
def Home():
    if request.method == "POST":
        # try:
        # Extract form data
        num_persons = int(request.form['numPersons'])
        email = request.form['email']
        
        # Generate PDF name based on the first person's full name
        nome_do_document = nome_pdf(request.form['fullName1'])

        # Process each person's data and store in a list
        person_data = []
        for i in range(1, num_persons + 1):
            person = process_person_data(request, i)
            person_data.append(person)  
        print(person_data)

        # Fill the PDF form with the collected data
        filled = form_filler_for_contract(person_data, nome_do_document)
        
        if filled:
            # Send the filled PDF as an email attachment
            send_email_with_attachments(email, nome_do_document)
            return "done"
        return "Ocorreu um erro inesperado!"
        # except Exception as e:
        #     # Handle unexpected errors and provide details in the response
        #     return f"Ocorreu um erro inesperado! Detalhes: {str(e)}"

    else:
        # Render the initial form on GET request
        return render_template("home.html")

# Helper function to process individual person's data from the form
def process_person_data(request, i):
    person = {
        'fullName': request.form[f'fullName{i}'],
        'rg': request.form[f'rg{i}'],
        'cpf': request.form[f'cpf{i}'],
        'address': request.form[f'address{i}'],
        'numChildren': int(request.form[f'numChildren{i}']),
        'children': []
    }

    # Process children's data for the current person
    for j in range(1, person['numChildren'] + 1):
        child_name = request.form[f'childName{i}_{j}']
        # child_dob = request.form[f'childDob{i}_{j}']
        # child_cpf = request.form[f'childCpf{i}_{j}']
        child_dob, child_cpf = request.form.get(f'childDob{i}_{j}', None), request.form.get(f'childCpf{i}_{j}', None)

        person['children'].append({'childName': child_name,'child_dob':child_dob,'child_cpf':child_cpf})

    return person

# Route for successful completion
@views.route("/done", methods=['GET', 'POST'])
def done(): 
    return render_template("done.html", msg='Tudo OK e finalizado com sucesso!')

# Route for unexpected errors
@views.route("/pagErro", methods=['GET', 'POST'])
def pagErro(): 
    return render_template("done.html", msg='Ocorreu um erro inesperado!')
