import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st


def inject_tailwind_theme() -> None:
    """Clean, professional website design."""
    st.markdown(
        """
        <style>
        :root {
            --primary: #4F46E5;
            --primary-dark: #4338CA;
            --bg: #F9FAFB;
            --text: #111827;
            --text-light: #6B7280;
            --border: #E5E7EB;
            --success: #10B981;
        }

        html, body {
            background: var(--bg);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        /* Main Header - Single Bar */
        .app-header {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            padding: 1rem 2rem;
            display: grid;
            grid-template-columns: 2fr 3fr 2fr;
            align-items: center;
            gap: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .header-left { font-size: 1.125rem; font-weight: 600; }
        .header-center {
            font-size: 0.875rem;
            text-align: center;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        .header-right {
            display: flex;
            gap: 0.5rem;
            justify-content: flex-end;
        }
        .header-btn {
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.1);
            color: white;
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .header-btn:hover {
            background: rgba(255,255,255,0.2);
        }

        /* Content Area */
        .content-wrapper {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Upload Section - Clean */
        .upload-area {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        .upload-label {
            font-weight: 600;
            color: var(--text);
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }

        /* Navigation - Clean Bar */
        .nav-bar {
            background: white;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid var(--border);
        }

        .nav-info {
            display: flex;
            gap: 2rem;
            align-items: center;
            font-size: 0.875rem;
            color: var(--text);
        }

        .nav-info-text {
            font-weight: 500;
        }

        .nav-info-text strong {
            color: var(--text-light);
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
        }

        /* Editor Section - Clean Panel */
        .editor-panel {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
        }

        .panel-header {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--primary);
        }

        .field-label {
            font-weight: 600;
            color: var(--text);
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
        }

        .field-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .field-row-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        /* Reference Section */
        .reference-panel {
            background: #FAFBFC;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
        }

        .reference-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        .reference-col h4 {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 1rem;
            text-transform: uppercase;
        }

        .ref-item {
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .ref-item:last-child {
            border-bottom: none;
        }

        .ref-label {
            font-size: 0.75rem;
            color: var(--text-light);
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .ref-value {
            color: var(--text);
            font-size: 0.875rem;
        }

        /* Form Fields */
        .stTextArea textarea, .stTextInput input {
            border-radius: 6px !important;
            border: 1px solid var(--border) !important;
            background: white !important;
            padding: 0.625rem !important;
            font-size: 0.875rem !important;
            color: var(--text) !important;
        }

        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 6px !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
            color: white !important;
            transition: all 0.2s !important;
            min-height: 38px !important;
        }

        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        }

        .stButton>button:disabled {
            background: #D1D5DB !important;
            color: #6B7280 !important;
        }

        /* Login Page */
        body[data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
        }

        .login-box {
            background: white;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            margin: 10vh auto;
        }

        .login-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.5rem;
            text-align: center;
        }

        .login-subtitle {
            color: var(--text-light);
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Success Toast */
        .success-toast {
            background: #D1FAE5;
            color: #065F46;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-size: 0.875rem;
            margin-top: 0.5rem;
            border: 1px solid #6EE7B7;
        }

        /* Data Editor */
        div[data-testid="stDataFrame"] {
            border-radius: 6px;
            border: 1px solid var(--border);
            overflow: hidden;
        }

        header, footer {visibility: hidden;}
        #MainMenu {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )


# --- Configuration -----------------------------------------------------------------

SESSION_ROOT = Path("session_store")
SESSION_ROOT.mkdir(parents=True, exist_ok=True)

# Placeholder user store; replace with your real authentication source.
USER_DIRECTORY: Dict[str, Dict[str, str]] = {
    "teacher": {"password": "teach@123", "display_name": "Teacher One", "role": "SME"},
    "assistant": {"password": "assist@123", "display_name": "Teaching Assistant", "role": "TA"},
}

QUESTION_COLUMN_CANDIDATES: Dict[str, List[str]] = {
    "tamil_question": ["கேள்வி", "கேள்வி ", "tamil_question"],
    "options": ["விருப்பங்கள்", "விருப்பங்கள் ", "questionOptions"],
    "options_english": ["questionOptions", "Options", "Options (English)", "options_english"],
    "answer_tamil": ["பதில்", "பதில் ", "answers ", "answer_tamil"],
    "explanation_tamil": ["விளக்கம்", "விளக்கம் ", "tam_explanation"],
    "glossary": ["Glossary", "glossary"],
    "question_english": ["question", "question ", "Question"],
    "answer_english": ["answer", "answers", "answers ", "Answer"],
    "explanation_english": ["explanation", "Explanation"],
    "question_id": ["_id", "id", "Id", "question_id", "QuestionID", "questionId", "_id Number"],
}

GLOSSARY_COLUMN_CANDIDATES: Dict[str, List[str]] = {
    "question_id": ["question_id", "QuestionID", "_id", "id", "questionId"],
    "term": ["term", "Term", "GlossaryTerm"],
    "definition": ["definition", "Definition", "GlossaryDefinition", "meaning"],
}


# --- Utility helpers ----------------------------------------------------------------

def resolve_columns(df: pd.DataFrame, candidates: Dict[str, List[str]]) -> Dict[str, Optional[str]]:
    """Map semantic keys to actual columns by scanning candidate names."""
    mapping: Dict[str, Optional[str]] = {}
    columns = {col.strip(): col for col in df.columns}
    df.rename(columns=columns, inplace=True)

    for key, options in candidates.items():
        mapping[key] = next((opt for opt in options if opt in df.columns), None)
    return mapping


def load_persisted_state(username: str) -> Optional[Dict]:
    payload_path = SESSION_ROOT / f"{username}_state.json"
    if not payload_path.exists():
        return None

    with payload_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def persist_state(username: str) -> None:
    payload_path = SESSION_ROOT / f"{username}_state.json"
    questions = st.session_state.get("question_df")
    glossary = st.session_state.get("glossary_df")

    payload = {
        "current_idx": st.session_state.get("current_idx", 0),
        "question_df": {
            "columns": list(questions.columns) if isinstance(questions, pd.DataFrame) else [],
            "records": questions.to_dict(orient="records") if isinstance(questions, pd.DataFrame) else [],
        },
        "glossary_df": {
            "columns": list(glossary.columns) if isinstance(glossary, pd.DataFrame) else [],
            "records": glossary.to_dict(orient="records") if isinstance(glossary, pd.DataFrame) else [],
        },
    }

    with payload_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def bootstrap_state_from_disk(username: str) -> None:
    if st.session_state.get("state_loaded"):
        return

    persisted = load_persisted_state(username)
    if not persisted:
        return

    st.session_state.current_idx = persisted.get("current_idx", 0)

    question_data = persisted.get("question_df", {})
    if question_data.get("records"):
        qdf = pd.DataFrame(question_data["records"])
        if question_data.get("columns"):
            qdf = qdf.reindex(columns=question_data["columns"])
        st.session_state.question_df = qdf
        st.session_state.question_columns = resolve_columns(qdf, QUESTION_COLUMN_CANDIDATES)

    glossary_data = persisted.get("glossary_df", {})
    if glossary_data.get("records"):
        gdf = pd.DataFrame(glossary_data["records"])
        if glossary_data.get("columns"):
            gdf = gdf.reindex(columns=glossary_data["columns"])
        st.session_state.glossary_df = gdf
        st.session_state.glossary_columns = resolve_columns(gdf, GLOSSARY_COLUMN_CANDIDATES)

    st.session_state.state_loaded = True


def store_login_state(username: str) -> None:
    login_timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    st.session_state.user = {
        "username": username,
        "display_name": USER_DIRECTORY[username]["display_name"],
        "role": USER_DIRECTORY[username]["role"],
        "login_at": login_timestamp,
    }
    st.session_state.current_idx = 0
    st.session_state.question_df = None
    st.session_state.glossary_df = None
    st.session_state.state_loaded = False


def _trigger_rerun() -> None:
    """Compatibility helper for rerunning the Streamlit script."""
    rerun_fn = getattr(st, "rerun", None)
    if rerun_fn is None:
        rerun_fn = getattr(st, "experimental_rerun")
    rerun_fn()


def logout_and_rerun(message: str) -> None:
    username = st.session_state.user["username"]
    persist_state(username)
    st.session_state.clear()
    st.session_state["flash_message"] = message
    _trigger_rerun()


def normalize_options_from_row(raw_options: str) -> Dict[str, str]:
    if not raw_options or not isinstance(raw_options, str):
        return {"optA": "", "optB": "", "optC": "", "optD": ""}

    parts = [segment.strip() for segment in raw_options.split("|")]
    while len(parts) < 4:
        parts.append("")

    return {
        "optA": parts[0],
        "optB": parts[1],
        "optC": parts[2],
        "optD": parts[3],
    }


def compose_options_string(options: Dict[str, str]) -> str:
    return " | ".join(options.get(key, "").strip() for key in ["optA", "optB", "optC", "optD"] if options.get(key))


def current_row_and_id() -> Tuple[Optional[pd.Series], Optional[str]]:
    qdf: Optional[pd.DataFrame] = st.session_state.get("question_df")
    if qdf is None or qdf.empty:
        return None, None

    idx = st.session_state.get("current_idx", 0)
    idx = max(0, min(idx, len(qdf) - 1))
    st.session_state.current_idx = idx
    row = qdf.iloc[idx]

    id_column = st.session_state.question_columns.get("question_id") if st.session_state.get("question_columns") else None
    question_id = str(row[id_column]).strip() if id_column and pd.notna(row.get(id_column)) else None
    return row, question_id


def ensure_row_buffer(row: pd.Series) -> None:
    if not st.session_state.get("row_cache") or st.session_state.get("row_cache_id") != st.session_state.current_idx:
        columns = st.session_state.question_columns
        raw_options = row.get(columns.get("options")) if columns and columns.get("options") else ""
        options = normalize_options_from_row(raw_options)

        st.session_state.row_cache = {
            "tamil_question": row.get(columns.get("tamil_question"), "") if columns else "",
            "question_english": row.get(columns.get("question_english"), "") if columns else "",
            "optA": options["optA"],
            "optB": options["optB"],
            "optC": options["optC"],
            "optD": options["optD"],
            "glossary": row.get(columns.get("glossary"), "") if columns else "",
            "answer_tamil": row.get(columns.get("answer_tamil"), "") if columns else "",
            "answer_english": row.get(columns.get("answer_english"), "") if columns else "",
            "explanation_tamil": row.get(columns.get("explanation_tamil"), "") if columns else "",
            "explanation_english": row.get(columns.get("explanation_english"), "") if columns else "",
        }
        st.session_state.row_cache_id = st.session_state.current_idx

        widget_defaults = {
            "tamil_q": st.session_state.row_cache["tamil_question"],
            "eng_q": st.session_state.row_cache["question_english"],
            "opt_optA": st.session_state.row_cache["optA"],
            "opt_optB": st.session_state.row_cache["optB"],
            "opt_optC": st.session_state.row_cache["optC"],
            "opt_optD": st.session_state.row_cache["optD"],
            "glossary_key": st.session_state.row_cache["glossary"],
            "tamil_ans": st.session_state.row_cache["answer_tamil"],
            "eng_ans": st.session_state.row_cache["answer_english"],
            "tamil_expl": st.session_state.row_cache["explanation_tamil"],
            "eng_expl": st.session_state.row_cache["explanation_english"],
        }
        for key, value in widget_defaults.items():
            st.session_state[key] = value


def apply_question_updates(action: str) -> None:
    row_cache = st.session_state.get("row_cache", {})
    qdf: pd.DataFrame = st.session_state.question_df
    columns = st.session_state.question_columns
    idx = st.session_state.current_idx

    if columns.get("tamil_question"):
        qdf.at[idx, columns["tamil_question"]] = row_cache.get("tamil_question", "")
    if columns.get("question_english"):
        qdf.at[idx, columns["question_english"]] = row_cache.get("question_english", "")
    if columns.get("answer_tamil"):
        qdf.at[idx, columns["answer_tamil"]] = row_cache.get("answer_tamil", "")
    if columns.get("answer_english"):
        qdf.at[idx, columns["answer_english"]] = row_cache.get("answer_english", "")
    if columns.get("explanation_tamil"):
        qdf.at[idx, columns["explanation_tamil"]] = row_cache.get("explanation_tamil", "")
    if columns.get("explanation_english"):
        qdf.at[idx, columns["explanation_english"]] = row_cache.get("explanation_english", "")
    if columns.get("glossary"):
        qdf.at[idx, columns["glossary"]] = row_cache.get("glossary", "")

    # Options handling (split into four editable inputs).
    merged_options = compose_options_string(row_cache)
    if columns.get("options"):
        qdf.at[idx, columns["options"]] = merged_options
    else:
        qdf.at[idx, "questionOptions"] = merged_options

    st.session_state.question_df = qdf
    persist_state(st.session_state.user["username"])

    if action == "next":
        st.session_state.current_idx = min(idx + 1, len(qdf) - 1)
        st.session_state.row_cache_id = None
        _trigger_rerun()
    if action == "exit":
        logout_and_rerun("Progress saved. Please log in again to continue.")


def render_login() -> bool:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">SME Review Portal</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Please sign in to continue</p>', unsafe_allow_html=True)

        username = st.text_input("Username", label_visibility="visible")
        password = st.text_input("Password", type="password", label_visibility="visible")

        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        do_login = st.button("Login", use_container_width=True)

        if do_login:
            user_record = USER_DIRECTORY.get(username)
            if not user_record or password != user_record["password"]:
                st.error("Invalid credentials. Please try again.")
            else:
                store_login_state(username)
                _trigger_rerun()

        st.markdown('</div>', unsafe_allow_html=True)
    return False


def render_top_banner() -> None:
    now = datetime.now()
    user = st.session_state.get("user", {})
    teacher_name = user.get("display_name", "Expert")
    login_at = user.get("login_at", "—")
    role = user.get("role", "")

    # Create columns for header layout
    col_left, col_center, col_right = st.columns([2, 3, 2])

    with col_left:
        st.markdown(
            f'<div class="header-left">Hello, {teacher_name} · {role}</div>',
            unsafe_allow_html=True
        )

    with col_center:
        st.markdown(
            f'''<div class="header-center">
                <div><strong>Current:</strong> {now.strftime('%d-%m-%Y %H:%M:%S')}</div>
                <div><strong>Logged in:</strong> {login_at}</div>
            </div>''',
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown('<div class="header-right">', unsafe_allow_html=True)
        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("💾 Save", key="save_btn", use_container_width=True):
                persist_state(user["username"])
                st.success("Progress saved!")
        with btn_cols[1]:
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                logout_and_rerun("You have been logged out.")
        st.markdown('</div>', unsafe_allow_html=True)


def handle_uploads() -> None:
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="upload-label">Bilingual Q&A workbook (.xlsx)</div>', unsafe_allow_html=True)
        upload_cols = st.columns([3, 1])
        with upload_cols[0]:
            question_file = st.file_uploader("", type=["xlsx"], label_visibility="collapsed", key="questions_upload")
        with upload_cols[1]:
            if st.button("Load", use_container_width=True, key="load_q_btn"):
                if question_file:
                    qdf = pd.read_excel(question_file)
                    qdf.columns = [col.strip() for col in qdf.columns]
                    st.session_state.question_df = qdf
                    st.session_state.question_columns = resolve_columns(qdf, QUESTION_COLUMN_CANDIDATES)
                    st.session_state.current_idx = 0
                    st.session_state.row_cache_id = None
                    st.session_state["questions_status"] = "✓ Questions workbook loaded"
                else:
                    st.session_state["questions_status"] = "⚠ Please select a file"

        if st.session_state.get("questions_status"):
            st.markdown(
                f'<div class="success-toast">{st.session_state["questions_status"]}</div>',
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown('<div class="upload-label">Glossary workbook (.xlsx)</div>', unsafe_allow_html=True)
        upload_cols = st.columns([3, 1])
        with upload_cols[0]:
            glossary_file = st.file_uploader("", type=["xlsx"], label_visibility="collapsed", key="glossary_upload")
        with upload_cols[1]:
            if st.button("Load", use_container_width=True, key="load_g_btn"):
                if glossary_file:
                    gdf = pd.read_excel(glossary_file)
                    gdf.columns = [col.strip() for col in gdf.columns]
                    st.session_state.glossary_df = gdf
                    st.session_state.glossary_columns = resolve_columns(gdf, GLOSSARY_COLUMN_CANDIDATES)
                    st.session_state["glossary_status"] = "✓ Glossary workbook loaded"
                else:
                    st.session_state["glossary_status"] = "⚠ Please select a file"

        if st.session_state.get("glossary_status"):
            st.markdown(
                f'<div class="success-toast">{st.session_state["glossary_status"]}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def render_navigation(question_id: Optional[str], total_rows: int) -> None:
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)

    btn_prev, info_section, btn_next = st.columns([1, 4, 1])

    with btn_prev:
        if st.button("← Previous", key="nav_prev", use_container_width=True, disabled=st.session_state.current_idx <= 0):
            st.session_state.current_idx = max(0, st.session_state.current_idx - 1)
            st.session_state.row_cache_id = None
            _trigger_rerun()

    with info_section:
        st.markdown(
            f'''<div class="nav-info">
                <span class="nav-info-text"><strong>Current Row:</strong> {st.session_state.current_idx + 1}</span>
                <span class="nav-info-text"><strong>Question ID:</strong> {question_id or "N/A"}</span>
                <span class="nav-info-text"><strong>Total Rows:</strong> {total_rows}</span>
            </div>''',
            unsafe_allow_html=True,
        )

    with btn_next:
        if st.button("Next →", key="nav_next", use_container_width=True, disabled=st.session_state.current_idx >= total_rows - 1):
            st.session_state.current_idx = min(total_rows - 1, st.session_state.current_idx + 1)
            st.session_state.row_cache_id = None
            _trigger_rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_question_editor(row: pd.Series) -> None:
    ensure_row_buffer(row)
    cache = st.session_state.row_cache

    st.markdown('<div class="editor-panel">', unsafe_allow_html=True)

    with st.form("question_editor"):
        st.markdown('<div class="panel-header">Question Editor</div>', unsafe_allow_html=True)

        # Questions
        st.markdown('<div class="field-row">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="field-label">கேள்வி (Tamil)</div>', unsafe_allow_html=True)
            cache["tamil_question"] = st.text_area("", value=cache.get("tamil_question", ""), height=90, key="tamil_q", label_visibility="collapsed")
        with col2:
            st.markdown('<div class="field-label">Question (English)</div>', unsafe_allow_html=True)
            cache["question_english"] = st.text_area("", value=cache.get("question_english", ""), height=90, key="eng_q", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Options
        st.markdown('<div class="field-label">Options</div>', unsafe_allow_html=True)
        st.markdown('<div class="field-row-4">', unsafe_allow_html=True)
        option_labels = ["A", "B", "C", "D"]
        option_keys = ["optA", "optB", "optC", "optD"]
        opt_cols = st.columns(4)
        for idx, col in enumerate(opt_cols):
            with col:
                cache[option_keys[idx]] = st.text_area(f"Option {option_labels[idx]}", value=cache.get(option_keys[idx], ""), height=60, key=f"opt_{option_keys[idx]}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Answers
        st.markdown('<div class="field-row">', unsafe_allow_html=True)
        ans1, ans2 = st.columns(2)
        with ans1:
            st.markdown('<div class="field-label">Tamil Answer</div>', unsafe_allow_html=True)
            cache["answer_tamil"] = st.text_area("", value=cache.get("answer_tamil", ""), height=65, key="tamil_ans", label_visibility="collapsed")
        with ans2:
            st.markdown('<div class="field-label">Answer (English)</div>', unsafe_allow_html=True)
            cache["answer_english"] = st.text_area("", value=cache.get("answer_english", ""), height=65, key="eng_ans", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Glossary
        st.markdown('<div class="field-label">Glossary Keywords <span style="color: #6B7280; font-weight: normal; font-size: 0.75rem;">(comma-separated)</span></div>', unsafe_allow_html=True)
        cache["glossary"] = st.text_area("", value=cache.get("glossary", ""), height=60, key="glossary_key", label_visibility="collapsed")

        # Explanations
        st.markdown('<div class="field-row">', unsafe_allow_html=True)
        exp1, exp2 = st.columns(2)
        with exp1:
            st.markdown('<div class="field-label">விளக்கம் (Tamil)</div>', unsafe_allow_html=True)
            cache["explanation_tamil"] = st.text_area("", value=cache.get("explanation_tamil", ""), height=100, key="tamil_expl", label_visibility="collapsed")
        with exp2:
            st.markdown('<div class="field-label">Explanation (English)</div>', unsafe_allow_html=True)
            cache["explanation_english"] = st.text_area("", value=cache.get("explanation_english", ""), height=100, key="eng_expl", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Action buttons
        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        btn1, btn2, btn3 = st.columns(3)
        save_continue = btn1.form_submit_button("Save & Continue", use_container_width=True)
        save_next = btn2.form_submit_button("Save & Next", use_container_width=True)
        save_exit = btn3.form_submit_button("Save & Exit", use_container_width=True)

        if save_continue:
            st.session_state.row_cache = cache
            apply_question_updates("stay")
            st.success("✓ Saved successfully")
        if save_next:
            st.session_state.row_cache = cache
            apply_question_updates("next")
        if save_exit:
            st.session_state.row_cache = cache
            apply_question_updates("exit")

    st.markdown("</div>", unsafe_allow_html=True)


def render_reference_block(row: pd.Series, question_id: Optional[str]) -> None:
    columns = st.session_state.question_columns
    tamil_question = row.get(columns.get("tamil_question"), "") if columns else ""
    options = row.get(columns.get("options"), "") if columns else ""
    if pd.isna(options):
        options = ""
    tamil_answer = row.get(columns.get("answer_tamil"), "") if columns else ""
    tamil_exp = row.get(columns.get("explanation_tamil"), "") if columns else ""
    eng_question = row.get(columns.get("question_english"), "") if columns else ""
    eng_answer = row.get(columns.get("answer_english"), "") if columns else ""
    eng_exp = row.get(columns.get("explanation_english"), "") if columns else ""
    english_options_col = columns.get("options_english") if columns else None
    english_options = row.get(english_options_col, "") if english_options_col else ""
    if pd.isna(english_options):
        english_options = ""

    st.markdown(
        f'''<div class="reference-panel">
            <div class="reference-grid">
                <div class="reference-col">
                    <h4>தமிழ் Reference</h4>
                    <div class="ref-item">
                        <div class="ref-label">கேள்வி</div>
                        <div class="ref-value">{tamil_question or "—"}</div>
                    </div>
                    <div class="ref-item">
                        <div class="ref-label">விருப்பங்கள்</div>
                        <div class="ref-value">{options or "—"}</div>
                    </div>
                    <div class="ref-item">
                        <div class="ref-label">பதில்</div>
                        <div class="ref-value">{tamil_answer or "—"}</div>
                    </div>
                    <div class="ref-item">
                        <div class="ref-label">விளக்கம்</div>
                        <div class="ref-value">{tamil_exp or "—"}</div>
                    </div>
                </div>
                <div class="reference-col">
                    <h4>English Reference</h4>
                    <div class="ref-item">
                        <div class="ref-label">Question</div>
                        <div class="ref-value">{eng_question or "—"}</div>
                    </div>
                    <div class="ref-item">
                        <div class="ref-label">Options</div>
                        <div class="ref-value">{english_options or "—"}</div>
                    </div>
                    <div class="ref-item">
                        <div class="ref-label">Answer</div>
                        <div class="ref-value">{eng_answer or "—"}</div>
                    </div>
                    <div class="ref-item">
                        <div class="ref-label">Explanation</div>
                        <div class="ref-value">{eng_exp or "—"}</div>
                    </div>
                    <div class="ref-item">
                        <div class="ref-label">Question ID</div>
                        <div class="ref-value">{question_id or "N/A"}</div>
                    </div>
                </div>
            </div>
        </div>''',
        unsafe_allow_html=True,
    )


def render_glossary_editor(question_id: Optional[str]) -> None:
    glossary_df: Optional[pd.DataFrame] = st.session_state.get("glossary_df")
    mapping = st.session_state.get("glossary_columns", {})

    st.markdown('<div class="editor-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">Glossary Editor</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6B7280; font-size: 0.875rem; margin-bottom: 1.5rem;">Add, edit, or remove glossary entries associated with this question.</p>', unsafe_allow_html=True)

    if glossary_df is None or mapping.get("question_id") is None:
        st.info("Upload a glossary workbook to enable editing.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    id_col = mapping["question_id"]
    term_col = mapping.get("term") or "term"
    definition_col = mapping.get("definition") or "definition"

    if term_col not in glossary_df.columns:
        glossary_df[term_col] = ""
    if definition_col not in glossary_df.columns:
        glossary_df[definition_col] = ""

    if question_id:
        matching_rows = glossary_df[glossary_df[id_col].astype(str) == question_id].copy()
    else:
        matching_rows = glossary_df.head(0).copy()

    if matching_rows.empty:
        matching_rows = pd.DataFrame([{id_col: question_id or "", term_col: "", definition_col: ""}])

    edited = st.data_editor(
        matching_rows.reset_index(drop=True),
        num_rows="dynamic",
        use_container_width=True,
        key=f"glossary_editor_{question_id or 'new'}",
    )

    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 3])
    with btn_col1:
        if st.button("Save Glossary", key=f"save_glossary_{question_id or 'new'}", use_container_width=True):
            edited[id_col] = edited[id_col].fillna(question_id or "")
            edited[term_col] = edited[term_col].fillna("")
            edited[definition_col] = edited[definition_col].fillna("")

            if question_id:
                glossary_df = glossary_df[glossary_df[id_col].astype(str) != question_id]
                glossary_df = pd.concat([glossary_df, edited], ignore_index=True)
            else:
                glossary_df = pd.concat([glossary_df, edited], ignore_index=True)

            st.session_state.glossary_df = glossary_df
            persist_state(st.session_state.user["username"])
            st.success("✓ Glossary updated")

    st.markdown("</div>", unsafe_allow_html=True)


# --- Main application flow -----------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="SME Review Tool", layout="wide")
    inject_tailwind_theme()

    if st.session_state.get("flash_message"):
        st.success(st.session_state.pop("flash_message"))

    user = st.session_state.get("user")
    if not user:
        render_login()
        return

    bootstrap_state_from_disk(user["username"])
    render_top_banner()

    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

    handle_uploads()

    question_df: Optional[pd.DataFrame] = st.session_state.get("question_df")

    if question_df is None or question_df.empty:
        st.info("📁 Upload the bilingual questions workbook to begin reviewing.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.session_state.get("question_columns") is None:
        st.session_state.question_columns = resolve_columns(question_df, QUESTION_COLUMN_CANDIDATES)

    row, question_id = current_row_and_id()
    if row is None:
        st.warning("⚠️ No rows found in the uploaded workbook.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    render_navigation(question_id, len(question_df))
    render_question_editor(row)
    render_reference_block(row, question_id)
    render_glossary_editor(question_id)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
