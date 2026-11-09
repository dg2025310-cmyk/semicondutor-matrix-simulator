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
