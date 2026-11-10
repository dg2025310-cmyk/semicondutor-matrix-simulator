
import streamlit as st
import numpy as np
import pandas as pd

# -------------------------
# 1. 기본 설정
# -------------------------
st.set_page_config(
    page_title="반도체 행렬 연산 시뮬레이터",
    page_icon="🔬",
    layout="wide"
)

# -------------------------
# 2. 디자인
# -------------------------
st.markdown("""
<style>
.stApp {
    background-color: #081426;
    color: #EAF2FF;
}

[data-testid="stHeader"] {
    background-color: #081426;
}

h1, h2, h3, h4 {
    color: #8FC8FF !important;
}

p, label, span {
    color: #EAF2FF;
}

.step-card {
    background-color: #142944;
    border: 1px solid #294766;
    border-radius: 14px;
    padding: 25px;
    margin-top: 15px;
    margin-bottom: 15px;
}

.step-number {
    color: #65B9FF;
    font-size: 14px;
    font-weight: bold;
}

.step-title {
    color: #8FC8FF;
    font-size: 25px;
    font-weight: bold;
    margin-top: 5px;
}

.step-description {
    color: #D6E8FF;
    font-size: 15px;
}

.arrow {
    text-align: center;
    color: #65B9FF;
    font-size: 30px;
    padding: 5px;
}

.stButton > button {
    background-color: #1769AA;
    color: white;
    border-radius: 8px;
    border: none;
    height: 45px;
}

div[data-testid="stDataFrame"] {
    background-color: #142944;
    border-radius: 10px;
}

div[data-testid="stMetric"] {
    background-color: #142944;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# 3. 제목
# -------------------------
st.title("🔬 반도체 행렬 연산 시뮬레이터")

st.markdown("""
인공지능 반도체 NPU 내부에서 데이터가 입력되고,
행렬로 변환되어 최종 결과가 만들어지는 과정을 알아보자.
""")

st.markdown("---")


# -------------------------
# 01. 데이터 입력
# -------------------------
st.markdown("""
<div class="step-card">
    <div class="step-number">STEP 01</div>
    <div class="step-title">데이터 입력</div>
    <div class="step-description">
    연산에 필요한 숫자 데이터를 입력하는 단계
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
인공지능 반도체는 이미지, 음성 등의 정보를
숫자 형태로 입력받아 처리한다.

아래는 행렬 연산을 이해하기 위한 예시 데이터다.
""")

cols = st.columns(4)

default_values = [1, 2, 3, 4]
input_values = []

for i, col in enumerate(cols):
    with col:
        value = st.number_input(
            f"데이터 {i+1}",
            min_value=0,
            max_value=255,
            value=default_values[i],
            key=f"input_{i}"
        )
        input_values.append(value)

st.session_state["input_values"] = input_values

st.info("입력된 숫자 데이터는 다음 단계에서 행렬로 변환된다.")


# 화살표
st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)


# -------------------------
# 02. 행렬 변환
# -------------------------
st.markdown("""
<div class="step-card">
    <div class="step-number">STEP 02</div>
    <div class="step-title">행렬 변환</div>
    <div class="step-description">
    입력 데이터를 행렬 형태로 구성하는 단계
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
입력된 숫자를 2×2 행렬로 배열한다.
또한 연산에 사용되는 가중치 행렬을 준비한다.
""")

A = np.array(input_values).reshape(2, 2)

B = np.array([
    [5, 6],
    [7, 8]
])

col1, col2 = st.columns(2)

with col1:
    st.subheader("입력 행렬 A")
    st.dataframe(
        pd.DataFrame(A),
        use_container_width=True
    )

with col2:
    st.subheader("가중치 행렬 B")
    st.dataframe(
        pd.DataFrame(B),
        use_container_width=True
    )

st.session_state["A"] = A
st.session_state["B"] = B

st.success("숫자 데이터가 행렬 형태로 구성되었다.")

st.caption(
    "가중치 행렬은 설명을 위한 예시값이다. "
    "실제 인공지능에서는 학습을 통해 정해진 가중치를 사용한다."
)


st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)


# -------------------------
# 03. 행렬 연산
# -------------------------
st.markdown("""
<div class="step-card">
    <div class="step-number">STEP 03</div>
    <div class="step-title">행렬 연산</div>
    <div class="step-description">
    곱셈과 누적 덧셈을 반복하여 결과를 계산하는 단계
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
두 행렬의 행과 열에 해당하는 숫자를 곱한 뒤
그 결과를 더하는 과정을 반복한다.
이러한 연산 구조를 MAC이라고 한다.
""")

selected_row = st.selectbox(
    "계산할 결과의 행",
    [0, 1],
    format_func=lambda x: f"{x+1}번째 행"
)

selected_col = st.selectbox(
    "계산할 결과의 열",
    [0, 1],
    format_func=lambda x: f"{x+1}번째 열"
)

total = 0

for k in range(2):
    multiply = A[selected_row, k] * B[k, selected_col]
    before = total
    total += multiply

    st.markdown(f"**연산 {k+1}**")

    st.latex(
        f"{A[selected_row,k]:g}"
        + r" \times "
        + f"{B[k,selected_col]:g}"
        + f" = {multiply:g}"
    )

    st.write(
        f"누적 계산: {before:g} + {multiply:g} = {total:g}"
    )

C = A @ B

st.divider()

st.subheader("전체 행렬 곱셈")

st.latex(r"C=A\times B")

st.dataframe(
    pd.DataFrame(C),
    use_container_width=True
)

st.session_state["result"] = C

st.info("""
MAC은 Multiply-Accumulate의 약자다.
곱셈 결과를 누적해서 더하는 연산으로,
행렬 곱셈의 각 결과값을 계산할 때 활용된다.
""")


st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)


# -------------------------
# 04. 결과 전달
# -------------------------
st.markdown("""
<div class="step-card">
    <div class="step-number">STEP 04</div>
    <div class="step-title">결과 전달</div>
    <div class="step-description">
    계산된 결과 행렬을 생성하고 다음 연산 단계로 전달하는 단계
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
모든 행렬 계산이 완료되면 최종 결과 행렬이 만들어진다.
이 결과는 다음 신경망 연산 단계 등에서 활용될 수 있다.
""")

st.subheader("최종 결과 행렬")

st.dataframe(
    pd.DataFrame(C),
    use_container_width=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("입력 데이터 수", "4개")

with col2:
    st.metric("행렬 크기", "2 × 2")

with col3:
    st.metric("MAC 연산 횟수", "8회")

st.success("행렬 연산 및 결과 생성 완료!")

st.markdown("---")

st.subheader("핵심 내용 정리")

st.write("""
① 데이터 입력: 숫자 형태의 데이터 입력

② 행렬 변환: 입력 데이터를 행렬로 구성

③ 행렬 연산: 곱셈과 누적 덧셈 수행

④ 결과 전달: 최종 결과 행렬 생성 및 전달
""")

st.caption(
    "교육용 시뮬레이터 | NPU 행렬 연산의 기본 원리"
)
