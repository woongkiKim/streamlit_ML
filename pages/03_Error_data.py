import pandas as pd
import plotly.express as px
import streamlit as st
import joblib
import lightgbm as lgb
import numpy as np

# 기본 데이터 프레임 생성
default_values = {
    'molten_temp': 731,
    'production_cycletime': 120,
    'low_section_speed': 110,
    'high_section_speed': 110,
    'cast_pressure': 310,
    'biscuit_thickness': 40,
    'upper_mold_temp1': 200,
    'upper_mold_temp2': 200,
    'lower_mold_temp1': 200,
    'lower_mold_temp2': 200,
    'lower_mold_temp3': 1449,
    'sleeve_temperature': 480,
    'physical_strength': 0,
    'Coolant_temperature': 30,
    'EMS_operation_time': 2
}

df = pd.DataFrame(default_values, index=[0])

# Streamlit 레이아웃
st.title("주조 모델 예측 대시보드")

# 모델 불러오기
model = joblib.load('models/casting_lgbm.pkl')

# 첫 번째 구역: 개별 데이터 입력 및 결과 출력
st.header("개별 예측")

with st.form("individual_prediction_form"):
    edited_df = st.data_editor(df, num_rows="dynamic")
    submit_button = st.form_submit_button(label="예측")

if submit_button:
    result_proba = model.predict_proba(edited_df)
    result = model.predict(edited_df)
    result_text = "✅ 정상품" if result[0] == 0 else "❌ 불량품"
    st.write(f"예측 결과: {result_text}")
    st.write(f"불량 확률: {result_proba[0][1] * 100:.2f}%")

# 두 번째 구역: 특정 칼럼의 값을 범위로 지정하여 확률 시각화
st.header("특정 변수의 범위 예측")

with st.form("range_prediction_form"):
    selected_col = st.selectbox("범위로 지정할 변수 선택", list(default_values.keys()))
    min_value = st.number_input(f"최소 변경 값", value=0)
    max_value = st.number_input(f"최대 변경 값", value=1000)
    step_value = st.number_input("스텝 값", value=10)

    # 나머지 변수들 입력
    for col in df.columns:
        if col != selected_col:
            default_values[col] = st.number_input(f"{col} 값", value=default_values[col])
    
    range_submit_button = st.form_submit_button(label="시각화")

if range_submit_button:
    selected_values = np.arange(min_value, max_value + step_value, step_value)
    range_df = pd.concat([pd.DataFrame(default_values, index=[0])] * len(selected_values), ignore_index=True)
    range_df[selected_col] = selected_values
    
    range_result_proba = model.predict_proba(range_df)
    range_df['failure_probability'] = range_result_proba[:, 1] * 100

    fig = px.line(range_df, x=selected_col, y='failure_probability',
                  title=f'{selected_col} 값의 범위에 따른 불량 확률',
                  labels={selected_col: f'{selected_col}', 'failure_probability': '불량 확률 (%)'})
    st.plotly_chart(fig)