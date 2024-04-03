import csv
from flask import Flask, jsonify, render_template, request
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import EmailField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

CSVFile = 'Car_Model_List.csv'

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

# class to hold form data
class CarModelForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    year = SelectField(u'Year', validators=[DataRequired()], validate_choice=False)
    make = SelectField(u'Make', validators=[DataRequired()], validate_choice=False)
    model = SelectField(u'Model', validators=[DataRequired()], validate_choice=False)
    submit = SubmitField('Submit', validators=[DataRequired()])

# End point for form submission and retrieval
@app.route('/', methods=['GET', 'POST'])
def index():
    form = CarModelForm()

    # Populate form select fields with data from CSV
    years, makes, models = read_csv_data(CSVFile)
    form.year.choices = [(year, year) for year in years]
    form.make.choices = [(make, make) for make in makes]
    form.model.choices = [(model, model) for model in models]

    if request.method == 'POST' and form.validate_on_submit():
        # Process form submission
        name = form.name.data
        email = form.email.data
        year = form.year.data
        make = form.make.data
        model = form.model.data

        # Store submitted data in a variable
        submitted_data = {'name': name, 'email': email, 'year': year, 'make': make, 'model': model}

        # Pass submitted data to the template
        return render_template('index.html', form=form, submitted_data=submitted_data)

    return render_template('index.html', form=form)



# Route to get models for a given year and make of a car
@app.route('/models')
def get_models():
    year = request.args.get('year')
    make = request.args.get('make')
    
    # Read models based on the selected year and make from CSV file
    models = get_models_from_csv(CSVFile, year, make)
    
    return jsonify({'models': models})



# Helper function to read csv file and get year, make and model
def read_csv_data(csv_file):
    years = ['']
    makes = ['']
    models = ['']

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            years.append(row['Year'])
            makes.append(row['Make'])
            models.append(row['Model'])

    # Remove duplicates and sort
    years = sorted(list(set(years)))
    makes = sorted(list(set(makes)))
    models = sorted(list(set(models)))

    return years, makes, models

# Helper function to get models from csv for a given year and make of a car
def get_models_from_csv(csv_file, year, make):
    models = ['']
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Year'] == year and row['Make'] == make:
                models.append(row['Model'])
    return models


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)