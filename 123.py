import streamlit as st
from openai import OpenAI

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="칭찬 생성기",
    page_icon="✨",
    layout="centered"
)

st.title("✨ AI 칭찬 생성기")
st.write("상황이나 사람의 특징을 입력하면 AI가 자연스러운 칭찬을 만들어 줍니다.")

# -----------------------------
# OpenAI API 연결
# -----------------------------
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error(
        "OPENAI_API_KEY가 설정되지 않았습니다.\n\n"
        "Streamlit Cloud의 Settings → Secrets에서 "
        "OPENAI_API_KEY를 추가해주세요."
    )
    st.stop()


# -----------------------------
# 입력 영역
# -----------------------------
st.subheader("칭찬할 사람에 대해 알려주세요")

name = st.text_input(
    "이름",
    placeholder="예: 민수"
)

situation = st.text_area(
    "어떤 사람인지 또는 어떤 일을 했는지",
    placeholder="예: 학교 축제 준비를 열심히 했고 친구들을 잘 도와줬어."
)

style = st.selectbox(
    "칭찬 스타일",
    [
        "따뜻하고 진심 어린 칭찬",
        "재미있고 유쾌한 칭찬",
        "친구에게 하는 자연스러운 칭찬",
        "감동적인 칭찬",
        "짧고 간단한 칭찬"
    ]
)

length = st.selectbox(
    "칭찬 길이",
    [
        "한 문장",
        "2~3문장",
        "조금 자세하게"
    ]
)


# -----------------------------
# 칭찬 생성
# -----------------------------
if st.button("✨ 칭찬 만들어줘", use_container_width=True):

    if not situation.strip():
        st.warning("칭찬할 사람의 특징이나 상황을 입력해주세요.")
        st.stop()

    person = name.strip() if name.strip() else "그 사람"

    prompt = f"""
다음 정보를 바탕으로 자연스럽고 기분 좋은 칭찬을 만들어줘.

이름: {person}
특징 또는 상황: {situation}
칭찬 스타일: {style}
칭찬 길이: {length}

조건:
- 한국어로 작성해줘.
- 진심이 느껴지는 자연스러운 표현을 사용해줘.
- 외모에 대한 평가보다는 행동, 노력, 성격, 능력 등을 중심으로 칭찬해줘.
- 과장되거나 어색한 표현은 피하고 실제로 친구에게 말할 수 있는 표현으로 만들어줘.
- 결과만 출력하고 설명은 하지 마.
"""

    try:
        with st.spinner("칭찬을 만들고 있어요..."):

            response = client.responses.create(
                model="gpt-5.4-nano",
                input=prompt
            )

            compliment = response.output_text.strip()

        st.success("칭찬이 완성됐어요! ✨")

        st.markdown(
            f"""
            <div style="
                padding: 25px;
                border-radius: 15px;
                border: 1px solid #ddd;
                margin-top: 10px;
                font-size: 20px;
                text-align: center;
            ">
                💬 {compliment}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error("칭찬을 생성하는 중 오류가 발생했습니다.")
        st.caption(f"오류 내용: {e}")


# -----------------------------
# 안내
# -----------------------------
st.divider()

st.caption(
    "💡 이름을 입력하지 않아도 사용할 수 있습니다. "
    "상황이나 특징을 자세히 입력할수록 더 자연스러운 칭찬을 만들 수 있습니다."
)
