import pandas as pd
import plotly.express as px
import streamlit as st
from modules.charts import MakeChart
from modules.preprocess import Preprocess
import plotly.graph_objects as go

make_chart = MakeChart()
preprocess = Preprocess()

casting = pd.read_csv('./data/casting.csv', encoding='cp949', index_col=0)

df = casting[['registration_time','mold_code','count',
        'molten_temp', 'facility_operation_cycleTime',
        'production_cycletime', 'low_section_speed', 'high_section_speed',
        'molten_volume', 'cast_pressure', 'biscuit_thickness',
        'upper_mold_temp1', 'upper_mold_temp2', 'upper_mold_temp3',
        'lower_mold_temp1', 'lower_mold_temp2', 'lower_mold_temp3',
        'sleeve_temperature', 'physical_strength', 'Coolant_temperature',
        'passorfail']]

df['mold_code'] = df['mold_code'].astype(str)

st.write(df)


result = preprocess.hour_data_cleansing(df)

# # 제조 데이터의 시간 정보 변환
# df['registration_time'] = pd.to_datetime(df['registration_time'])
# df['date'] = df['registration_time'].dt.date
# df['hour'] = df['registration_time'].dt.hour
# df['weekday'] = df['registration_time'].dt.weekday ## 0:월요일, 6:일요일
# df['date_time'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['hour'].astype(str) + ':00:00')
# df['weekday'] = df['weekday'].map({0:'월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'})
# # 평균 생산시간 계산
# df['average_cycle_time'] = (df['facility_operation_cycleTime'] + df['production_cycletime']) / 2
# ## 정상품, 불량품 생성
# df['pass'] = df['passorfail'].apply(lambda x: 1 if x == 0 else 0)
# df['fail'] = df['passorfail'].apply(lambda x: 1 if x == 1 else 0)


# # 데이터프레임에서 평균 생산 시간과 생산량 계산
# grouped_data = df.groupby(['date_time','weekday','hour'])['average_cycle_time'].agg(['mean','median','count']).reset_index()
# ## 불량률 계산
# grouped_data2 = df.groupby(['date_time','weekday','hour'])['pass'].sum().reset_index(name='pass_count')
# grouped_data3 = df.groupby(['date_time','weekday','hour'])['fail'].sum().reset_index(name='error_count')

# merge_grouped_df = pd.merge(grouped_data, grouped_data2,
#                                on=['date_time','weekday','hour'], how='left') 

# merge_grouped_df = pd.merge(merge_grouped_df, grouped_data3,
#                                  on=['date_time','weekday','hour'], how='left')

# ## 
# merge_grouped_df['mean'] = merge_grouped_df['mean'].round(1)
# merge_grouped_df['median'] = merge_grouped_df['median'].round(1)
# merge_grouped_df['error_ratio'] = (merge_grouped_df['error_count'] / merge_grouped_df['count']).round(2)
# merge_grouped_df['pass_ratio'] = 1 - merge_grouped_df['error_ratio'].round(2)
# merge_grouped_df['date'] = merge_grouped_df['date_time'].dt.date




# Streamlit 대시보드
st.title('시간별 제조 데이터 대시보드')
st.divider()

# Streamlit에서 날짜 범위 선택 위젯을 가로로 배치
# 도넛 차트
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input('시작 날짜', value=result['date_time'].min())
with col2:
    end_date = st.date_input('종료 날짜', value=result['date_time'].max())
    

# 선택한 날짜 범위에 맞게 데이터 필터링
filtered_data = result[(result['date_time'] >= pd.to_datetime(start_date)) &
                                   (result['date_time'] <= pd.to_datetime(end_date))]


## 정상품 비율
pass_ratio = filtered_data['pass_count'].sum() / filtered_data['count'].sum()
## 불량품 비율
fail_ratio = filtered_data['error_count'].sum() / filtered_data['count'].sum()

# 필터링된 데이터로 도넛 차트 생성
donut_chart_pass = make_chart.make_donut(pass_ratio.round(2) * 100, '정상품', 'green')
donut_chart_fail = make_chart.make_donut(fail_ratio.round(2) * 100, '불량품', 'red')

with col1:
    st.write('정상품 비율')
    st.altair_chart(donut_chart_pass, use_container_width=True)

with col2:
    st.write('불량품 비율') 
    st.altair_chart(donut_chart_fail, use_container_width=True)



# Streamlit을 사용해 대시보드에 차트 표시
tab1, tab2, tab3 = st.tabs(['생산량', '불량률', '평균 생산 시간'])

with tab1:
    # 날짜별, 요일별, 시간별 생산량 시각화
    fig1 = px.bar(filtered_data, x='date_time', y='count',
        color='weekday',
        title='날짜별, 요일별, 시간별 생산량',
        labels={'count': '생산량', 'hour': '시간', 'weekday': '요일'})

    # x축 범위 설정
    fig1.update_xaxes(range=[str(start_date), str(end_date)])
    st.plotly_chart(fig1)

with tab2:
        # 날짜별, 요일별, 시간별 불량률 시각화
        fig2 = px.bar(filtered_data, x='date_time', y='error_ratio',
                color='weekday', title='날짜별, 요일별, 시간별 불량률',
                labels={'error_ratio': '불량률', 'hour': '시간', 'weekday': '요일'})
        
        ## 0.8 부분에 빨간색 점선 추가
        fig2.add_hline(y=0.8, line_dash='dot', line_color='red', annotation_text='불량률 80%', annotation_position='top right')


        # x축 범위 설정
        fig2.update_xaxes(range=[str(start_date), str(end_date)])
        st.plotly_chart(fig2)

with tab3:

        # 날짜별, 요일별, 시간별 평균 생산 시간 시각화
        fig3 = px.bar(filtered_data, x='date_time', y='mean',
                color='weekday',
                title='날짜별, 요일별, 시간별 평균 생산 시간',
                labels={'mean': '평균 생산 시간', 'hour': '시간', 'weekday': '요일'},
                color_continuous_scale='Plasma'
                )

        # x축 범위 설정
        fig3.update_xaxes(range=[str(start_date), str(end_date)])
        st.plotly_chart(fig3)
