import joblib

def predict(data):
    
    clf = joblib.load('models/iris_classifier.pkl')

    return clf.predict(data)