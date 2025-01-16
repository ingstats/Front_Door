import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from main import get_combined_sampled_data

# 페이지 설정
st.set_page_config(page_title="업종 대분류 분석", layout="wide")

# 페이지 제목 및 설명
st.title("📊 업종 대분류 분석")
st.markdown("""
    선택한 업종 대분류에 대한 소비 데이터와 트렌드를 시각적으로 분석합니다. 
    데이터는 월별, 성별, 연령대, 요일, 시간대별로 세분화하여 제공합니다.
""")

# 데이터 로드
region_url = st.session_state.get("region_url", None)
if not region_url:
    st.error("❌ 지역 정보를 찾을 수 없습니다. 먼저 지역을 선택해주세요.")
    st.stop()

sampled_df = get_combined_sampled_data(region_url)
if sampled_df.empty:
    st.error("❌ 데이터를 불러올 수 없습니다. 다시 시도해주세요.")
    st.stop()

# 데이터 처리
df = sampled_df.copy()
df['month'] = pd.to_datetime(df['ta_ymd'], format='%Y%m%d').dt.month

# 업종 대분류 선택
st.markdown("## 🔍 업종 대분류 선택")
unique_main_categories = df["card_tpbuz_nm_1"].dropna().unique()
selected_category = st.selectbox("관심 있는 업종 대분류를 선택하세요:", sorted(unique_main_categories))

# 데이터 필터링
filtered_df = df[df["card_tpbuz_nm_1"] == selected_category]
if filtered_df.empty:
    st.warning(f"선택한 대분류 업종 '{selected_category}'에 해당하는 데이터가 없습니다.")
    st.stop()

# 선택한 대분류 표시
st.markdown(f"### **선택한 업종 대분류: {selected_category}**")

# 1. 월별 매출 금액 추이
st.markdown("#### 📈 월별 매출 금액 추이")
monthly_sales = filtered_df.groupby("month")["amt"].sum().reset_index()
fig1 = px.line(
    monthly_sales, x="month", y="amt",
    title="월별 총 매출 금액 추이",
    labels={"month": "월", "amt": "매출 금액"},
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

# 2. 성별 매출 비율
st.markdown("#### 👫 성별 매출 비율")
gender_sales = filtered_df.groupby("sex")["amt"].sum().reset_index()
fig2 = px.pie(
    gender_sales, values="amt", names="sex",
    title="성별 매출 비율",
    color_discrete_map={'M': 'blue', 'F': 'pink'}
)
st.plotly_chart(fig2, use_container_width=True)

# 3. 성별 및 연령대별 매출 비교
st.markdown("#### 👥 성별 & 연령대별 매출 비교")
sales_by_gender_age = filtered_df.groupby(['sex', 'age'])['amt'].sum().reset_index()
fig3 = px.bar(
    sales_by_gender_age, x='age', y='amt', color='sex',
    barmode='group',
    labels={'amt': '매출 금액', 'age': '연령대', 'sex': '성별'},
    title='성별 및 연령대별 매출 비교',
    color_discrete_map={'M': 'blue', 'F': 'pink'}
)
st.plotly_chart(fig3, use_container_width=True)

# 4. 요일별 소비 패턴 분석
st.markdown("#### 📅 요일별 소비 패턴 분석")
day_mapping = {
    1: '월', 2: '화', 3: '수', 4: '목', 5: '금', 6: '토', 7: '일'
}
filtered_df["day_name"] = filtered_df["day"].map(day_mapping)
weekday_data = filtered_df.groupby("day_name").agg(
    total_amount=("amt", "sum"),
    total_count=("cnt", "sum")
).reset_index()

fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=weekday_data['day_name'], y=weekday_data['total_amount'],
    mode='lines+markers', name='소비 금액',
    line=dict(color='#1F77B4'), marker=dict(size=8)
))
fig4.add_trace(go.Scatter(
    x=weekday_data['day_name'], y=weekday_data['total_count'],
    mode='lines+markers', name='소비 건수',
    line=dict(color='#FF7F0E'), marker=dict(size=8), yaxis='y2'
))
fig4.update_layout(
    title="요일별 소비 금액 및 건수",
    xaxis=dict(title="요일"),
    yaxis=dict(title="소비 금액", titlefont=dict(color='#1F77B4')),
    yaxis2=dict(title="소비 건수", titlefont=dict(color='#FF7F0E'), overlaying='y', side='right'),
    legend=dict(orientation="h")
)
st.plotly_chart(fig4, use_container_width=True)

# 5. 시간대별 소비 패턴 분석
st.markdown("#### ⏰ 시간대별 소비 패턴 분석")
hourly_data = filtered_df.groupby("hour")[["amt", "cnt"]].sum().reset_index()
fig5 = go.Figure()
fig5.add_trace(go.Bar(
    x=hourly_data['hour'], y=hourly_data['amt'],
    name='소비 금액', marker_color='#008080'
))
fig5.add_trace(go.Scatter(
    x=hourly_data['hour'], y=hourly_data['cnt'],
    name='소비 건수', mode='lines+markers', marker_color='#F4A261', yaxis='y2'
))
fig5.update_layout(
    title="시간대별 소비 금액 및 건수",
    xaxis=dict(title="시간대"),
    yaxis=dict(title="소비 금액", titlefont=dict(color='#008080')),
    yaxis2=dict(title="소비 건수", titlefont=dict(color='#F4A261'), overlaying='y', side='right'),
    legend=dict(orientation="h"),
    bargap=0.2
)
st.plotly_chart(fig5, use_container_width=True)
