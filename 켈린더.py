import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(
    page_title="학급 일정표",
    page_icon="📅",
    layout="wide"
)

# 세션 상태 초기화 (앱 실행 동안 데이터 유지)
if "events" not in st.session_state:
    st.session_state.events = pd.DataFrame(
        [
            {"날짜": "2026-03-02", "반": "1반", "일정 내용": "입학식 및 오리엔테이션", "비고": "강당"},
            {"날짜": "2026-03-15", "반": "전체", "일정 내용": "학급 임원 선거", "비고": "각 교실"},
            {"날짜": "2026-04-20", "반": "2반", "일정 내용": "과학의 날 행사", "비고": "준비물 지참"},
        ]
    )

st.title("📅 우리 반 학급 일정표")
st.caption("Streamlit Cloud를 통해 공유되는 학급 일정 관리 앱입니다.")

# 사이드바: 새 일정 추가
st.sidebar.header("➕ 새 일정 추가")
with st.sidebar.form("add_event_form", clear_on_submit=True):
    event_date = st.date_input("날짜 선택", datetime.now())
    event_class = st.selectbox("대상 학급/범위", ["전체", "1반", "2반", "3반", "기타"])
    event_title = st.text_input("일정 내용")
    event_note = st.text_input("비고 (장소, 준비물 등)")
    
    submitted = st.form_submit
