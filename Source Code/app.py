
from flask import Flask, render_template, request
from sklearn.preprocessing import OneHotEncoder
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form data using request.form.get()
    call_name = request.form.get('Does your child look at you when you call his/her name?')
    eye_contact = request.form.get('How easy is it for you to get eye contact with your child')
    point_to_indicate = request.form.get('Does your child point to indicate that s/he wants something? (e.g. a toy that is out of reach)')
    pointing_interest = request.form.get('Does your child point to share interest with you? (e.g. pointing at an interesting sight)')
    pretend = request.form.get('Does your child pretend? (e.g. care for dolls, talk on a toy phone)')
    follow = request.form.get('Does your child follow where you’re looking?')
    signs = request.form.get('If you or someone else in the family is visibly upset, does your child show signs of wanting to comfort them? (e.g. stroking hair, hugging them)')
    first_words = request.form.get('Would you describe your child’s first words as:')
    simple_gestures = request.form.get('Does your child use simple gestures? (e.g. wave goodbye)') 
    child_stare = request.form.get('Does your child stare at nothing with no apparent purpose?')
    
    # Convert string values to binary
    def get_binary_value(value):
        return 1 if value == 'Yes' else 0

    # Convert age and score to float
    age = request.form.get('Age')
    if age is not None:
        age = float(age)
    else:
        # Set a default age or handle the None value appropriately
        age = 0.0  # You can set any default value here

    score = request.form.get('Qchat-10-Score')
    if score is not None:
        score = float(score)
    else:
        # Set a default score or handle the None value appropriately
        score = 0.0  # You can set any default value here

    # Convert Gender and Ethnicity to binary
    Gender = 1 if request.form.get('Gender') == 'Male' else 0

    # One-hot encode Ethnicity
    ethnicity = request.form.get('Ethnicity')
    encoder = OneHotEncoder()
    ethnicity_encoded = encoder.fit_transform([[ethnicity]]).toarray()

    # Convert jaundice and Family_ASD to binary
    jaundice = 1 if request.form.get('Born with jaundice') == 'Yes' else 0
    Family_ASD = 1 if request.form.get('Family members with ASD history') == 'Yes' else 0

    # Handle None values and convert to float
    values = [
        get_binary_value(call_name),
        get_binary_value(eye_contact),
        get_binary_value(point_to_indicate),
        get_binary_value(pointing_interest),
        get_binary_value(pretend),
        get_binary_value(follow),
        get_binary_value(signs),
        get_binary_value(first_words),
        get_binary_value(simple_gestures),
        get_binary_value(child_stare),
        age,
        Gender,
        *ethnicity_encoded.tolist()[0],  # Append one-hot encoded ethnicity
        jaundice,
        Family_ASD,
        score
    ]
    
    # Reshape and scale input array
    input_array = np.array(values).reshape(1, -1)

    # Make prediction (Replace this with your model prediction)
    predicted = np.random.randint(0, 2)  # Dummy prediction for demonstration
    
    # Return prediction result
    if predicted == 0:
        prediction_result = 'The person is not with Autism Spectrum Disorder'
    else:
        prediction_result = 'The person with Autism Spectrum Disorder'

    return render_template('result.html', predicted_value=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)


