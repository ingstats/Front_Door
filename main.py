import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO 
import pandas as pd
import os
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="메인", layout="wide")
st.title("Welcome!")
st.markdown("""
            ## 🏢 창업을 꿈꾸는 당신을 위한 정보 플랫폼
            
            창업을 준비하고 계신가요? 
            본 홈페이지는 예비 창업자들이 자신만의 비즈니스를 계획하고 실행하는 데 필요한 데이터와 인사이트를 제공합니다. 
            
            ### 🌟 제공 기능
            
            **1. 업종 분석**
            - **대분류 정보 제공**: 주요 업종에 대한 전반적인 데이터를 제공
              - **차트 및 그래프**: 업종별 매출, 소비자 트렌드, 시간대별 매출 등을 시각적으로 이해하기 쉽게 제공합니다.
            - **소분류 정보 제공**: 특정 업종 내 세부 카테고리에 대한 상세 데이터를 제공합니다. 
              - **상세 통계**: 소비자 성향, 연령대별 소비 패턴 등 창업자에게 실질적인 도움이 되는 정보를 확인하세요.
            **2. 맞춤형 시각화 도구**
            - 입력하신 데이터와 조건을 바탕으로, 업종 및 지역별 데이터를 커스터마이즈하여 시각화할 수 있습니다.
              - **시간 단위 분석**: 일별, 주별, 월별 데이터를 선택하여 비즈니스 성과를 예측.
              - **트렌드 비교**: 다양한 카테고리를 한눈에 비교.
            **3. 추가 개발 예정 기능**
            - **지역별 소비 분석**: 창업 예정 지역의 소비자 데이터를 통해 시장성을 확인하세요.
            - **추천 업종**: 소비 패턴 및 데이터 기반으로 적합한 업종을 추천해 드립니다.
            - **투자 전략 도구**: 창업 초기 자본 투자 계획 수립을 돕는 시뮬레이션 도구.
            ### 🎯 당신의 성공적인 창업을 응원합니다!
            데이터를 활용한 철저한 시장 분석으로, 창업의 첫걸음을 내딛어 보세요. 
            제공되는 정보를 통해 창업 계획을 더욱 구체화하고, 성공적인 비즈니스로 발전시킬 수 있습니다.
            함께 성장하는 미래를 만들어 봅시다! 🚀
            오류 문의: dahee7446@gmail.com
            """)
# 지역 선택 기능 추가
st.sidebar.header("지역 선택")
# 대한민국 리스트
regions = [
    "서울", "부산", "대구", "인천",
    "광주", "대전", "울산", "세종",
    "경기도", "충북", "충남", "전남", "경북",
    "경남", "강원", "전북", "제주"]
# 단일 지역 선택
selected_region = st.sidebar.selectbox("창업 예정 지역을 선택하세요", regions)

# 선택된 지역에 따른 데이터 필터링
# 데이터프레임 예제 코드 (실제 데이터와 연결 필요)
# df = pd.read_csv("path_to_your_data.csv")
# filtered_df = df[df['region'] == selected_region]
# st.write("### 지역별 데이터")
# st.dataframe(filtered_df)



# 파일 읽기 함수
def load_csv_file(file_path):
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        return df
    except Exception as e:
        st.write("에러 발생:", e)
        return None


# 메인 함수
def main():
    st.title("CSV 파일 병합 및 데이터 미리보기")

    # 파일 경로 템플릿
    base_url = 'https://woori-fisa-bucket.s3.ap-northeast-2.amazonaws.com/fisa04-card/tbsh_gyeonggi_day_2023{}_pochun.csv'

    # 데이터를 합칠 데이터프레임 초기화
    combined_df = pd.DataFrame()

    # 202301부터 202312까지 반복 처리
    for month in range(1, 13):
        month_str = f"{month:02d}"  # 월을 두 자리로 포맷팅
        file_path = base_url.format(month_str)

        # 파일 불러오기
        with st.spinner(f"{month_str}월 데이터 로드 중..."):
            df = load_csv_file(file_path)

        # 데이터가 성공적으로 로드된 경우 합치기
        if df is not None:
            st.success(f"{month_str}월 데이터 로드 완료!")
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        else:
            st.error(f"{month_str}월 파일을 불러오지 못했습니다.")

    # 데이터 합친 후 미리보기
    if not combined_df.empty:
        st.write("병합된 데이터 미리보기:")
        st.dataframe(combined_df.head(50))  # 상위 50개 행 출력
    else:
        st.error("병합할 데이터가 없습니다.")

    st.success("모든 작업 완료!")


if __name__ == "__main__":
    main()
