import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from modules.predict import predict
import numpy as np


st.title('Classifying Iris Flowers')
st.markdown('Toy model to play to classify iris flowers into setosa, versicolor, virginica')

st.header("Plant Features")
col1, col2 = st.columns(2)
with col1:
    st.text("Sepal characteristics")
    sepal_l = st.slider('Sepal lenght (cm)', 1.0, 8.0, 0.5)
    sepal_w = st.slider('Sepal width (cm)', 2.0, 4.4, 0.5)

with col2:
    st.text("Pepal characteristics")
    petal_l = st.slider('Petal lenght (cm)', 1.0, 7.0, 0.5)
    petal_w = st.slider('Petal width (cm)', 0.1, 2.5, 0.5)


if st.button('예측하기'):
    result = predict(np.array([[sepal_l, sepal_w, petal_l, petal_w]]))
    print(result)
    st.text(f"✅ {result[0]}")
          
# # 데이터 불러오기
# iris = load_iris()
# X = iris.data
# y = iris.target
# df = pd.DataFrame(X, columns=iris.feature_names)

# # 모델 학습
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X, y)

# # Streamlit 앱
# st.title("Iris Species Prediction")

# st.write("""
# # Iris 데이터셋
# """)

# # 입력 받기
# sepal_length = st.slider("Sepal length", float(df['sepal length (cm)'].min()), float(df['sepal length (cm)'].max()))
# sepal_width = st.slider("Sepal width", float(df['sepal width (cm)'].min()), float(df['sepal width (cm)'].max()))
# petal_length = st.slider("Petal length", float(df['petal length (cm)'].min()), float(df['petal length (cm)'].max()))
# petal_width = st.slider("Petal width", float(df['petal width (cm)'].min()), float(df['petal width (cm)'].max()))

# # 입력 데이터를 데이터프레임으로 변환
# input_data = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]], columns=iris.feature_names)

# # 예측
# prediction = model.predict(input_data)
# prediction_proba = model.predict_proba(input_data)

# st.write(f"Predicted species: {iris.target_names[prediction][0]}")
# st.write("Prediction probabilities:")
# st.write(pd.DataFrame(prediction_proba, columns=iris.target_names))