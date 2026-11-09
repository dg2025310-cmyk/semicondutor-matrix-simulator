
import streamlit as st
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="반도체 행렬연산 시뮬레이터",
    page_icon="💻",
    layout="wide"
)

st.title("💻 반도체 신호 처리 시뮬레이터")
st.write("행렬연산을 이용해 반도체 센서의 신호 처리 과정을 알아봅시다.")

st.info(
    "이 프로그램은 반도체 센서의 신호 측정과 "
    "행렬연산을 단순화하여 표현한 교육용 시뮬레이션입니다."
)

st.subheader("1. 센서 측정값 입력")

st.write(
    "행렬 A는 센서에서 측정한 신호값을 나타냅니다."
)

st.write(
    "행렬 B는 신호를 변환하는 처리 계수를 나타냅니다."
)

def make_matrix(title, prefix, defaults):
    st.markdown(f"### {title}")

    matrix = []

    for i in range(2):
        cols = st.columns(2)
        row = []

        for j in range(2):
            value = cols[j].number_input(
                f"{prefix} ({i+1},{j+1})",
                min_value=-10,
                max_value=10,
                value=defaults[i][j],
                step=1,
                key=f"{prefix}_{i}_{j}"
            )
            row.append(value)

        matrix.append(row)

    return np.array(matrix)

col1, col2 = st.columns(2)

with col1:
    A = make_matrix(
        "센서 측정 행렬 A",
        "A",
        [[2, 4], [3, 5]]
    )

with col2:
    B = make_matrix(
        "신호 처리 행렬 B",
        "B",
        [[1, 2], [2, 1]]
    )

st.divider()

st.subheader("2. 행렬연산 선택")

operation = st.radio(
    "실행할 연산을 선택하세요.",
    ["행렬 곱셈", "행렬 덧셈"],
    horizontal=True
)

if operation == "행렬 곱셈":
    result = A @ B
else:
    result = A + B

st.divider()

st.subheader("3. 시뮬레이션 결과")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("입력 행렬 A")
    st.dataframe(A, hide_index=True)

with col2:
    st.write("처리 행렬 B")
    st.dataframe(B, hide_index=True)

with col3:
    st.write("연산 결과")
    st.dataframe(result, hide_index=True)

st.success("행렬연산이 완료되었습니다!")

st.divider()

st.subheader("4. 계산 과정 알아보기")

if operation == "행렬 곱셈":

    st.write("행렬 곱셈은 행과 열의 원소를 곱한 뒤 더하는 방식입니다.")

    for i in range(2):
        for j in range(2):
            x = A[i][0] * B[0][j]
            y = A[i][1] * B[1][j]

            st.write(
                f"결과 행렬의 ({i+1},{j+1}) 위치: "
                f"({A[i][0]} × {B[0][j]}) + "
                f"({A[i][1]} × {B[1][j]}) = {result[i][j]}"
            )

    st.info(
        "이처럼 행렬 곱셈을 이용하면 여러 센서의 신호값을 "
        "한 번에 변환하고 계산할 수 있습니다."
    )

else:

    st.write("행렬 덧셈은 같은 위치에 있는 원소끼리 더합니다.")

    for i in range(2):
        for j in range(2):
            st.write(
                f"({i+1},{j+1}) 위치: "
                f"{A[i][j]} + {B[i][j]} = {result[i][j]}"
            )

    st.info(
        "행렬 덧셈을 이용하면 같은 크기의 신호 행렬을 "
        "원소별로 결합할 수 있습니다."
    )

st.divider()

st.subheader("5. 핵심 개념 정리")

st.markdown("""
- **행렬 A:** 센서가 측정한 신호값
- **행렬 B:** 신호를 변환하는 처리 계수
- **행렬 곱셈:** 여러 신호값을 일정한 규칙에 따라 변환하는 연산
- **행렬 덧셈:** 같은 위치의 신호값을 더하는 연산

실제 반도체 시스템에서는 다양한 행렬연산이
신호 처리와 데이터 계산에 활용됩니다.
""")

st.caption("반도체 행렬연산 교육용 시뮬레이터")
