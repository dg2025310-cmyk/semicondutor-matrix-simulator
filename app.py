
import streamlit as st
import numpy as np

# -----------------------------
# 기본 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="CMOS 반도체 행렬연산 시뮬레이터",
    page_icon="🔬",
    layout="wide"
)

# -----------------------------
# 화면 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #101A2E;
    color: #F4F7FC;
}

section[data-testid="stSidebar"] {
    background-color: #17243B;
}

h1, h2, h3, p, label {
    color: #F4F7FC !important;
}

[data-testid="stMetric"] {
    background-color: #1D2D49;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #344967;
}

.matrix-card {
    background-color: #1D2D49;
    border: 1px solid #344967;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}

.matrix-title {
    color: #8EC5FF;
    font-weight: bold;
    margin-bottom: 12px;
}

.matrix-table {
    display: grid;
    grid-template-columns: repeat(2, minmax(55px, 1fr));
    gap: 8px;
    max-width: 260px;
}

.matrix-cell {
    background-color: #263B5C;
    color: #FFFFFF;
    padding: 13px;
    text-align: center;
    border-radius: 7px;
    font-weight: bold;
}

.process-card {
    background-color: #1D2D49;
    border-left: 4px solid #55A9FF;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
}

.small-text {
    color: #B9C9DF;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 행렬 출력 함수
# -----------------------------
def show_matrix(title, matrix, digits=1):
    cells = ""

    for row in matrix:
        for value in row:
            number = f"{value:.{digits}f}"
            cells += f'<div class="matrix-cell">{number}</div>'

    html = f"""
    <div class="matrix-card">
        <div class="matrix-title">{title}</div>
        <div class="matrix-table">
            {cells}
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


# -----------------------------
# 제목
# -----------------------------
st.title("🔬 CMOS 반도체 행렬연산 시뮬레이터")

st.markdown(
    "빛을 감지한 이미지 센서의 데이터가 디지털 신호로 변환되고, "
    "행렬연산을 통해 보정되는 과정을 체험해 보는 시뮬레이터입니다."
)

st.divider()


# -----------------------------
# 사용자 입력
# -----------------------------
st.sidebar.header("⚙️ 시뮬레이션 설정")

st.sidebar.subheader("① 픽셀별 빛의 세기")

pixel_11 = st.sidebar.slider("픽셀 1", 0, 100, 80)
pixel_12 = st.sidebar.slider("픽셀 2", 0, 100, 60)
pixel_21 = st.sidebar.slider("픽셀 3", 0, 100, 40)
pixel_22 = st.sidebar.slider("픽셀 4", 0, 100, 90)

light_matrix = np.array([
    [pixel_11, pixel_12],
    [pixel_21, pixel_22]
], dtype=float)

st.sidebar.divider()

st.sidebar.subheader("② 센서 조건")

exposure = st.sidebar.slider(
    "노출 정도",
    0.5, 2.0, 1.0, 0.1
)

adc_bits = st.sidebar.selectbox(
    "ADC 해상도",
    [8, 10, 12]
)

st.sidebar.divider()

st.sidebar.subheader("③ 행렬연산 조건")

gain = st.sidebar.slider(
    "신호 보정 계수",
    0.5, 1.5, 1.0, 0.1
)

offset = st.sidebar.slider(
    "밝기 보정값",
    -50, 50, 0
)


# -----------------------------
# 센서 신호 계산
# -----------------------------

# 빛의 세기를 전압으로 변환
voltage_matrix = light_matrix * exposure * 3.3 / 100
voltage_matrix = np.clip(voltage_matrix, 0, 3.3)

# ADC 변환
max_adc = (2 ** adc_bits) - 1

adc_matrix = np.rint(
    voltage_matrix / 3.3 * max_adc
)

# 0~255 범위로 정규화
digital_matrix = adc_matrix / max_adc * 255

# -----------------------------
# 행렬연산
# -----------------------------

# 신호 처리 행렬
B = np.array([
    [gain, 0.1],
    [0.1, gain]
])

# 행렬 곱셈
matrix_result = digital_matrix @ B

# 밝기 보정
final_matrix = matrix_result + offset

# 출력값 범위 제한
final_matrix = np.clip(final_matrix, 0, 255)


# -----------------------------
# 핵심 수치 표시
# -----------------------------
st.subheader("📊 시뮬레이션 결과")

col1, col2, col3 = st.columns(3)

col1.metric(
    "ADC 해상도",
    f"{adc_bits} bit"
)

col2.metric(
    "최대 디지털 값",
    f"{max_adc}"
)

col3.metric(
    "평균 보정 밝기",
    f"{np.mean(final_matrix):.1f}"
)

st.divider()


# -----------------------------
# 탭 구성
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "전체 처리 과정",
    "행렬 계산 분석",
    "데이터 비교",
    "반도체 원리"
])


# -----------------------------
# TAB 1
# -----------------------------
with tab1:

    st.subheader("이미지 센서 데이터 처리 과정")

    st.markdown("""
    <div class="process-card">
        <b>STEP 1. 빛 감지</b><br>
        CMOS 이미지 센서의 픽셀이 들어오는 빛을 감지합니다.
    </div>

    <div class="process-card">
        <b>STEP 2. 전기 신호 생성</b><br>
        포토다이오드에서 빛에 반응하여 전기적 신호가 만들어집니다.
    </div>

    <div class="process-card">
        <b>STEP 3. ADC 변환</b><br>
        아날로그 신호가 ADC를 통해 디지털 데이터로 변환됩니다.
    </div>

    <div class="process-card">
        <b>STEP 4. 행렬연산</b><br>
        디지털 데이터를 행렬로 표현하고 행렬 곱셈과 보정값을 적용합니다.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    left, right = st.columns(2)

    with left:
        show_matrix("입력된 빛의 세기", light_matrix)

    with right:
        show_matrix("디지털 변환 데이터", digital_matrix)

    left, right = st.columns(2)

    with left:
        show_matrix("행렬연산 결과", matrix_result)

    with right:
        show_matrix("최종 보정 데이터", final_matrix)


# -----------------------------
# TAB 2
# -----------------------------
with tab2:

    st.subheader("행렬 계산 분석")

    st.markdown(
        "디지털 데이터 행렬에 신호 처리 행렬을 곱하는 과정을 확인합니다."
    )

    st.latex(r"A \times B = C")

    left, right = st.columns(2)

    with left:
        show_matrix("A : 디지털 데이터 행렬", digital_matrix)

    with right:
        show_matrix("B : 신호 처리 행렬", B)

    st.markdown("### 행렬 곱셈 결과")

    show_matrix("C = A × B", matrix_result)

    st.markdown("### 밝기 보정")

    st.latex(r"D = C + k")

    st.write(f"현재 밝기 보정값 k = {offset}")

    show_matrix("최종 결과 D", final_matrix)


# -----------------------------
# TAB 3
# -----------------------------
with tab3:

    st.subheader("처리 전후 데이터 비교")

    before, after = st.columns(2)

    with before:
        show_matrix("처리 전 데이터", digital_matrix)

    with after:
        show_matrix("처리 후 데이터", final_matrix)

    st.markdown("### 픽셀별 밝기 변화")

    chart_data = {
        "처리 전": digital_matrix.flatten().tolist(),
        "처리 후": final_matrix.flatten().tolist()
    }

    st.line_chart(chart_data)

    difference = final_matrix - digital_matrix

    show_matrix("밝기 변화량", difference)


# -----------------------------
# TAB 4
# -----------------------------
with tab4:

    st.subheader("CMOS 이미지 센서와 행렬연산")

    st.markdown("""
    ### 1. CMOS 이미지 센서란?

    CMOS 이미지 센서는 카메라에 사용되는 반도체 센서입니다.
    픽셀에 들어오는 빛을 감지하여 전기적 신호로 바꿉니다.

    ### 2. ADC란?

    ADC는 아날로그 신호를 디지털 데이터로 변환하는 장치입니다.
    이 과정에서 빛에 대한 정보가 컴퓨터가 처리할 수 있는 숫자로 바뀝니다.

    ### 3. 행렬연산은 왜 사용될까?

    이미지 데이터는 여러 픽셀의 숫자로 이루어져 있기 때문에
    행렬로 표현할 수 있습니다.

    행렬 곱셈과 덧셈 등의 연산을 이용하면
    이미지의 밝기나 신호를 보정하는 과정을 수학적으로 표현할 수 있습니다.

    ### 4. 이번 시뮬레이션의 의미

    이번 프로그램은 CMOS 이미지 센서의 전체 회로를 재현한 것이 아니라,
    센서에서 만들어진 디지털 데이터가 행렬연산으로 처리되는 원리를
    이해하기 위한 교육용 단순화 모델입니다.
    """)

    st.divider()

    st.info(
        "실제 반도체 내부의 신호 처리 방식은 이 시뮬레이션보다 훨씬 복잡하지만, "
        "행렬연산이 디지털 데이터 처리에 활용되는 기본 원리를 확인할 수 있습니다."
    )


# -----------------------------
# 하단 안내
# -----------------------------
st.divider()

st.caption(
    "CMOS Semiconductor Matrix Simulation | "
    "교육용 시뮬레이션 프로그램"
)
