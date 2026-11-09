
import streamlit as st
import numpy as np

# ==========================================
# 1. 페이지 기본 설정
# ==========================================

st.set_page_config(
    page_title="CMOS Signal Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 네이비 테마 디자인
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #101A2E;
    color: #EAF2FF;
}

header[data-testid="stHeader"] {
    background-color: #101A2E;
}

section[data-testid="stSidebar"] {
    background-color: #16243D;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3 {
    color: #F0F6FF !important;
}

p, label, li {
    color: #C4D2E5;
}

div[data-testid="stMetric"] {
    background-color: #1B2B46;
    border: 1px solid #304969;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #9DB7D8;
}

div[data-testid="stMetricValue"] {
    color: #66D9EF;
}

div[data-testid="stExpander"] {
    background-color: #1B2B46;
    border: 1px solid #304969;
    border-radius: 12px;
}

div[data-testid="stTabs"] button {
    color: #C4D2E5;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

.stButton button {
    background-color: #2478B8;
    color: white;
    border: none;
    border-radius: 9px;
    min-height: 42px;
}

.stButton button:hover {
    background-color: #329BD5;
    color: white;
}

div[data-testid="stNumberInput"] input {
    background-color: #203451;
    color: white;
}

hr {
    border-color: #304969;
}

.matrix-card {
    background: #1B2B46;
    border: 1px solid #345477;
    border-radius: 14px;
    padding: 17px;
    margin-bottom: 12px;
}

.matrix-title {
    color: #79D9F2;
    font-size: 15px;
    font-weight: bold;
    margin-bottom: 12px;
}

.matrix-table {
    display: grid;
    grid-template-columns: repeat(2, minmax(55px, 1fr));
    gap: 8px;
}

.matrix-cell {
    background: #263D5D;
    color: #FFFFFF;
    text-align: center;
    padding: 13px 5px;
    border-radius: 8px;
    font-size: 17px;
    font-weight: bold;
}

.process-card {
    background: #1B2B46;
    border-left: 4px solid #42BCE8;
    border-radius: 10px;
    padding: 16px;
    margin: 10px 0;
}

.process-label {
    color: #70D7EF;
    font-size: 12px;
    font-weight: bold;
}

.process-description {
    color: #D4E1F1;
    font-size: 14px;
    line-height: 1.7;
}

.small-note {
    color: #9DB7D8;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. 행렬 화면 출력 함수
# ==========================================

def show_matrix(title, matrix, digits=1):

    st.markdown(
        f'<div class="matrix-card">'
        f'<div class="matrix-title">{title}</div>'
        f'<div class="matrix-table">',
        unsafe_allow_html=True
    )

    for row in matrix:
        for value in row:
            number = f"{value:.{digits}f}"

            st.markdown(
                f'<div class="matrix-cell">{number}</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '</div></div>',
        unsafe_allow_html=True
    )


def process_card(number, title, description):

    st.markdown(
        f"""
        <div class="process-card">
            <div class="process-label">
                STEP {number}
            </div>
            <h4>{title}</h4>
            <div class="process-description">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 4. 상단 제목
# ==========================================

st.markdown(
    '<p style="color:#67CDEB; font-weight:bold;">'
    'SEMICONDUCTOR EDUCATION LAB'
    '</p>',
    unsafe_allow_html=True
)

st.title("CMOS SIGNAL LAB")

st.markdown(
    "### 반도체 이미지 센서 신호 처리 시뮬레이터"
)

st.caption(
    "CMOS Image Sensor · Digital Signal · Matrix Processing"
)

st.divider()


# ==========================================
# 5. 핵심 정보 표시
# ==========================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("센서 배열", "2 × 2 PIXELS")
c2.metric("처리 방식", "MATRIX")
c3.metric("디지털 변환", "ADC")
c4.metric("출력 범위", "0 ~ 255")

st.divider()


# ==========================================
# 6. 사이드바 센서 설정
# ==========================================

st.sidebar.title("⚙️ SENSOR CONTROL")

st.sidebar.caption("센서 입력값과 처리 조건을 설정하세요.")

st.sidebar.subheader("① 픽셀 밝기 입력")

default_values = [
    [80, 120],
    [160, 200]
]

pixel_values = []

for i in range(2):

    row = []

    cols = st.sidebar.columns(2)

    for j in range(2):

        value = cols[j].number_input(
            f"P{i+1}{j+1}",
            min_value=0,
            max_value=100,
            value=default_values[i][j],
            key=f"pixel_{i}_{j}"
        )

        row.append(value)

    pixel_values.append(row)

light_matrix = np.array(pixel_values, dtype=float)

st.sidebar.divider()

st.sidebar.subheader("② 센서 설정")

exposure = st.sidebar.slider(
    "빛 감도 설정",
    0.5,
    2.0,
    1.0,
    0.1
)

adc_bits = st.sidebar.selectbox(
    "ADC 해상도",
    [8, 10, 12],
    index=0
)

st.sidebar.divider()

st.sidebar.subheader("③ 신호 처리 계수")

gain = st.sidebar.slider(
    "신호 증폭 계수",
    0.5,
    2.0,
    1.0,
    0.1
)

offset = st.sidebar.slider(
    "신호 보정값",
    -30,
    30,
    0,
    1
)

st.sidebar.caption(
    "※ 모든 수치는 교육용 모델을 위한 설정값입니다."
)


# ==========================================
# 7. 센서 및 ADC 계산
# ==========================================

# 빛의 세기에 따른 가상 전압
voltage = np.clip(
    light_matrix * exposure * 3.3 / 100,
    0,
    3.3
)

# ADC 디지털 변환
max_adc = (2 ** adc_bits) - 1

adc_matrix = np.rint(
    voltage / 3.3 * max_adc
)

# 8비트 밝기값으로 정규화
digital_matrix = (
    adc_matrix / max_adc * 255
)


# ==========================================
# 8. 신호 처리 행렬
# ==========================================

B = np.array([
    [1.2, 0.1],
    [0.1, 1.1]
])

B = B * gain

# 행렬 곱셈
matrix_result = digital_matrix @ B

# 보정값 추가
corrected_matrix = matrix_result + offset

# 디지털 출력 범위 제한
final_matrix = np.clip(
    corrected_matrix,
    0,
    255
)


# ==========================================
# 9. 상단 메뉴
# ==========================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📡 전체 처리 과정",
    "🔢 행렬 계산 분석",
    "📊 데이터 비교",
    "🧠 반도체 원리"
])


# ==========================================
# TAB 1. 전체 처리 과정
# ==========================================

with tab1:

    st.header("반도체 신호 처리 PROCESS")

    st.write(
        "빛이 센서에 들어온 순간부터 최종 디지털 데이터가 "
        "만들어지는 과정까지 단계별로 확인할 수 있습니다."
    )

    st.markdown("## STEP 01. 빛 감지")

    process_card(
        "01",
        "포토다이오드의 빛 감지",
        "CMOS 이미지 센서의 각 픽셀에는 포토다이오드가 "
        "있습니다. 빛이 들어오면 광전 효과에 의해 "
        "전하가 생성됩니다. 빛의 양이 달라지면 "
        "생성되는 전하량도 달라집니다."
    )

    show_matrix(
        "픽셀별 빛의 세기 (%)",
        light_matrix,
        0
    )

    st.markdown("## STEP 02. 전기 신호 생성")

    process_card(
        "02",
        "광전 변환 모델",
        "포토다이오드에서 생성되는 전하를 이용하여 "
        "전기 신호를 얻습니다. 아래 전압은 실제 소자의 "
        "정확한 출력값이 아니라 빛의 세기에 비례한다고 "
        "가정한 교육용 모델입니다."
    )

    show_matrix(
        "가상 전압 행렬 (V)",
        voltage,
        3
    )

    st.markdown("## STEP 03. ADC 디지털 변환")

    process_card(
        "03",
        "아날로그-디지털 변환",
        "ADC는 연속적인 아날로그 신호를 "
        "일정한 단계의 디지털 숫자로 변환합니다. "
        "해상도가 높을수록 표현할 수 있는 단계가 많아집니다."
    )

    st.write(f"현재 ADC 해상도: {adc_bits} bit")
    st.write(f"표현 가능한 단계 수: {max_adc + 1:,}개")

    show_matrix(
        "ADC 변환 결과",
        adc_matrix,
        0
    )

    st.markdown("## STEP 04. 디지털 데이터 정규화")

    process_card(
        "04",
        "데이터 정규화",
        "ADC의 출력값을 0~255 범위의 밝기 데이터로 "
        "변환합니다. 서로 다른 ADC 해상도의 결과를 "
        "동일한 범위에서 비교하기 위한 과정입니다."
    )

    show_matrix(
        "정규화된 디지털 데이터",
        digital_matrix,
        1
    )

    st.markdown("## STEP 05. 행렬연산 및 신호 처리")

    process_card(
        "05",
        "행렬 곱셈",
        "디지털 데이터 행렬에 처리 계수 행렬을 곱합니다. "
        "이 과정을 통해 여러 데이터가 일정한 수학적 "
        "규칙에 따라 변환되는 모습을 확인할 수 있습니다."
    )

    show_matrix(
        "신호 처리 행렬 B",
        B,
        2
    )

    show_matrix(
        "행렬 곱셈 결과",
        matrix_result,
        2
    )

    st.markdown("## STEP 06. 신호 보정 및 최종 출력")

    process_card(
        "06",
        "디지털 신호 보정",
        "행렬연산 결과에 보정값을 더합니다. "
        "이후 0~255 범위로 제한하여 최종 밝기 데이터를 "
        "만듭니다. 이는 실제 영상 처리의 보정 개념을 "
        "단순화한 예시입니다."
    )

    show_matrix(
        "최종 출력 데이터",
        final_matrix,
        1
    )

    st.success("전체 신호 처리 과정 확인 완료!")


# ==========================================
# TAB 2. 행렬 계산 분석
# ==========================================

with tab2:

    st.header("MATRIX PROCESSING ANALYSIS")

    st.write(
        "실제 숫자가 어떤 계산을 거쳐 최종 결과가 되는지 "
        "하나씩 살펴봅니다."
    )

    st.subheader("① 입력 행렬")

    col1, col2 = st.columns(2)

    with col1:
        show_matrix(
            "입력 데이터 A",
            digital_matrix,
            1
        )

    with col2:
        show_matrix(
            "처리 계수 B",
            B,
            2
        )

    st.subheader("② 행렬 곱셈 계산")

    st.latex(
        r"C=A\times B"
    )

    for i in range(2):

        for j in range(2):

            a = digital_matrix[i][0]
            b = digital_matrix[i][1]

            x = B[0][j]
            y = B[1][j]

            first = a * x
            second = b * y

            with st.expander(
                f"C[{i+1},{j+1}] 계산 과정 보기"
            ):

                st.write(
                    f"첫 번째 곱셈: {a:.2f} × {x:.2f}"
                )

                st.write(
                    f"두 번째 곱셈: {b:.2f} × {y:.2f}"
                )

                st.latex(
                    rf"{first:.2f}+{second:.2f}"
                    rf"={matrix_result[i][j]:.2f}"
                )

    st.subheader("③ 행렬 곱셈 최종 결과")

    show_matrix(
        "계산 결과 C",
        matrix_result,
        2
    )

    st.subheader("④ 보정 과정")

    st.latex(
        r"D=\operatorname{clip}(C+\text{offset},0,255)"
    )

    st.write(f"현재 보정값: {offset}")

    show_matrix(
        "최종 출력 D",
        final_matrix,
        2
    )


# ==========================================
# TAB 3. 데이터 비교
# ==========================================

with tab3:

    st.header("BEFORE & AFTER")

    st.write(
        "행렬연산 전후의 데이터가 어떻게 달라졌는지 "
        "한눈에 비교합니다."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("처리 전")

        show_matrix(
            "입력 데이터",
            digital_matrix,
            1
        )

    with col2:

        st.subheader("처리 후")

        show_matrix(
            "최종 데이터",
            final_matrix,
            1
        )

    st.divider()

    st.subheader("픽셀별 데이터 변화")

    for i in range(2):

        for j in range(2):

            before = digital_matrix[i][j]
            after = final_matrix[i][j]

            st.write(
                f"픽셀 P{i+1}{j+1}: "
                f"{before:.1f} → {after:.1f}"
            )

            st.progress(
                float(after / 255)
            )

    st.divider()

    st.subheader("데이터 변화 그래프")

    st.line_chart({
        "처리 전": digital_matrix.flatten(),
        "처리 후": final_matrix.flatten()
    })


# ==========================================
# TAB 4. 반도체 원리
# ==========================================

with tab4:

    st.header("SEMICONDUCTOR KNOWLEDGE")

    st.subheader("① CMOS 이미지 센서")

    st.write("""
    CMOS 이미지 센서는 빛을 감지하여 전기 신호로 변환하는
    반도체 소자입니다.

    각 픽셀에는 포토다이오드와 신호 판독에 필요한
    트랜지스터 등이 사용됩니다.
    """)

    st.subheader("② 포토다이오드")

    st.write("""
    포토다이오드는 빛을 받으면 광전 효과에 의해
    전하를 생성합니다.

    빛의 세기와 노출 조건에 따라 생성되는 전하량이 달라지고,
    이를 이용하여 영상 정보를 얻을 수 있습니다.
    """)

    st.subheader("③ ADC")

    st.write("""
    ADC는 아날로그 신호를 디지털 숫자로 바꾸는 장치입니다.

    예를 들어 8비트 ADC는 0부터 255까지 총 256단계로
    신호를 표현할 수 있습니다.
    """)

    st.subheader("④ 행렬연산")

    st.write("""
    이미지의 픽셀 데이터를 행렬로 표현하면
    여러 데이터를 한꺼번에 처리할 수 있습니다.

    행렬 곱셈은 이미지 변환, 필터 처리,
    인공지능 연산 등 다양한 분야에서 활용됩니다.
    """)

    st.subheader("⑤ 실제 기술과의 차이")

    st.warning("""
    이 시뮬레이터는 실제 반도체 제조 공정이나
    CMOS 회로의 전기적 동작을 그대로 재현하지 않습니다.

    빛 감지부터 디지털 데이터 처리까지의 개념을
    이해하기 위해 단순화한 교육용 모델입니다.
    """)


# ==========================================
# 10. 하단 안내
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#8EA9CA;">
        SEMICONDUCTOR SIGNAL LAB<br>
        CMOS IMAGE SENSOR & MATRIX PROCESSING<br>
        EDUCATIONAL SIMULATION
    </div>
    """,
    unsafe_allow_html=True
)
