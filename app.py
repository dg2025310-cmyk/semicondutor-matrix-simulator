
import streamlit as st
import numpy as np
import pandas as pd

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="NPU MATRIX ENGINE",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. DESIGN SYSTEM
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
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.hero {
    background: linear-gradient(120deg,#102B4B,#0B1930);
    border: 1px solid #23517B;
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    color: #80C8FF;
    letter-spacing: 1px;
}

.hero-sub {
    color: #9BB8D6;
    font-size: 13px;
    letter-spacing: 2px;
}

.panel {
    background: #101F34;
    border: 1px solid #253F5D;
    border-radius: 15px;
    padding: 22px;
    margin-top: 12px;
    margin-bottom: 12px;
}

.step-label {
    color: #46B7FF;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.step-title {
    color: #E5EEFF;
    font-size: 27px;
    font-weight: 750;
    margin-top: 5px;
}

.small-text {
    color: #8FAAC8;
    font-size: 13px;
}

.arrow {
    text-align: center;
    color: #318BCC;
    font-size: 28px;
    margin: 10px;
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

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. HEADER
# ==========================================
st.markdown("""
<div class="hero">
    <div class="hero-sub">
        SEMICONDUCTOR TECHNOLOGY / AI ACCELERATOR
    </div>
    <div class="hero-title">
        NPU MATRIX ENGINE
    </div>
    <p>
        Neural Processing Architecture & Matrix Computation Simulator
    </p>
    <div class="small-text">
        MATRIX MULTIPLICATION · MAC · PARALLEL PROCESSING
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. PIPELINE OVERVIEW
# ==========================================
st.markdown("### PROCESSING PIPELINE")

pipeline = st.columns(4)

steps = [
    ("01", "DATA INPUT"),
    ("02", "MATRIX MAPPING"),
    ("03", "PARALLEL COMPUTING"),
    ("04", "OUTPUT ANALYSIS")
]

for col, (number, name) in zip(pipeline, steps):
    with col:
        st.markdown(f"""
        <div class="panel">
            <div class="step-label">STEP {number}</div>
            <b>{name}</b>
        </div>
        """, unsafe_allow_html=True)

st.divider()


# ==========================================
# STEP 01. DATA INPUT
# ==========================================
st.markdown("""
<div class="panel">
    <div class="step-label">STEP 01 / INPUT STAGE</div>
    <div class="step-title">데이터 입력</div>
    <p>Input Data & Weight Configuration</p>
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
    st.markdown("#### INPUT MATRIX A")

    df_A = st.data_editor(
        pd.DataFrame(
            default_A,
            columns=["C1", "C2", "C3", "C4"]
        ),
        key="input_A",
        use_container_width=True,
        num_rows="fixed"
    )

with col_b:
    st.markdown("#### WEIGHT MATRIX B")

    df_B = st.data_editor(
        pd.DataFrame(
            default_B,
            columns=["C1", "C2", "C3", "C4"]
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
DATA TYPE : SIGNED INTEGER / EDUCATIONAL INPUT
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# STEP 02. MATRIX MAPPING
# ==========================================
st.markdown("""
<div class="panel">
    <div class="step-label">STEP 02 / MAPPING STAGE</div>
    <div class="step-title">행렬 변환 및 데이터 배치</div>
    <p>Matrix Mapping & Data Arrangement</p>
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
    st.markdown("#### MATRIX A")
    st.dataframe(pd.DataFrame(A), use_container_width=True)

with map2:
    st.markdown("#### OPERATION")
    st.markdown(
        "<h2 style='text-align:center;color:#55B9FF'>×</h2>",
        unsafe_allow_html=True
    )

with map3:
    st.markdown("#### MATRIX B")
    st.dataframe(pd.DataFrame(B), use_container_width=True)

st.markdown("""
<div class="panel">
    <b>DATA MAPPING PRINCIPLE</b>
    <p>
    행렬 A의 각 행과 행렬 B의 각 열이 서로 대응한다.
    대응하는 원소들은 곱셈과 누적 덧셈을 통해
    결과 행렬의 한 원소를 생성한다.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# STEP 03. PARALLEL COMPUTING
# ==========================================
st.markdown("""
<div class="panel">
    <div class="step-label">STEP 03 / COMPUTING STAGE</div>
    <div class="step-title">병렬 행렬 연산</div>
    <p>Processing Element Array & MAC Operation</p>
    <div class="small-text">
    여러 연산 장치가 각각의 행렬 원소를 계산하는 원리를 확인한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 3-1. PE ARRAY ARCHITECTURE")

st.write("""
PE(Processing Element)는 연산을 담당하는 처리 장치다.

이번 시뮬레이터는 결과 행렬의 각 원소를
하나의 PE가 담당하는 4×4 교육용 구조를 사용한다.
""")

C = A @ B

# PE Array
for i in range(4):
    pe_cols = st.columns(4)

    for j in range(4):
        with pe_cols[j]:
            st.markdown(f"""
            <div class="pe">
                <div class="pe-name">PE {i+1}-{j+1}</div>
                <div class="pe-value">{C[i,j]}</div>
            </div>
            """, unsafe_allow_html=True)

st.caption(
    "각 PE에 표시된 숫자는 해당 위치의 최종 연산 결과다. "
    "이는 병렬 연산 원리를 설명하기 위한 논리적 매핑이다."
)

st.divider()

# MAC Operation
st.markdown("### 3-2. MAC COMPUTATION")

st.write("""
MAC은 Multiply-Accumulate의 약자다.
곱셈 결과를 누적해서 더하는 연산 구조다.
""")

row = st.selectbox(
    "연산 과정을 확인할 PE의 행",
    range(4),
    format_func=lambda x: f"ROW {x+1}"
)

col = st.selectbox(
    "연산 과정을 확인할 PE의 열",
    range(4),
    format_func=lambda x: f"COLUMN {x+1}"
)

total = 0
mac_data = []

for k in range(4):
    product = int(A[row, k] * B[k, col])
    previous = total
    total += product

    mac_data.append({
        "연산 단계": f"MAC {k+1}",
        "A 데이터": int(A[row, k]),
        "B 데이터": int(B[k, col]),
        "곱셈 결과": product,
        "누적 결과": total
    })

    st.markdown(f"**MAC UNIT {k+1}**")

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
    f"PE {row+1}-{col+1} 최종 출력값 : {total}"
)

st.divider()

# Parallel processing explanation
st.markdown("### 3-3. PARALLEL PROCESSING")

st.markdown("""
<div class="panel">
    <b>PARALLEL COMPUTING PRINCIPLE</b>
    <p>
    4×4 결과 행렬에는 총 16개의 출력 원소가 존재한다.
    각 출력 원소의 계산을 서로 다른 PE에 배정하면
    여러 결과를 병렬로 계산할 수 있다.
    </p>
    <p>
    각 PE는 4개의 곱셈과 누적 과정을 수행한다.
    </p>
</div>
""", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    st.metric("PE UNITS", "16")

with p2:
    st.metric("MAC PER PE", "4")

with p3:
    st.metric("TOTAL MAC", "64")

st.caption("""
※ 이 수치는 16개 PE에 출력 원소를 하나씩 배정한 교육용 가정이다.
실제 NPU의 PE 개수, 데이터 흐름, 병렬화 방식은 설계에 따라 달라진다.
""")

st.divider()


# ==========================================
# STEP 04. OUTPUT ANALYSIS
# ==========================================
st.markdown("""
<div class="panel">
    <div class="step-label">STEP 04 / OUTPUT STAGE</div>
    <div class="step-title">결과 전달 및 연산 분석</div>
    <p>Output Matrix & Performance Analysis</p>
    <div class="small-text">
    행렬 연산의 최종 결과와 계산 구조를 분석한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 4-1. FINAL OUTPUT MATRIX")

st.dataframe(
    pd.DataFrame(
        C,
        index=["ROW 1", "ROW 2", "ROW 3", "ROW 4"],
        columns=["COL 1", "COL 2", "COL 3", "COL 4"]
    ),
    use_container_width=True
)

st.markdown("""
<div class="result-box">
    <h3 style="color:#72E2C2">PROCESSING COMPLETED</h3>
    <p>
    입력 행렬과 가중치 행렬의 곱셈이 완료되었다.
    생성된 결과는 다음 신경망 연산 단계 등으로 전달될 수 있다.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Performance Analysis
st.markdown("### 4-2. COMPUTATION ANALYSIS")

multiplications = 4 * 4 * 4
accumulations = 4 * 4 * 3
total_macs = 4 * 4 * 4
total_arithmetic = multiplications + accumulations

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("MULTIPLICATIONS", f"{multiplications}")

with m2:
    st.metric("ACCUMULATIONS", f"{accumulations}")

with m3:
    st.metric("OUTPUT ELEMENTS", "16")

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
    <b>RESULT INTERPRETATION</b>
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

# Final Summary
st.markdown("### SYSTEM SUMMARY")

st.write("""
| 처리 단계 | 주요 역할 |
|---|---|
| DATA INPUT | 입력 데이터와 가중치 설정 |
| MATRIX MAPPING | 행렬 구성 및 데이터 배치 |
| PARALLEL COMPUTING | PE Array를 통한 MAC 연산 |
| OUTPUT ANALYSIS | 결과 행렬 생성 및 연산량 분석 |
""")

st.caption(
    "NPU MATRIX ENGINE | EDUCATIONAL SIMULATION "
    "| 실제 NPU 회로를 그대로 재현한 것은 아님"
)
