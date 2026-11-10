
import streamlit as st
import numpy as np
import pandas as pd

# =====================================
# 1. 기본 설정
# =====================================
st.set_page_config(
    page_title="반도체 행렬 연산 시뮬레이터",
    page_icon="🔬",
    layout="wide"
)

# =====================================
# 2. 디자인 설정
# =====================================
st.markdown("""
<style>
.stApp {
    background-color: #07111F;
    color: #E5EEFF;
}

[data-testid="stHeader"] {
    background: #07111F;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4 {
    color: #E5EEFF !important;
}

p, label {
    color: #C2D3E9;
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
    margin-top: 15px;
    margin-bottom: 15px;
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
    font-size: 30px;
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


# =====================================
# 3. 상단 제목
# =====================================
st.markdown("""
<div class="hero">
    <div class="hero-sub">
        반도체 기술 연구 · 인공지능 연산 구조
    </div>
    <div class="hero-title">
        반도체 행렬 연산 시뮬레이터
    </div>
    <p>
        인공지능 반도체 NPU 내부의 행렬 연산과
        병렬 처리 원리를 시각적으로 분석한다.
    </p>
    <div class="small-text">
        행렬 곱셈 · MAC 연산 · 병렬 처리 · 결과 분석
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================
# 4. 전체 처리 과정
# =====================================
st.markdown("### 전체 처리 과정")

pipeline = st.columns(4)

steps = [
    ("01", "데이터 입력"),
    ("02", "행렬 변환"),
    ("03", "병렬 행렬 연산"),
    ("04", "결과 전달")
]

for col, (number, name) in zip(pipeline, steps):
    with col:
        st.markdown(f"""
        <div class="panel">
            <div class="step-label">단계 {number}</div>
            <b>{name}</b>
        </div>
        """, unsafe_allow_html=True)

st.divider()


# =====================================
# 1단계. 데이터 입력
# =====================================
st.markdown("""
<div class="panel">
    <div class="step-label">01 / 데이터 입력 단계</div>
    <div class="step-title">데이터 입력</div>
    <p>연산에 사용할 입력 데이터와 가중치 설정</p>
    <div class="small-text">
    인공지능 연산에 필요한 숫자 데이터를 준비한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
인공지능 반도체는 이미지, 음성 등의 정보를
숫자 형태로 처리한다.

아래 숫자는 행렬 연산 원리를 이해하기 위한 예시 데이터다.
직접 숫자를 수정하여 계산 결과를 비교할 수 있다.
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
    st.markdown("#### 입력 데이터 행렬 A")

    df_A = st.data_editor(
        pd.DataFrame(
            default_A,
            columns=["열 1", "열 2", "열 3", "열 4"]
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
            columns=["열 1", "열 2", "열 3", "열 4"]
        ),
        key="input_B",
        use_container_width=True,
        num_rows="fixed"
    )

try:
    A_float = df_A.to_numpy(dtype=float)
    B_float = df_B.to_numpy(dtype=float)

    if not np.all(np.isfinite(A_float)) or not np.all(np.isfinite(B_float)):
        raise ValueError

    if not np.all(A_float == np.floor(A_float)):
        raise ValueError

    if not np.all(B_float == np.floor(B_float)):
        raise ValueError

    if np.max(np.abs(A_float)) > 127:
        raise ValueError

    if np.max(np.abs(B_float)) > 127:
        raise ValueError

    A = A_float.astype(np.int64)
    B = B_float.astype(np.int64)

except (ValueError, TypeError):
    st.error("행렬에는 -127부터 127까지의 정수만 입력해 주세요.")
    st.stop()

st.caption("데이터 형식: 정수형 / 교육용 예시 데이터")

st.info("""
입력 데이터는 연산에 필요한 숫자로 구성된다.
가중치 행렬은 실제 인공지능에서는 학습 과정을 통해 정해진다.
""")

st.markdown(
    '<div class="arrow">↓</div>',
    unsafe_allow_html=True
)


# =====================================
# 2단계. 행렬 변환
# =====================================
st.markdown("""
<div class="panel">
    <div class="step-label">02 / 행렬 변환 단계</div>
    <div class="step-title">행렬 변환 및 데이터 배치</div>
    <p>입력 데이터를 연산에 적합한 행렬 구조로 구성</p>
    <div class="small-text">
    행렬의 행과 열을 이용하여 계산할 데이터를 배치한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("""
두 행렬을 곱하려면 첫 번째 행렬의 열 개수와
두 번째 행렬의 행 개수가 같아야 한다.

현재 두 행렬은 모두 4×4 구조다.
따라서 계산 결과도 4×4 행렬로 생성된다.
""")

map1, map2, map3 = st.columns([1, 0.4, 1])

with map1:
    st.markdown("#### 입력 행렬 A")
    st.dataframe(
        pd.DataFrame(A),
        use_container_width=True
    )

with map2:
    st.markdown("#### 연산")
    st.markdown(
        "<h1 style='text-align:center;color:#55B9FF'>×</h1>",
        unsafe_allow_html=True
    )

with map3:
    st.markdown("#### 가중치 행렬 B")
    st.dataframe(
        pd.DataFrame(B),
        use_container_width=True
    )

st.markdown("""
<div class="panel">
    <b>행렬 배치 원리</b>
    <p>
    행렬 A의 각 행과 행렬 B의 각 열이 서로 대응한다.
    대응하는 원소들을 곱하고 더하여 결과 행렬의
    각 위치에 해당하는 값을 계산한다.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="arrow">↓</div>',
    unsafe_allow_html=True
)


# =====================================
# 3단계. 병렬 행렬 연산
# =====================================
st.markdown("""
<div class="panel">
    <div class="step-label">03 / 행렬 연산 단계</div>
    <div class="step-title">병렬 행렬 연산</div>
    <p>연산 처리 장치(PE Array)와 MAC 연산</p>
    <div class="small-text">
    여러 연산 장치가 행렬의 각 결과값을 계산하는 원리를 살펴본다.
    </div>
</div>
""", unsafe_allow_html=True)

C = A @ B

st.markdown("### 3-1. 연산 처리 장치 배열 (PE Array)")

st.write("""
PE(Processing Element)는 개별 계산을 담당하는 처리 장치다.

이번 시뮬레이터에서는 16개의 PE가 결과 행렬의
각 원소 하나씩을 담당하는 구조로 표현한다.
""")

for i in range(4):

    pe_cols = st.columns(4)

    for j in range(4):

        with pe_cols[j]:

            st.markdown(f"""
            <div class="pe">
                <div class="pe-name">연산 장치 {i+1}-{j+1}</div>
                <div class="pe-value">{C[i,j]}</div>
            </div>
            """, unsafe_allow_html=True)

st.caption("""
각 연산 장치에 표시된 숫자는 해당 위치의 최종 계산 결과다.
실제 NPU의 물리적 회로를 그대로 재현한 것은 아니며,
병렬 연산 구조를 이해하기 위한 교육용 모델이다.
""")

st.divider()


# =====================================
# MAC 연산
# =====================================
st.markdown("### 3-2. MAC 연산 과정")

st.write("""
MAC은 곱셈(Multiply)과 누적 덧셈(Accumulate)을
결합한 연산 구조다.

행렬의 한 원소가 계산되는 과정을 단계별로 확인해 보자.
""")

row = st.selectbox(
    "계산할 결과의 행 선택",
    range(4),
    format_func=lambda x: f"{x+1}번째 행"
)

col = st.selectbox(
    "계산할 결과의 열 선택",
    range(4),
    format_func=lambda x: f"{x+1}번째 열"
)

total = 0
mac_data = []

for k in range(4):

    product = int(A[row, k] * B[k, col])
    previous = total
    total += product

    mac_data.append({
        "연산 단계": f"{k+1}단계",
        "입력값 A": int(A[row, k]),
        "가중치 B": int(B[k, col]),
        "곱셈 결과": product,
        "누적 결과": total
    })

    st.markdown(f"**{k+1}번째 곱셈 및 누적 연산**")

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
    f"최종 계산 결과: {total}"
)

st.caption(
    "각 결과 원소는 4회의 곱셈과 3회의 덧셈으로 계산된다."
)

st.divider()


# =====================================
# 병렬 처리 원리
# =====================================
st.markdown("### 3-3. 병렬 연산 구조")

st.write("""
하나의 연산 장치가 모든 계산을 담당하는 대신,
여러 PE가 서로 다른 결과 원소를 나누어 계산할 수 있다.

이를 병렬 처리라고 한다.
""")

p1, p2, p3 = st.columns(3)

with p1:
    st.metric("연산 처리 장치", "16개")

with p2:
    st.metric("장치당 곱셈", "4회")

with p3:
    st.metric("전체 곱셈", "64회")

st.info("""
이 시뮬레이터는 16개의 PE에 결과 행렬의 원소를
하나씩 배정한 교육용 병렬 처리 모델이다.

실제 NPU에서는 설계에 따라 데이터가 이동하는 방식,
연산 장치의 개수와 병렬 처리 구조가 달라진다.
""")

st.markdown(
    '<div class="arrow">↓</div>',
    unsafe_allow_html=True
)


# =====================================
# 4단계. 결과 전달
# =====================================
st.markdown("""
<div class="panel">
    <div class="step-label">04 / 결과 전달 단계</div>
    <div class="step-title">최종 결과 및 연산 분석</div>
    <p>행렬 연산 결과 생성과 계산량 분석</p>
    <div class="small-text">
    연산을 마친 결과 행렬을 확인하고 처리 구조를 분석한다.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 4-1. 최종 결과 행렬")

st.dataframe(
    pd.DataFrame(
        C,
        index=["행 1", "행 2", "행 3", "행 4"],
        columns=["열 1", "열 2", "열 3", "열 4"]
    ),
    use_container_width=True
)

st.success("모든 행렬 계산이 완료되었다.")

st.write("""
생성된 결과 행렬은 다음 신경망 연산 단계 등으로
전달되어 이미지 인식이나 음성 인식과 같은
인공지능 정보 처리에 활용될 수 있다.
""")

st.divider()


# =====================================
# 연산량 분석
# =====================================
st.markdown("### 4-2. 연산량 분석")

multiplications = 4 * 4 * 4
additions = 4 * 4 * 3
output_elements = 4 * 4

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("전체 곱셈 횟수", f"{multiplications}회")

with m2:
    st.metric("전체 덧셈 횟수", f"{additions}회")

with m3:
    st.metric("결과 원소 개수", f"{output_elements}개")

analysis = pd.DataFrame({
    "연산 종류": ["곱셈", "덧셈"],
    "연산 횟수": [multiplications, additions]
})

st.markdown("#### 연산 종류별 횟수 비교")

st.bar_chart(
    analysis,
    x="연산 종류",
    y="연산 횟수"
)

st.markdown("""
<div class="panel">
    <b>연산 결과 해석</b>
    <p>
    4×4 행렬 곱셈에서는 총 16개의 결과 원소가 생성된다.
    각 결과 원소는 4회의 곱셈과 3회의 덧셈을 거친다.
    </p>
    <p>
    따라서 전체 곱셈은 64회, 덧셈은 48회 수행된다.
    </p>
    <p>
    이러한 반복적인 연산을 여러 처리 장치에 분배하면
    병렬 처리를 통해 연산 효율을 높일 수 있다.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# =====================================
# 전체 정리
# =====================================
st.markdown("### 전체 처리 과정 정리")

summary = pd.DataFrame({
    "처리 단계": [
        "01. 데이터 입력",
        "02. 행렬 변환",
        "03. 병렬 행렬 연산",
        "04. 결과 전달"
    ],
    "주요 기능": [
        "입력 데이터와 가중치 설정",
        "행렬 구성 및 데이터 배치",
        "PE Array와 MAC 연산",
        "결과 행렬 생성 및 분석"
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.markdown("""
<div class="hero">
    <div class="hero-title" style="font-size:23px;">
        시뮬레이션 완료
    </div>
    <p>
    데이터 입력부터 행렬 연산과 결과 전달까지,
    NPU의 행렬 처리 원리를 확인하였다.
    </p>
    <div class="small-text">
    교육용 반도체 행렬 연산 시뮬레이터
    </div>
</div>
""", unsafe_allow_html=True)
