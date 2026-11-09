import streamlit as st
import numpy as np

# =====================================
# 1. 기본 화면 설정
# =====================================

st.set_page_config(
    page_title="CMOS 반도체 센서 시뮬레이터",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 반도체 CMOS 이미지 센서 시뮬레이터")

st.write(
    "행렬연산을 이용하여 이미지 센서의 "
    "디지털 신호 처리 과정을 체험해 봅시다."
)

st.info(
    "이 프로그램은 실제 CMOS 이미지 센서의 "
    "작동 원리를 단순화한 교육용 시뮬레이션입니다."
)

# =====================================
# 2. 반도체 기본 원리
# =====================================

st.header("1. 반도체 이미지 센서란?")

with st.expander("CMOS 이미지 센서의 작동 원리 알아보기"):
    st.markdown("""
    **① 빛 감지**

    이미지 센서의 픽셀에 빛이 들어오면
    포토다이오드가 빛을 감지합니다.

    **② 전기 신호 생성**

    빛의 세기에 따라 전기 신호가 만들어집니다.

    **③ 디지털 변환**

    ADC(아날로그-디지털 변환기)를 통해
    전기 신호가 디지털 데이터로 변환됩니다.

    **④ 신호 처리**

    변환된 데이터는 보정 및 영상 처리 과정을 거칩니다.
    이 과정에서 행렬연산과 같은 수학적 계산이 활용됩니다.
    """)

st.divider()

# =====================================
# 3. 센서 측정값 설정
# =====================================

st.header("2. 이미지 센서의 픽셀값 설정")

st.write(
    "아래 숫자는 4개의 픽셀이 측정한 밝기를 "
    "0~255 범위의 디지털 값으로 단순화한 것입니다."
)

light = st.slider(
    "빛의 세기 조절",
    min_value=25,
    max_value=150,
    value=100,
    step=5
)

st.write(f"현재 빛의 세기: {light}%")

def input_matrix(title, prefix, defaults, minimum, maximum, step):
    st.subheader(title)

    matrix = []

    for i in range(2):
        cols = st.columns(2)
        row = []

        for j in range(2):
            value = cols[j].number_input(
                f"{prefix} ({i+1},{j+1})",
                min_value=minimum,
                max_value=maximum,
                value=defaults[i][j],
                step=step,
                key=f"{prefix}_{i}_{j}"
            )
            row.append(value)

        matrix.append(row)

    return np.array(matrix, dtype=float)

A = input_matrix(
    "센서 측정 행렬 A",
    "A",
    [[80, 120], [160, 200]],
    0, 255, 1
)

# 빛의 세기에 따른 센서값 변화
sensor = A * (light / 100)

sensor = np.clip(sensor, 0, 255)

st.write("빛의 세기가 반영된 센서 데이터")

st.dataframe(
    np.round(sensor, 1),
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================
# 4. 신호 처리 행렬 설정
# =====================================

st.header("3. 반도체 신호 처리 행렬 설정")

st.write(
    "센서에서 얻은 데이터를 변환하기 위한 "
    "처리 계수 행렬 B를 설정합니다."
)

B = input_matrix(
    "신호 처리 행렬 B",
    "B",
    [[1.2, 0.1], [0.1, 1.1]],
    -2.0, 2.0, 0.1
)

st.caption(
    "행렬 B의 숫자를 바꾸면 센서 데이터의 변환 결과도 달라집니다."
)

st.divider()

# =====================================
# 5. 행렬연산 실행
# =====================================

st.header("4. 행렬연산 시뮬레이션")

operation = st.radio(
    "실행할 연산을 선택하세요.",
    ["행렬 곱셈", "행렬 덧셈"],
    horizontal=True
)

if operation == "행렬 곱셈":
    raw_result = sensor @ B
    st.write("센서 데이터와 처리 행렬의 곱셈")
else:
    raw_result = sensor + B
    st.write("센서 데이터와 처리 행렬의 덧셈")

# 신호 보정값
offset = st.slider(
    "신호 보정값 설정",
    min_value=-50,
    max_value=50,
    value=0,
    step=5
)

# 보정 전 결과와 보정 후 결과
corrected = raw_result + offset

# 디지털 밝기 범위 적용
result = np.clip(corrected, 0, 255)

st.divider()

# =====================================
# 6. 처리 결과 비교
# =====================================

st.header("5. 신호 처리 결과 비교")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("센서 입력값")
    st.dataframe(
        np.round(sensor, 1),
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("처리 전 결과")
    st.dataframe(
        np.round(raw_result, 1),
        use_container_width=True,
        hide_index=True
    )

with col3:
    st.subheader("최종 처리 결과")
    st.dataframe(
        np.round(result, 1),
        use_container_width=True,
        hide_index=True
    )

st.success("반도체 신호 처리 시뮬레이션 완료!")

# =====================================
# 7. 계산 과정 설명
# =====================================

st.header("6. 행렬 계산 과정 확인")

if operation == "행렬 곱셈":

    st.write(
        "행렬 곱셈은 앞 행렬의 행과 "
        "뒤 행렬의 열을 곱하고 더하는 방식입니다."
    )

    for i in range(2):
        for j in range(2):

            first = sensor[i][0] * B[0][j]
            second = sensor[i][1] * B[1][j]

            st.write(
                f"({i+1},{j+1}) 위치: "
                f"({sensor[i][0]:.1f} × {B[0][j]:.1f}) + "
                f"({sensor[i][1]:.1f} × {B[1][j]:.1f}) "
                f"= {raw_result[i][j]:.1f}"
            )

else:

    st.write(
        "행렬 덧셈은 같은 위치에 있는 "
        "숫자끼리 더하는 연산입니다."
    )

    for i in range(2):
        for j in range(2):
            st.write(
                f"({i+1},{j+1}) 위치: "
                f"{sensor[i][j]:.1f} + "
                f"{B[i][j]:.1f} "
                f"= {raw_result[i][j]:.1f}"
            )

st.write(f"추가 보정값: {offset}")

st.write(
    "최종 결과는 0~255 범위로 제한됩니다. "
    "이는 디지털 밝기값을 단순화하여 표현한 것입니다."
)

st.divider()

# =====================================
# 8. 반도체와 행렬연산의 관계
# =====================================

st.header("7. 반도체와 행렬연산의 관계")

st.markdown("""
### ① 이미지 센서와 행렬

이미지 센서는 수많은 픽셀로 구성되어 있습니다.
각 픽셀에서 얻은 디지털 데이터는 행렬 형태로 표현할 수 있습니다.

### ② 행렬 곱셈과 신호 처리

행렬 곱셈은 여러 데이터에 일정한 변환 규칙을 적용하는 데
활용할 수 있습니다.

이미지 처리 및 인공지능 연산에서도 중요한 역할을 합니다.

### ③ 신호 보정의 필요성

센서에서 얻은 데이터는 상황에 따라 보정이 필요할 수 있습니다.
밝기나 신호의 특성을 조절하는 과정은 이미지 처리의
기본적인 개념 중 하나입니다.

### ④ 실제 반도체 기술과의 연결

실제 CMOS 이미지 센서에는 포토다이오드와
트랜지스터 등의 반도체 소자가 사용됩니다.

이 소자들이 빛을 전기 신호로 변환하고
읽어내는 과정에 관여합니다.
""")

st.info(
    "탐구 핵심: 반도체 이미지 센서에서 얻은 디지털 데이터를 "
    "행렬로 표현하고, 행렬연산을 통해 신호가 변환되는 과정을 확인했습니다."
)

st.caption("CMOS 반도체 이미지 센서 교육용 시뮬레이터")
