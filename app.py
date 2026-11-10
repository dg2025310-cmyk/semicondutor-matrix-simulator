
import streamlit as st
import numpy as np
import pandas as pd

# -------------------------
# 기본 설정
# -------------------------
st.set_page_config(
    page_title="반도체 행렬 연산 시뮬레이터",
    page_icon="🔬",
    layout="wide"
)

# -------------------------
# 디자인
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

[data-testid="stAppViewContainer"] {
    background-color: #081426;
}

h1, h2, h3, h4 {
    color: #8FC8FF !important;
}

p, label, span {
    color: #EAF2FF;
}

div[data-testid="stMetric"] {
    background-color: #142944;
    border: 1px solid #294766;
    padding: 15px;
    border-radius: 12px;
}

.stButton > button {
    background-color: #1769AA;
    color: white;
    border: none;
    border-radius: 8px;
    height: 45px;
}

.stButton > button:hover {
    background-color: #278BD8;
    color: white;
}

div[data-testid="stDataFrame"] {
    background-color: #142944;
    border-radius: 10px;
}

div[data-testid="stNumberInput"] input {
    background-color: #142944;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# 제목
# -------------------------
st.title("🔬 반도체 행렬 연산 시뮬레이터")

st.markdown("""
인공지능 반도체 NPU 내부에서 데이터가 입력되고,
행렬로 변환되어 연산 결과가 만들어지는 과정을 알아보자.
""")

st.divider()


# -------------------------
# 4단계 구성
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "01 데이터 입력",
    "02 행렬 변환",
    "03 행렬 연산",
    "04 결과 전달"
])


# -------------------------
# 01 데이터 입력
# -------------------------
with tab1:

    st.header("01. 데이터 입력")

    st.write("""
    인공지능 반도체는 이미지, 음성 등의 데이터를
    숫자 형태로 입력받아 처리할 수 있다.

    아래는 이해를 돕기 위한 예시 숫자 데이터다.
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
                key=f"input_{i}"
            )
            input_values.append(value)

    st.session_state["input_values"] = input_values

    st.info("""
    입력 데이터는 이후 행렬 형태로 정리된다.
    실제 인공지능 시스템에서는 이미지 픽셀값이나
    신경망의 중간 계산 결과 등이 입력될 수 있다.
    """)


# -------------------------
# 02 행렬 변환
# -------------------------
with tab2:

    st.header("02. 행렬 변환")

    st.write("""
    입력받은 숫자 데이터를 행렬 형태로 배열한다.
    행렬 연산을 위해 가중치 행렬도 함께 준비한다.
    """)

    values = st.session_state.get(
        "input_values", [1, 2, 3, 4]
    )

    A = np.array(values).reshape(2, 2)

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

    st.success("숫자 데이터가 2×2 행렬로 구성되었다.")

    st.caption(
        "가중치 행렬은 설명을 위한 예시값이며, "
        "실제 AI에서는 학습된 가중치가 사용된다."
    )


# -------------------------
# 03 행렬 연산
# -------------------------
with tab3:

    st.header("03. 행렬 연산")

    st.write("""
    두 행렬을 곱하면 행과 열의 대응하는 숫자들을
    곱하고 그 결과를 더하는 과정이 반복된다.
    이때 활용되는 대표적인 연산 구조가 MAC이다.
    """)

    A = st.session_state.get(
        "A", np.array([[1, 2], [3, 4]])
    )

    B = st.session_state.get(
        "B", np.array([[5, 6], [7, 8]])
    )

    C = A @ B

    st.subheader("MAC 연산 과정")

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

        st.markdown(f"#### 연산 {k+1}")

        st.latex(
            f"{A[selected_row,k]:g}"
            r"\\times"
            f"{B[k,selected_col]:g}"
            f"={multiply:g}"
        )

        st.write(
            f"이전 누적값 {before:g} + "
            f"현재 곱셈 결과 {multiply:g} "
            f"= {total:g}"
        )

    st.divider()

    st.subheader("전체 행렬 곱셈 결과")

    st.latex(r"C=A\\times B")

    st.dataframe(
        pd.DataFrame(C),
        use_container_width=True
    )

    st.session_state["result"] = C

    st.info("""
    MAC은 Multiply-Accumulate의 약자다.
    두 값을 곱하고 그 결과를 누적해서 더하는 연산으로,
    행렬 곱셈의 각 결과값을 계산할 때 활용된다.
    """)


# -------------------------
# 04 결과 전달
# -------------------------
with tab4:

    st.header("04. 결과 전달")

    st.write("""
    모든 행렬 연산이 완료되면 최종 결과 행렬이 생성된다.
    이 결과는 다음 신경망 연산 단계 등으로 전달되어
    인공지능 정보 처리에 활용될 수 있다.
    """)

    A = st.session_state.get(
        "A", np.array([[1, 2], [3, 4]])
    )

    B = st.session_state.get(
        "B", np.array([[5, 6], [7, 8]])
    )

    C = A @ B

    st.subheader("최종 결과 행렬")

    st.dataframe(
        pd.DataFrame(C),
        use_container_width=True
    )

    st.success("행렬 연산 결과가 생성되었다.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("입력 데이터 수", "4개")

    with col2:
        st.metric("행렬 크기", "2 × 2")

    with col3:
        st.metric("MAC 연산 횟수", "8회")

    st.divider()

    st.subheader("전체 처리 과정 정리")

    st.markdown("""
    **① 데이터 입력**

    숫자 형태의 데이터를 입력한다.

    **② 행렬 변환**

    입력 데이터를 행렬로 배열하고 가중치 행렬을 준비한다.

    **③ 행렬 연산**

    MAC 연산을 통해 곱셈과 누적 덧셈을 수행한다.

    **④ 결과 전달**

    최종 행렬을 생성하고 다음 연산 단계로 전달한다.
    """)

    st.caption(
        "교육용 NPU 행렬 연산 시뮬레이터"
    )
