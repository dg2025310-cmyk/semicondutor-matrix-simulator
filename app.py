
import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# 1. 기본 설정
# -----------------------------
st.set_page_config(
    page_title="반도체 행렬 연산 시뮬레이터",
    page_icon="🔬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #081426;
    color: #EAF2FF;
}
h1, h2, h3 {
    color: #8FC8FF !important;
}
p, label, span {
    color: #EAF2FF;
}
div[data-testid="stMetric"] {
    background: #142944;
    padding: 15px;
    border-radius: 12px;
}
div[data-testid="stDataFrame"] {
    background: #142944;
    border-radius: 10px;
}
.stButton button {
    background-color: #1769AA;
    color: white;
    border-radius: 8px;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 2. 제목
# -----------------------------
st.title("🔬 반도체 행렬 연산 시뮬레이터")

st.markdown("""
### NPU 내부에서 행렬은 어떻게 계산될까?

인공지능 반도체인 NPU가 입력 데이터와 가중치 행렬을
이용하여 연산하는 과정을 살펴보자.
""")

st.divider()


# -----------------------------
# 3. 반도체 연산 원리
# -----------------------------
st.subheader("01. 반도체 내부의 연산 구조")

st.markdown("""
NPU는 행렬 연산을 빠르게 처리하기 위해
여러 연산 장치(Processing Element)를 활용할 수 있다.

각 연산 장치는 곱셈과 누적 덧셈을 반복하는
MAC 연산을 수행한다.
""")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("① 데이터 입력")
    st.write("입력 행렬 A와 가중치 행렬 B가 연산 장치에 전달된다.")

with c2:
    st.info("② MAC 연산")
    st.write("대응하는 원소를 곱하고 그 결과를 누적해서 더한다.")

with c3:
    st.info("③ 결과 출력")
    st.write("누적 연산이 끝나면 결과 행렬 C가 만들어진다.")

st.divider()


# -----------------------------
# 4. 행렬 입력
# -----------------------------
st.subheader("02. 연산에 사용할 행렬")

st.write("""
아래 두 행렬은 이해를 돕기 위한 예시 데이터다.
숫자를 직접 바꾸면 연산 결과도 자동으로 바뀐다.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 입력 행렬 A")
    df_a = st.data_editor(
        pd.DataFrame(
            [[1, 2], [3, 4]],
            columns=["열 1", "열 2"],
            index=["행 1", "행 2"]
        ),
        key="matrix_a",
        use_container_width=True,
        num_rows="fixed"
    )

with col2:
    st.markdown("### 가중치 행렬 B")
    df_b = st.data_editor(
        pd.DataFrame(
            [[5, 6], [7, 8]],
            columns=["열 1", "열 2"],
            index=["행 1", "행 2"]
        ),
        key="matrix_b",
        use_container_width=True,
        num_rows="fixed"
    )

A = df_a.to_numpy(dtype=float)
B = df_b.to_numpy(dtype=float)

st.caption(
    "※ 현재 예시는 2×2 행렬을 사용한다. "
    "실제 NPU는 더 큰 행렬과 다양한 데이터 형식을 처리한다."
)

st.divider()


# -----------------------------
# 5. 행렬 연산
# -----------------------------
st.subheader("03. 행렬 곱셈 시작")

if st.button("행렬 연산 실행", use_container_width=True):

    C = A @ B

    st.session_state["result"] = C
    st.session_state["A"] = A
    st.session_state["B"] = B

    st.success("행렬 곱셈이 완료되었다!")


# -----------------------------
# 6. 계산 결과
# -----------------------------
if "result" in st.session_state:

    A = st.session_state["A"]
    B = st.session_state["B"]
    C = st.session_state["result"]

    st.markdown("### 최종 연산 결과")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.markdown("**입력 행렬 A**")
        st.dataframe(
            pd.DataFrame(A),
            use_container_width=True
        )

    with r2:
        st.markdown("**가중치 행렬 B**")
        st.dataframe(
            pd.DataFrame(B),
            use_container_width=True
        )

    with r3:
        st.markdown("**결과 행렬 C**")
        st.dataframe(
            pd.DataFrame(C),
            use_container_width=True
        )

    st.latex(r"C=A\times B")

    st.divider()

    # -------------------------
    # 7. MAC 연산 과정
    # -------------------------
    st.subheader("04. MAC 연산 과정 자세히 보기")

    row = st.selectbox(
        "확인할 결과 행 선택",
        [0, 1],
        format_func=lambda x: f"{x+1}번째 행"
    )

    col = st.selectbox(
        "확인할 결과 열 선택",
        [0, 1],
        format_func=lambda x: f"{x+1}번째 열"
    )

    st.markdown("### 선택한 결과값이 만들어지는 과정")

    st.write(
        f"결과 행렬의 {row+1}행 {col+1}열을 계산한다."
    )

    total = 0

    for k in range(A.shape[1]):

        multiplication = A[row, k] * B[k, col]
        before = total
        total += multiplication

        st.markdown(f"#### STEP {k+1}")

        st.code(
            f"{A[row, k]:g} × {B[k, col]:g} "
            f"= {multiplication:g}"
        )

        st.write(
            f"이전 누적값: {before:g}"
        )

        st.write(
            f"현재 누적값: {before:g} + "
            f"{multiplication:g} = {total:g}"
        )

        st.progress(
            (k + 1) / A.shape[1]
        )

    st.success(
        f"최종 결과: C[{row+1}, {col+1}] = {total:g}"
    )

    st.divider()

    # -------------------------
    # 8. 연산 원리 설명
    # -------------------------
    st.subheader("05. 반도체 내부에서는 무슨 일이 일어날까?")

    st.markdown("""
    **① 입력 데이터 전달**

    행렬 A의 행 데이터와 행렬 B의 열 데이터가
    연산 장치에 전달된다.

    **② 곱셈 수행**

    연산 장치 내부의 곱셈 회로가 두 값을 곱한다.

    **③ 누적 덧셈 수행**

    곱셈 결과를 누적 덧셈 회로에 전달하여
    이전 계산 결과에 더한다.

    **④ 결과 저장**

    모든 곱셈과 누적 덧셈이 끝나면
    해당 위치의 최종 결과를 저장한다.

    이러한 과정이 반복되어 전체 결과 행렬이 만들어진다.
    """)

    st.info("""
    실제 NPU에서는 여러 MAC 연산 장치가 병렬로 작동할 수 있다.
    따라서 위 시뮬레이터의 순차적인 설명은 원리를 이해하기 위한
    교육용 표현이며, 모든 NPU의 실제 동작 순서와 동일한 것은 아니다.
    """)

else:

    st.info(
        "먼저 행렬을 입력한 뒤 '행렬 연산 실행' 버튼을 눌러보자."
    )


# -----------------------------
# 9. 학습 정리
# -----------------------------
st.divider()

st.subheader("06. 핵심 개념 정리")

with st.expander("행렬 곱셈이란?"):
    st.write("""
    한 행렬의 행과 다른 행렬의 열에 있는 원소를
    각각 곱한 뒤 모두 더하는 연산이다.
    """)

with st.expander("MAC 연산이란?"):
    st.write("""
    MAC은 Multiply-Accumulate의 약자다.
    두 수를 곱한 뒤 기존 누적값에 더하는 연산이다.
    인공지능 반도체의 행렬 연산에 널리 활용된다.
    """)

with st.expander("NPU란?"):
    st.write("""
    NPU는 Neural Processing Unit의 약자다.
    인공지능에 필요한 신경망 연산을 효율적으로 처리하도록
    설계된 반도체 연산 장치다.
    """)

st.caption(
    "교육용 시뮬레이터 | NPU 행렬 연산의 기본 원리 학습"
)
