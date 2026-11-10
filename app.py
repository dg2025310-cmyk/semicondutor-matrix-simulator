
import streamlit as st
import numpy as np
import pandas as pd

# ==========================================
# 1. 화면 설정
# ==========================================
st.set_page_config(
    page_title="NPU 행렬 연산 시뮬레이터",
    page_icon="⚡",
    layout="centered"
)

# ==========================================
# 2. 디자인 설정
# ==========================================
st.markdown("""
<style>
.stApp {
    background: #07111F;
    color: #E5EEFF;
}

[data-testid="stHeader"] {
    background: #07111F;
}

h1, h2, h3, h4 {
    color: #E5EEFF !important;
}

p, label {
    color: #C2D3E9;
}

.block-container {
    max-width: 920px;
    padding: 1.4rem 1.2rem 3rem 1.2rem;
}

.hero {
    background: linear-gradient(120deg,#102B4B,#0B1930);
    border: 1px solid #23517B;
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 30px;
    font-weight: 800;
    color: #80C8FF;
    letter-spacing: 1px;
}

.hero-sub {
    color: #9BB8D6;
    font-size: 13px;
    letter-spacing: 1px;
}

.panel {
    background: #101F34;
    border: 1px solid #253F5D;
    border-radius: 15px;
    padding: 18px;
    margin-top: 10px;
    margin-bottom: 10px;
}

.step-label {
    color: #46B7FF;
    font-size: 12px;
    font-weight: 800;
}

.step-title {
    color: #E5EEFF;
    font-size: 23px;
    font-weight: 750;
    margin-top: 5px;
}

.small-text {
    color: #8FAAC8;
    font-size: 13px;
}

.pe {
    background: #142D49;
    border: 1px solid #3274A7;
    border-radius: 8px;
    padding: 10px 3px;
    text-align: center;
    margin: 2px;
}

.pe-name {
    color: #6CAEE5;
    font-size: 10px;
}

.pe-value {
    color: #FFFFFF;
    font-size: 19px;
    font-weight: bold;
}

.result-box {
    background: #102C36;
    border: 1px solid #268A78;
    padding: 20px;
    border-radius: 13px;
}

.stButton button {
    background: #1769AA;
    color: white;
    border: 1px solid #318BCC;
    border-radius: 9px;
    height: 43px;
}

div[data-testid="stMetric"] {
    background: #10243B;
    border: 1px solid #294A6A;
    padding: 16px;
    border-radius: 12px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #294A6A;
    border-radius: 10px;
}

hr {
    border-color: #29415E;
}

[data-testid="stHorizontalBlock"] {
    gap: 0.8rem;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .hero {
        padding: 18px;
    }

    .hero-title {
        font-size: 25px;
    }

    .step-title {
        font-size: 20px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. 상단 제목
# ==========================================
st.markdown("""
<div class="hero">
    <div class="hero-sub">
        반도체 기술 / 인공지능 연산 장치
    </div>
    <div class="hero-title">
        NPU 행렬 연산 시뮬레이터
    </div>
    <p>
        신경망 처리 구조와 행렬 계산 원리 체험
    </p>
    <div class="small-text">
        행렬 곱셈 · 곱셈 누적 연산 · 병렬 처리
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. 처리 과정 안내
# ==========================================
st.markdown("### 전체 처리 과정")

steps = [
    ("01", "데이터 입력"),
    ("02", "행렬 배치"),
    ("03", "병렬 연산"),
    ("04", "결과 분석")
]

for index in range(0, 4, 2):
    pipeline_row = st.columns(2)

    for col, (number, name) in zip(
        pipeline_row, steps[index:index + 2]
    ):
        with col:
            st.markdown(f"""
            <div class="panel">
                <div class="step-label">{number}단계</div>
                <b>{name}</b>
            </div>
            """, unsafe_allow_html=True)

st.divider()


# ==========================================
# 1단계. 데이터 입력
# ==========================================
st.markdown("""
<div class="panel">
    <div class="step-label">1단계 / 입력 과정</div>
    <div class="step-title">데이터 입력</div>
    <p>입력 데이터와 가중치 설정</p>
    <div class="small-text">
    입력 데이터와 가중치 데이터를 설정한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
인공지능 연산에서는 입력 데이터와 학습된 가중치가
행렬 연산에 사용된다.

아래 숫자는 원리를 이해하기 위한 예시 데이터이며,
직접 수정하여 결과를 비교할 수 있다.
""")

default_A = np.array([
    [1, 2, 3, 4],
    [2, 1, 4, 3],
    [3, 2, 1, 4],
    [4, 3, 2, 1]
])

default_B = np.array([
    [1, 0, 2, 1],
    [0, 1, 1, 2],
    [2, 1, 0, 1],
    [1, 2, 1, 0]
])

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### 입력 행렬 A")

    df_A = st.data_editor(
        pd.DataFrame(
            default_A,
            columns=["1열", "2열", "3열", "4열"]
        ),
        key="input_A",
        use_container_width=True,
        num_rows="fixed"
    )

with col_b:
    st.markdown("#### 가중치 행렬 B")

    df_B = st.data_editor(
        pd.DataFrame(
            default_B,
            columns=["1열", "2열", "3열", "4열"]
        ),
        key="input_B",
        use_container_width=True,
        num_rows="fixed"
    )

try:
    A_float = df_A.to_numpy(dtype=float)
    B_float = df_B.to_numpy(dtype=float)

    if not np.all(np.isfinite(A_float)) or not np.all(np.isfinite(B_float)):
        raise ValueError("유효하지 않은 숫자")

    if not np.all(A_float == np.floor(A_float)) or not np.all(B_float == np.floor(B_float)):
        raise ValueError("정수만 입력 가능")

    if np.max(np.abs(A_float)) > 127 or np.max(np.abs(B_float)) > 127:
        raise ValueError("입력 범위 초과")

    A = A_float.astype(np.int64)
    B = B_float.astype(np.int64)

except (ValueError, TypeError):
    st.error("행렬에는 -127부터 127까지의 정수만 입력해 주세요.")
    st.stop()

st.markdown("""
<div class="small-text">
데이터 형식 : 부호가 있는 정수 / 교육용 입력 데이터
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# 2단계. 행렬 배치
# ==========================================
st.markdown("""
<div class="panel">
    <div class="step-label">2단계 / 데이터 배치 과정</div>
    <div class="step-title">행렬 변환 및 데이터 배치</div>
    <p>행렬 구성과 데이터 배열</p>
    <div class="small-text">
    입력된 데이터를 연산 가능한 행렬 구조로 구성한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
두 행렬의 곱셈을 수행하려면 첫 번째 행렬의 열 개수와
두 번째 행렬의 행 개수가 같아야 한다.

현재 두 행렬은 4×4 구조이므로 결과도 4×4 행렬이 된다.
""")

map1, map2, map3 = st.columns([1, 0.5, 1])

with map1:
    st.markdown("#### 행렬 A")
    st.dataframe(pd.DataFrame(A), use_container_width=True)

with map2:
    st.markdown("#### 연산")
    st.markdown(
        "<h2 style='text-align:center;color:#55B9FF'>×</h2>",
        unsafe_allow_html=True
    )

with map3:
    st.markdown("#### 행렬 B")
    st.dataframe(pd.DataFrame(B), use_container_width=True)

st.markdown("""
<div class="panel">
    <b>데이터 배치 원리</b>
    <p>
    행렬 A의 각 행과 행렬 B의 각 열이 서로 대응한다.
    대응하는 원소들은 곱셈과 누적 덧셈을 통해
    결과 행렬의 한 원소를 생성한다.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# 3단계. 병렬 연산
# ==========================================
st.markdown("""
<div class="panel">
    <div class="step-label">3단계 / 연산 과정</div>
    <div class="step-title">병렬 행렬 연산</div>
    <p>연산 처리 장치 배열과 곱셈 누적 연산</p>
    <div class="small-text">
    여러 연산 장치가 각각의 행렬 원소를 계산하는 원리를 확인한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 3-1. 연산 처리 장치 배열 구조")

st.write("""
PE(연산 처리 장치)는 연산을 담당하는 처리 장치다.

이번 시뮬레이터는 결과 행렬의 각 원소를
하나의 PE가 담당하는 4×4 교육용 구조를 사용한다.
""")

C = A @ B

# 연산 처리 장치 배열
for i in range(4):
    pe_cols = st.columns(4)

    for j in range(4):
        with pe_cols[j]:
            st.markdown(f"""
            <div class="pe">
                <div class="pe-name">처리 장치 {i+1}-{j+1}</div>
                <div class="pe-value">{C[i,j]}</div>
            </div>
            """, unsafe_allow_html=True)

st.caption(
    "각 처리 장치에 표시된 숫자는 해당 위치의 최종 연산 결과다. "
    "이는 병렬 연산 원리를 설명하기 위한 논리적 배치다."
)

st.divider()


# ==========================================
# 곱셈 및 누적 연산
# ==========================================
st.markdown("### 3-2. 곱셈 및 누적 연산")

st.write("""
곱셈 누적 연산은 곱셈 결과를 차례대로 더하는 연산 구조다.
""")

row = st.selectbox(
    "연산 과정을 확인할 처리 장치의 행",
    range(4),
    format_func=lambda x: f"{x+1}행"
)

col = st.selectbox(
    "연산 과정을 확인할 처리 장치의 열",
    range(4),
    format_func=lambda x: f"{x+1}열"
)

total = 0
mac_data = []

for k in range(4):
    product = int(A[row, k] * B[k, col])
    previous = total
    total += product

    mac_data.append({
        "연산 단계": f"{k+1}단계",
        "A 데이터": int(A[row, k]),
        "B 데이터": int(B[k, col]),
        "곱셈 결과": product,
        "누적 결과": total
    })

    st.markdown(f"**{k+1}번째 연산 과정**")

    st.code(
        f"{A[row,k]} × {B[k,col]} = {product}\n"
        f"{previous} + {product} = {total}"
    )

st.dataframe(
    pd.DataFrame(mac_data),
    use_container_width=True,
    hide_index=True
)

st.success(
    f"{row+1}행 {col+1}열의 최종 결과값 : {total}"
)

st.divider()


# ==========================================
# 3-3. 병렬 처리 원리
# ==========================================
st.markdown("### 3-3. 병렬 처리 원리")

st.markdown("""
<div class="panel">
    <b>병렬 연산 원리</b>
    <p>
    4×4 결과 행렬에는 총 16개의 출력 원소가 존재한다.
    각 출력 원소의 계산을 서로 다른 처리 장치에 배정하면
    여러 결과를 병렬로 계산할 수 있다.
    </p>
    <p>
    각 처리 장치는 4개의 곱셈과 누적 과정을 수행한다.
    </p>
</div>
""", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    st.metric("연산 장치 수", "16개")

with p2:
    st.metric("장치당 곱셈 횟수", "4회")

with p3:
    st.metric("전체 곱셈 횟수", "64회")

st.caption("""
※ 이 수치는 16개 처리 장치에 출력 원소를 하나씩 배정한 교육용 가정이다.
실제 NPU의 처리 장치 개수, 데이터 흐름, 병렬화 방식은 설계에 따라 달라진다.
""")

st.divider()


# ==========================================
# 4단계. 결과 분석
# ==========================================
st.markdown("""
<div class="panel">
    <div class="step-label">4단계 / 결과 확인 과정</div>
    <div class="step-title">결과 전달 및 연산 분석</div>
    <p>최종 행렬과 연산량 분석</p>
    <div class="small-text">
    행렬 연산의 최종 결과와 계산 구조를 분석한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 4-1. 최종 결과 행렬")

st.dataframe(
    pd.DataFrame(
        C,
        index=["1행", "2행", "3행", "4행"],
        columns=["1열", "2열", "3열", "4열"]
    ),
    use_container_width=True
)

st.markdown("""
<div class="result-box">
    <h3 style="color:#72E2C2">연산 완료</h3>
    <p>
    입력 행렬과 가중치 행렬의 곱셈이 완료되었다.
    생성된 결과는 다음 신경망 연산 단계 등으로 전달될 수 있다.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# 4-2. 연산량 분석
# ==========================================
st.markdown("### 4-2. 연산량 분석")

multiplications = 4 * 4 * 4
accumulations = 4 * 4 * 3
total_macs = 4 * 4 * 4

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("곱셈 횟수", f"{multiplications}회")

with m2:
    st.metric("누적 덧셈 횟수", f"{accumulations}회")

with m3:
    st.metric("결과 원소 개수", "16개")

st.markdown("#### 연산량 구성")

analysis = pd.DataFrame({
    "연산 종류": [
        "곱셈",
        "누적 덧셈"
    ],
    "연산 횟수": [
        multiplications,
        accumulations
    ]
})

st.bar_chart(
    analysis,
    x="연산 종류",
    y="연산 횟수"
)

st.markdown("""
<div class="panel">
    <b>결과 해석</b>
    <p>
    4×4 행렬 곱셈은 16개의 결과 원소를 생성한다.
    각 결과 원소마다 4번의 곱셈이 필요하므로
    전체 곱셈 횟수는 64회다.
    </p>
    <p>
    각 결과 원소에서 첫 번째 곱셈 결과를 누적값으로 사용하고,
    나머지 3개의 결과를 더하므로 누적 덧셈은 총 48회다.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# 최종 시스템 요약
# ==========================================
st.markdown("### 전체 시스템 요약")

st.write("""
| 처리 단계 | 주요 역할 |
|---|---|
| 데이터 입력 | 입력 데이터와 가중치 설정 |
| 행렬 배치 | 행렬 구성 및 데이터 배치 |
| 병렬 연산 | 처리 장치를 통한 곱셈 누적 연산 |
| 결과 분석 | 결과 행렬 생성 및 연산량 분석 |
""")

st.caption(
    "NPU 행렬 연산 시뮬레이터 | 교육용 모의 실험 "
    "| 실제 NPU 회로를 그대로 재현한 것은 아님"
)
