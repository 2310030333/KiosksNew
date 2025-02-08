from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pandas as pd
from pymongo import MongoClient
from sklearn.tree import DecisionTreeClassifier
from twilio.rest import Client

# Flask app initialization
app = Flask(__name__)
app.secret_key = "76dd21eac4b898822e6cd58511730ccb"

# MongoDB setup
client = MongoClient('mongodb+srv://deepikapattem:chinni12@learncluster.r9vkc7l.mongodb.net/')  # Adjust URI if needed
db = client['healthcare_kiosk']
users_collection = db['users']

# Twilio setup (replace with your credentials)
twilio_sid = "AC3017e59dc2b145329fb97e4f1c3fa2ec"
twilio_auth_token = "2e5a322d58062720a3ffdb709e24dd76"
twilio_number = "+17756183067"
your_phone_number = "+919106954439"

# Initialize Twilio client
twilio_client = Client(twilio_sid, twilio_auth_token)

# Routes for the app
@app.route("/")
def main():
    return render_template("Loginpage.html")

@app.route("/login2")
def login2():
    return render_template("LoginPage2.html")

@app.route("/login3")
def login3():
    return render_template("Loginpage3.html")

@app.route("/reg")
def register():
    return render_template("Registerpage.html")

@app.route("/locate_facility", methods=["GET", "POST"])
def locate_facility():
    return render_template("locate_facility.html")

@app.route("/awareness", methods=["GET", "POST"])
def awareness():
    return render_template("aweraness.html")

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        user_data = {
            "username": request.form.get("name"),
            "age": request.form.get("age"),
            "gender": request.form.get("gender"),
            "address": request.form.get("address"),
            "blood_type": request.form.get("blood-type"),
            "id_proof": request.form.get("id-proof"),
            "govt_id": request.form.get("govt-id"),
            "password": request.form.get("password")
        }
        users_collection.insert_one(user_data)
    return render_template("submitted.html")

@app.route("/Profile", methods=["GET", "POST"])
def Profile():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users_collection.find_one({"username": username})

        if user and user["password"] == password:
            return render_template("Profilepage.html", username=username)
        else:
            return redirect(url_for("login3"))

@app.route("/webconsult", methods=["GET", "POST"])
def webconsult():
    # Link to the video call (you can generate or use a static link)
    video_call_link = "https://video-calling-app-1-donw.onrender.com"

    # Send SMS with the link to your phone
    message = twilio_client.messages.create(
        body=f"Your web consultation link: {video_call_link}",
        from_=twilio_number,
        to=your_phone_number
    )
    return render_template("webconsultation.html")

@app.route("/newServ")
def newServ():
    return render_template("Newservicepage.html")

@app.route("/prevServ")
def prevServ():
    user = users_collection.find_one({"username": "Deepika"})
    return render_template("Servicepage.html", array=user["Services"])

# Decision Tree Model for Medicine Prediction
data = {
    'Symptoms': ['Fever, Body Pain, Headache', 'Allergies, Runny Nose, Itchy',
                 'Sore Throat, Fever, Cough', 'Body Pain, Swelling',
                 'Fever, Runny Nose, Cough', 'Allergies, Sneezing'],
    'Medicine': ['Paracetamol', 'Levocetrizine', 'Azithromycin', 'Ibuprofen', 'Paracetamol', 'Levocetrizine']
}

df = pd.DataFrame(data)

# Add symptom columns to the dataframe
df['Fever'] = df['Symptoms'].apply(lambda x: 1 if 'Fever' in x else 0)
df['Body Pain'] = df['Symptoms'].apply(lambda x: 1 if 'Body Pain' in x else 0)
df['Headache'] = df['Symptoms'].apply(lambda x: 1 if 'Headache' in x else 0)
df['Runny Nose'] = df['Symptoms'].apply(lambda x: 1 if 'Runny Nose' in x else 0)
df['Itchy'] = df['Symptoms'].apply(lambda x: 1 if 'Itchy' in x else 0)
df['Sore Throat'] = df['Symptoms'].apply(lambda x: 1 if 'Sore Throat' in x else 0)
df['Cough'] = df['Symptoms'].apply(lambda x: 1 if 'Cough' in x else 0)
df['Swelling'] = df['Symptoms'].apply(lambda x: 1 if 'Swelling' in x else 0)
df['Sneezing'] = df['Symptoms'].apply(lambda x: 1 if 'Sneezing' in x else 0)

X = df[['Fever', 'Body Pain', 'Headache', 'Runny Nose', 'Itchy', 'Sore Throat', 'Cough', 'Swelling', 'Sneezing']]
y = df['Medicine']

# Train a Decision Tree Classifier
clf = DecisionTreeClassifier()
clf = clf.fit(X, y)

def convert_symptoms(symptom_list):
    symptom_map = { 'fever': 0, 'bodypain': 0, 'headache': 0, 'runnynose': 0, 'itchy': 0, 'sorethroat': 0, 'cough': 0, 'swelling': 0, 'sneezing': 0 }

    for symptom in symptom_list:
        if symptom.lower() in symptom_map:
            symptom_map[symptom.lower()] = 1

    return [[symptom_map['fever'], symptom_map['bodypain'], symptom_map['headache'], symptom_map['runnynose'], 
             symptom_map['itchy'], symptom_map['sorethroat'], symptom_map['cough'], symptom_map['swelling'], symptom_map['sneezing']]]

@app.route('/predict', methods=['POST'])
def predict_medicine():
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({'error': 'Invalid JSON format or missing symptoms'}), 400
    symptoms = data['symptoms']
    features = convert_symptoms(symptoms)
    prediction = clf.predict(features)
    return jsonify({'medicine': prediction[0]})


@app.route("/faq")
def faq():
    return render_template("random.html")

@app.route("/Serv")
def Serv():
    return render_template("ServicesPage.html")

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
