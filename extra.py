import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

# Sample dataset
data = {'Symptoms': ['Fever, Body Pain, Headache', 'Allergies, Runny Nose, Itchy', 
                     'Sore Throat, Fever, Cough', 'Body Pain, Swelling',
                     'Fever, Runny Nose, Cough', 'Allergies, Sneezing'],
        'Medicine': ['Paracetamol', 'Levocetrizine', 'Azithromycin', 'Ibuprofen', 'Paracetamol', 'Levocetrizine']}

df = pd.DataFrame(data)

# Preprocessing the data
# Convert Symptoms into individual symptom flags
df['Fever'] = df['Symptoms'].apply(lambda x: 1 if 'Fever' in x else 0)
df['Body Pain'] = df['Symptoms'].apply(lambda x: 1 if 'Body Pain' in x else 0)
df['Headache'] = df['Symptoms'].apply(lambda x: 1 if 'Headache' in x else 0)
df['Runny Nose'] = df['Symptoms'].apply(lambda x: 1 if 'Runny Nose' in x else 0)
df['Itchy'] = df['Symptoms'].apply(lambda x: 1 if 'Itchy' in x else 0)
df['Sore Throat'] = df['Symptoms'].apply(lambda x: 1 if 'Sore Throat' in x else 0)
df['Cough'] = df['Symptoms'].apply(lambda x: 1 if 'Cough' in x else 0)
df['Swelling'] = df['Symptoms'].apply(lambda x: 1 if 'Swelling' in x else 0)
df['Sneezing'] = df['Symptoms'].apply(lambda x: 1 if 'Sneezing' in x else 0)

# Features and Target
X = df[['Fever', 'Body Pain', 'Headache', 'Runny Nose', 'Itchy', 'Sore Throat', 'Cough', 'Swelling', 'Sneezing']]
y = df['Medicine']

# Split dataset into training set and test set (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Create Decision Tree classifier
clf = DecisionTreeClassifier()

# Train Decision Tree classifier
clf = clf.fit(X_train, y_train)

# Predict on test data
y_pred = clf.predict(X_test)

# Model Accuracy
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# Test the model with a new sample of symptoms
new_symptom = [[1, 1, 0, 0, 0, 0, 0, 0, 0]]  # Example: Fever, Body Pain
predicted_medicine = clf.predict(new_symptom)
print("Predicted Medicine:", predicted_medicine[0])
