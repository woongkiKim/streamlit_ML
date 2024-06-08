import pandas as pd



class Preprocess:

    def hour_data_cleansing(self, df):
        # 제조 데이터의 시간 정보 변환
        df['registration_time'] = pd.to_datetime(df['registration_time'])
        df['date'] = df['registration_time'].dt.date
        df['hour'] = df['registration_time'].dt.hour
        df['weekday'] = df['registration_time'].dt.weekday ## 0:월요일, 6:일요일
        df['date_time'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['hour'].astype(str) + ':00:00')
        df['weekday'] = df['weekday'].map({0:'월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'})
        # 평균 생산시간 계산
        df['average_cycle_time'] = (df['facility_operation_cycleTime'] + df['production_cycletime']) / 2
        ## 정상품, 불량품 생성
        df['pass'] = df['passorfail'].apply(lambda x: 1 if x == 0 else 0)
        df['fail'] = df['passorfail'].apply(lambda x: 1 if x == 1 else 0)


        # 데이터프레임에서 평균 생산 시간과 생산량 계산
        grouped_data = df.groupby(['date_time','mold_code','weekday','hour'])['average_cycle_time'].agg(['mean','median','count']).reset_index()
        ## 불량률 계산
        grouped_data2 = df.groupby(['date_time','mold_code','weekday','hour'])['pass'].sum().reset_index(name='pass_count')
        grouped_data3 = df.groupby(['date_time','mold_code','weekday','hour'])['fail'].sum().reset_index(name='error_count')

        merge_grouped_df = pd.merge(grouped_data, grouped_data2,
                                    on=['date_time','mold_code','weekday','hour'], how='left') 

        merge_grouped_df = pd.merge(merge_grouped_df, grouped_data3,
                                        on=['date_time','mold_code','weekday','hour'], how='left')

        ## 
        merge_grouped_df['mean'] = merge_grouped_df['mean'].round(1)
        merge_grouped_df['median'] = merge_grouped_df['median'].round(1)
        merge_grouped_df['error_ratio'] = (merge_grouped_df['error_count'] / merge_grouped_df['count']).round(2)
        merge_grouped_df['pass_ratio'] = 1 - merge_grouped_df['error_ratio'].round(2)
        merge_grouped_df['date'] = merge_grouped_df['date_time'].dt.date

        return merge_grouped_df

