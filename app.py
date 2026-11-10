
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
    padding: 22px;
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

.process-box {
    background-color: #10243D;
    border: 1px solid #315477;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
}

.result-box {
    background-color: #123A50;
    border: 1px solid #2786A5;
    border-radius: 12px;
    padding: 18px;
    margin-top: 12px;
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
인공지능 반도체 NPU가 숫자 데이터를 입력받아
행렬 연산을 수행하고 결과를 전달하는 과정을 알아보자.
""")

st.markdown("---")


# -------------------------
# STEP 01. 데이터 입력
# -------------------------
st.markdown("""
<div class="step-card">
    <div class="step-number">STEP 01</div>
    <div class="step-title">데이터 입력</div>
    <div class="step-description">
    인공지능 반도체가 처리할 숫자 데이터를 입력하는 단계
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
NPU는 이미지, 음성, 텍스트 등 다양한 정보를
컴퓨터가 계산할 수 있는 숫자 데이터로 처리한다.

이번 시뮬레이션에서는 이해하기 쉽도록
4개의 숫자 데이터를 사용한다.
""")

st.subheader("입력 데이터")

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
            step=1,
            key=f"input_{i}"
        )
        input_values.append(value)

st.info("입력한 숫자는 다음 단계에서 2×2 행렬로 정리된다.")

st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)


# -------------------------
# STEP 02. 행렬 변환
# -------------------------
st.markdown("""
<div class="step-card">
    <div class="step-number">STEP 02</div>
    <div class="step-title">행렬 변환</div>
    <div class="step-description">
    입력된 숫자를 행과 열로 구성된 행렬로 정리하는 단계
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
입력된 4개의 숫자를 2개의 행과 2개의 열로 배열한다.
이렇게 만들어진 행렬은 다음 단계의 계산에 사용된다.
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

st.markdown("""
<div class="process-box">
<b>행렬이 만들어지는 과정</b><br><br>
① 입력 데이터 1, 2, 3, 4 준비<br>
② 숫자를 두 개씩 나누어 배열<br>
③ 2×2 크기의 입력 행렬 A 완성<br>
④ 계산에 사용할 가중치 행렬 B 준비
</div>
""", unsafe_allow_html=True)

st.caption(
    "가중치 행렬은 계산 원리를 보여주기 위한 예시다. "
    "실제 인공지능에서는 학습을 통해 정해진 가중치를 사용한다."
)

st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)


# -------------------------
# STEP 03. 행렬 연산
# -------------------------
st.markdown("""
<div class="step-card">
    <div class="step-number">STEP 03</div>
    <div class="step-title">행렬 연산</div>
    <div class="step-description">
    두 행렬의 숫자를 곱하고 더하여 새로운 값을 만드는 단계
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
이 단계에서는 입력 행렬 A와 가중치 행렬 B를 계산한다.

계산 방법은 간단하다.

1. A의 한 행과 B의 한 열에서 숫자를 가져온다.
2. 서로 대응하는 숫자끼리 곱한다.
3. 곱한 결과를 더한다.
4. 이 과정을 반복하여 결과 행렬을 완성한다.
""")

st.markdown("""
<div class="process-box">
<b>MAC 연산이란?</b><br><br>
MAC은 곱셈(Multiply)과 누적 덧셈(Accumulate)을
반복하는 연산 방식이다.<br><br>
인공지능 반도체는 이러한 계산을 많이 수행하여
인공지능 모델의 결과를 만들어 낸다.
</div>
""", unsafe_allow_html=True)

# 전체 행렬 계산
C = A @ B

st.subheader("행렬 연산 과정")

st.write("각 결과값이 만들어지는 과정을 확인해 보자.")

# 각 결과 원소의 계산 과정
for i in range(2):
    for j in range(2):

        first = A[i, 0] * B[0, j]
        second = A[i, 1] * B[1, j]
        result = first + second

        with st.expander(
            f"결과 행렬의 {i+1}행 {j+1}열 계산 과정"
        ):
            st.markdown("**① 대응하는 숫자끼리 곱하기**")

            st.latex(
                f"{A[i,0]} \\times {B[0,j]} = {first}"
            )

            st.latex(
                f"{A[i,1]} \\times {B[1,j]} = {second}"
            )

            st.markdown("**② 곱셈 결과 더하기**")

            st.latex(
                f"{first} + {second} = {result}"
            )

            st.success(
                f"결과 행렬의 {i+1}행 {j+1}열 값은 {result}이다."
            )

st.divider()

st.subheader("완성된 결과 행렬")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("입력 행렬 A")
    st.dataframe(pd.DataFrame(A), use_container_width=True)

with col2:
    st.write("가중치 행렬 B")
    st.dataframe(pd.DataFrame(B), use_container_width=True)

st.markdown(
    '<div class="arrow">↓</div>',
    unsafe_allow_html=True
)

st.latex(r"C=A\times B")

st.dataframe(
    pd.DataFrame(C),
    use_container_width=True
)

st.info(
    "위의 계산을 통해 새로운 결과 행렬 C가 만들어진다. "
    "실제 NPU에서는 이러한 연산을 여러 연산 장치가 "
    "나누어 병렬로 처리할 수도 있다."
)

st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)


# -------------------------
# STEP 04. 결과 전달
# -------------------------
st.markdown("""
<div class="step-card">
    <div class="step-number">STEP 04</div>
    <div class="step-title">결과 전달</div>
    <div class="step-description">
    완성된 결과를 다음 인공지능 연산 단계로 전달하는 단계
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
모든 곱셈과 덧셈이 끝나면 최종 결과 행렬이 만들어진다.

이 결과는 다음 신경망 연산 단계로 전달되어
추가적인 계산에 사용될 수 있다.
""")

st.subheader("최종 결과")

st.markdown(
    '<div class="result-box"><b>최종 결과 행렬 C</b></div>',
    unsafe_allow_html=True
)

st.dataframe(
    pd.DataFrame(C),
    use_container_width=True
)

# 연산 횟수
multiply_count = 2 * 2 * 2
addition_count = 2 * 2 * 1

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("입력 데이터", "4개")

with col2:
    st.metric("행렬 크기", "2 × 2")

with col3:
    st.metric("곱셈 횟수", f"{multiply_count}회")

st.write(
    f"누적 덧셈 횟수: **{addition_count}회**"
)

st.success("전체 행렬 연산 과정이 완료되었다!")

st.markdown("---")


# -------------------------
# 전체 처리 과정 정리
# -------------------------
st.subheader("전체 처리 과정 한눈에 보기")

steps = [
    ("01. 데이터 입력", "숫자 형태의 데이터가 반도체에 입력된다."),
    ("02. 행렬 변환", "입력 데이터를 행렬 형태로 구성한다."),
    ("03. 행렬 연산", "숫자를 곱하고 더하여 새로운 값을 계산한다."),
    ("04. 결과 전달", "완성된 결과를 다음 연산 단계로 전달한다.")
]

for title, description in steps:
    st.markdown(f"""
    <div class="process-box">
        <b style="color:#65B9FF;">{title}</b><br><br>
        {description}
    </div>
    """, unsafe_allow_html=True)

st.caption(
    "교육용 시뮬레이터 | NPU의 행렬 연산 기본 원리를 단순화하여 표현한 모델"
)
