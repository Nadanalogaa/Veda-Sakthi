import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st


def inject_tailwind_theme() -> None:
    """Load Tailwind (CDN) and align Streamlit widgets with a modern surface style."""
    st.markdown(
        """
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
        :root {
            --brand-primary: #4F46E5;
            --brand-accent: #6366F1;
            --brand-surface: #F9FAFB;
            --brand-card: #ffffff;
            --brand-border: #E5E7EB;
            --brand-text: #111827;
            --success-bg: #D1FAE5;
            --success-text: #065F46;
        }
        html, body {
            background: var(--brand-surface);
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        .tw-shell {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 1.5rem 2rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .tw-card {
            background: var(--brand-card);
            border-radius: 0.75rem;
            border: 1px solid var(--brand-border);
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            width: 100%;
        }
        .tw-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.875rem 1.25rem;
            background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent));
            border-radius: 0.75rem;
            color: white;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        }
        .tw-header-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .tw-header-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .tw-header-name {
            font-size: 1.125rem;
            font-weight: 600;
            color: white;
        }
        .tw-header-info {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.4;
        }
        .tw-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(79, 70, 229, 0.1);
            color: var(--brand-primary);
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .tw-section-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.5rem;
        }
        .tw-muted {
            font-size: 0.875rem;
            color: #6B7280;
        }
        .tw-chip {
            border-radius: 0.5rem;
            border: 1px solid var(--brand-border);
            background: #F3F4F6;
            padding: 0.5rem 0.75rem;
            display: inline-flex;
            flex-direction: column;
            justify-content: center;
            min-width: 100px;
        }
        .tw-chip .label {
            display: block;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.625rem;
            font-weight: 600;
            color: #6B7280;
            margin-bottom: 0.25rem;
        }
        .tw-chip .value {
            display: block;
            font-size: 0.9rem;
            font-weight: 600;
            color: #111827;
            line-height: 1.2;
        }
        .tw-field-label {
            font-weight: 600;
            color: #374151;
            margin-bottom: 0.375rem;
            font-size: 0.875rem;
        }
        .tw-toast {
            border-radius: 0.5rem;
            padding: 0.5rem 0.75rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
        }
        .tw-toast.success {
            background: var(--success-bg);
            color: var(--success-text);
            border: 1px solid #6EE7B7;
        }
        .tw-badge {
            border-radius: 0.375rem;
            padding: 0.25rem 0.625rem;
            background: rgba(79, 70, 229, 0.1);
            color: var(--brand-primary);
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: inline-block;
        }
        .tw-upload-section {
            display: flex;
            gap: 1rem;
            align-items: flex-end;
        }
        .tw-upload-group {
            flex: 1;
        }
        .stTextArea textarea {
            border-radius: 0.5rem !important;
            border: 1px solid var(--brand-border) !important;
            background: #F9FAFB !important;
            padding: 0.625rem 0.875rem !important;
            font-size: 0.875rem !important;
            color: var(--brand-text) !important;
            transition: all 0.2s ease !important;
        }
        .stTextArea textarea:focus {
            border-color: var(--brand-primary) !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
            background: #ffffff !important;
        }
        .stTextArea[data-baseweb="textarea"] {
            min-height: auto !important;
        }
        .question-field textarea {
            min-height: 90px !important;
        }
        .option-field textarea {
            min-height: 60px !important;
        }
        .answer-field textarea {
            min-height: 65px !important;
        }
        .explanation-field textarea {
            min-height: 100px !important;
        }
        .glossary-field textarea {
            min-height: 60px !important;
        }
        .stButton>button {
            border-radius: 0.5rem !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent)) !important;
            color: white !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            min-height: 38px !important;
        }
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        }
        .stButton>button:disabled {
            background: #D1D5DB !important;
            color: #6B7280 !important;
            box-shadow: none !important;
            transform: none !important;
        }
        .stDownloadButton>button, button[kind="secondary"] {
            background: white !important;
            color: var(--brand-primary) !important;
            border: 2px solid var(--brand-primary) !important;
        }
        .stDownloadButton>button:hover, button[kind="secondary"]:hover {
            background: var(--brand-surface) !important;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 0.5rem;
            border: 1px solid var(--brand-border);
            overflow: hidden;
        }
        .tw-inline-actions {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
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
    st.title("SME/TA Review Portal")
    st.caption("Please sign in to continue.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    do_login = st.button("Login")
    if do_login:
        user_record = USER_DIRECTORY.get(username)
        if not user_record or password != user_record["password"]:
            st.error("Invalid credentials. Please try again.")
        else:
            store_login_state(username)
            _trigger_rerun()
    return False


def render_top_banner() -> None:
    now = datetime.now()
    user = st.session_state.get("user", {})
    teacher_name = user.get("display_name", "Expert")
    login_at = user.get("login_at", "—")
    role = user.get("role", "")

    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        st.markdown(
            f"""
            <div class="tw-header" style="justify-content: flex-start;">
                <div class="tw-header-name">Hello, {teacher_name}{f' · {role}' if role else ''}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="tw-header" style="justify-content: center;">
                <div class="tw-header-info" style="text-align: center;">
                    <div><strong>Current:</strong> {now.strftime('%d-%m-%Y %H:%M:%S')}</div>
                    <div><strong>Logged in:</strong> {login_at}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        save_logout_cols = st.columns(2)
        with save_logout_cols[0]:
            if st.button("💾 Save", use_container_width=True, key="header_save_btn"):
                persist_state(st.session_state.user["username"])
                st.success("Progress saved!")
        with save_logout_cols[1]:
            if st.button("🚪 Logout", use_container_width=True, key="header_logout_btn"):
                logout_and_rerun("You have been logged out.")


def handle_uploads() -> None:
    st.markdown(
        """
        <div class="tw-card" style="padding: 1rem 1.25rem;">
            <div style="margin-bottom: 1rem;">
                <span class="tw-pill">Content sources</span>
                <h2 class="tw-section-title" style="margin-top: 0.5rem;">Upload workbook links</h2>
                <p class="tw-muted">Pull in the bilingual question bank and glossary supplied by the admin.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    question_col, glossary_col = st.columns(2, gap="medium")

    with question_col:
        st.markdown('<div class="tw-field-label">Bilingual Q&A workbook (.xlsx)</div>', unsafe_allow_html=True)
        upload_row = st.columns([3, 1])
        with upload_row[0]:
            question_file = st.file_uploader("", type=["xlsx"], label_visibility="collapsed", key="questions_upload")
        with upload_row[1]:
            if st.button("Load questions", use_container_width=True, key="load_questions_btn"):
                if question_file is not None:
                    qdf = pd.read_excel(question_file)
                    qdf.columns = [col.strip() for col in qdf.columns]
                    st.session_state.question_df = qdf
                    st.session_state.question_columns = resolve_columns(qdf, QUESTION_COLUMN_CANDIDATES)
                    st.session_state.current_idx = 0
                    st.session_state.row_cache_id = None
                    st.session_state["questions_status"] = "Questions workbook loaded."
                else:
                    st.session_state["questions_status"] = "Attach the workbook before loading."
        status = st.session_state.get("questions_status")
        if status:
            tone = "success" if "loaded" in status.lower() else ""
            st.markdown(
                f'<div class="tw-toast {"success" if tone else ""}" style="margin-top: 0.5rem;">{status}</div>',
                unsafe_allow_html=True,
            )

    with glossary_col:
        st.markdown('<div class="tw-field-label">Glossary workbook (.xlsx)</div>', unsafe_allow_html=True)
        upload_row = st.columns([3, 1])
        with upload_row[0]:
            glossary_file = st.file_uploader("", type=["xlsx"], label_visibility="collapsed", key="glossary_upload")
        with upload_row[1]:
            if st.button("Load glossary", use_container_width=True, key="load_glossary_btn"):
                if glossary_file is not None:
                    gdf = pd.read_excel(glossary_file)
                    gdf.columns = [col.strip() for col in gdf.columns]
                    st.session_state.glossary_df = gdf
                    st.session_state.glossary_columns = resolve_columns(gdf, GLOSSARY_COLUMN_CANDIDATES)
                    st.session_state["glossary_status"] = "Glossary workbook loaded."
                else:
                    st.session_state["glossary_status"] = "Attach the glossary workbook before loading."
        status = st.session_state.get("glossary_status")
        if status:
            tone = "success" if "loaded" in status.lower() else ""
            st.markdown(
                f'<div class="tw-toast {"success" if tone else ""}" style="margin-top: 0.5rem;">{status}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def render_navigation(question_id: Optional[str], total_rows: int) -> None:
    st.markdown('<div class="tw-card" style="padding: 1rem 1.25rem;">', unsafe_allow_html=True)

    controls = st.columns([1, 3, 1])
    with controls[0]:
        if st.button("← Previous", key="nav_prev", use_container_width=True, disabled=st.session_state.current_idx <= 0):
            st.session_state.current_idx = max(0, st.session_state.current_idx - 1)
            st.session_state.row_cache_id = None
            _trigger_rerun()

    with controls[1]:
        st.markdown(
            f"""
            <div class="flex flex-wrap justify-center gap-3">
                <div class="tw-chip">
                    <span class="label">Current row</span>
                    <span class="value">{st.session_state.current_idx + 1}</span>
                </div>
                <div class="tw-chip">
                    <span class="label">Question ID</span>
                    <span class="value">{question_id or "N/A"}</span>
                </div>
                <div class="tw-chip">
                    <span class="label">Total rows</span>
                    <span class="value">{total_rows}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with controls[2]:
        if st.button("Next →", key="nav_next", use_container_width=True, disabled=st.session_state.current_idx >= total_rows - 1):
            st.session_state.current_idx = min(total_rows - 1, st.session_state.current_idx + 1)
            st.session_state.row_cache_id = None
            _trigger_rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_question_editor(row: pd.Series) -> None:
    ensure_row_buffer(row)
    cache = st.session_state.row_cache

    form_card = st.container()
    form_card.markdown('<div class="tw-card" style="padding: 1rem 1.25rem; margin-bottom: 1rem;">', unsafe_allow_html=True)

    with form_card.form("question_editor"):
        st.markdown('<span class="tw-pill">Question editor</span>', unsafe_allow_html=True)
        st.markdown('<h2 class="tw-section-title" style="margin-top: 0.5rem; margin-bottom: 0.75rem;">Review bilingual question content</h2>', unsafe_allow_html=True)

        bilingual_cols = st.columns(2, gap="medium")
        with bilingual_cols[0]:
            st.markdown('<div class="tw-field-label">கேள்வி (Tamil)</div>', unsafe_allow_html=True)
            cache["tamil_question"] = st.text_area(
                "tamil_question_edit",
                value=cache.get("tamil_question", ""),
                label_visibility="collapsed",
                height=90,
                key="tamil_q"
            )
        with bilingual_cols[1]:
            st.markdown('<div class="tw-field-label">Question (English)</div>', unsafe_allow_html=True)
            cache["question_english"] = st.text_area(
                "english_question_edit",
                value=cache.get("question_english", ""),
                label_visibility="collapsed",
                height=90,
                key="eng_q"
            )

        st.markdown('<div class="tw-field-label" style="margin-top: 0.75rem;">Options</div>', unsafe_allow_html=True)
        option_cols = st.columns(4, gap="small")
        option_labels = ["Option A", "Option B", "Option C", "Option D"]
        option_keys = ["optA", "optB", "optC", "optD"]
        for idx, col in enumerate(option_cols):
            with col:
                st.markdown(f'<div class="tw-badge" style="margin-bottom: 0.375rem;">{option_labels[idx]}</div>', unsafe_allow_html=True)
                cache[option_keys[idx]] = st.text_area(
                    f"{option_keys[idx]}_edit",
                    value=cache.get(option_keys[idx], ""),
                    label_visibility="collapsed",
                    height=60,
                    key=f"opt_{option_keys[idx]}"
                )

        answer_cols = st.columns(2, gap="medium")
        with answer_cols[0]:
            st.markdown('<div class="tw-field-label">Tamil answer</div>', unsafe_allow_html=True)
            cache["answer_tamil"] = st.text_area(
                "answer_tamil_edit",
                value=cache.get("answer_tamil", ""),
                label_visibility="collapsed",
                height=65,
                key="tamil_ans"
            )
        with answer_cols[1]:
            st.markdown('<div class="tw-field-label">Answer (English)</div>', unsafe_allow_html=True)
            cache["answer_english"] = st.text_area(
                "answer_english_edit",
                value=cache.get("answer_english", ""),
                label_visibility="collapsed",
                height=65,
                key="eng_ans"
            )

        glossary_cols = st.columns(2, gap="medium")
        with glossary_cols[0]:
            st.markdown('<div class="tw-field-label">Glossary keyword(s)</div>', unsafe_allow_html=True)
            cache["glossary"] = st.text_area(
                "glossary_edit",
                value=cache.get("glossary", ""),
                label_visibility="collapsed",
                height=60,
                key="glossary_key"
            )
        with glossary_cols[1]:
            st.markdown('<div class="tw-field-label">Help</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="tw-muted" style="margin-top: 0.5rem;">Link terms to glossary entries. Use commas for multiples.</div>',
                unsafe_allow_html=True,
            )

        expl_cols = st.columns(2, gap="medium")
        with expl_cols[0]:
            st.markdown('<div class="tw-field-label">விளக்கம் (Tamil)</div>', unsafe_allow_html=True)
            cache["explanation_tamil"] = st.text_area(
                "explanation_tamil_edit",
                value=cache.get("explanation_tamil", ""),
                label_visibility="collapsed",
                height=100,
                key="tamil_expl"
            )
        with expl_cols[1]:
            st.markdown('<div class="tw-field-label">Explanation (English)</div>', unsafe_allow_html=True)
            cache["explanation_english"] = st.text_area(
                "explanation_english_edit",
                value=cache.get("explanation_english", ""),
                label_visibility="collapsed",
                height=100,
                key="eng_expl"
            )

        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        control_cols = st.columns([1, 1, 1], gap="small")
        save_continue = control_cols[0].form_submit_button("Save & Continue", use_container_width=True)
        save_next = control_cols[1].form_submit_button("Save & Next", use_container_width=True)
        save_exit = control_cols[2].form_submit_button("Save & Exit", use_container_width=True)

        if save_continue:
            st.session_state.row_cache = cache
            apply_question_updates("stay")
            st.success("Row saved.")
        if save_next:
            st.session_state.row_cache = cache
            apply_question_updates("next")
        if save_exit:
            st.session_state.row_cache = cache
            apply_question_updates("exit")

    form_card.markdown("</div>", unsafe_allow_html=True)


def render_reference_block(row: pd.Series, question_id: Optional[str]) -> None:
    columns = st.session_state.question_columns
    tamil_question = row.get(columns.get("tamil_question"), "") if columns else ""
    options = row.get(columns.get("options"), "") if columns else ""
    tamil_answer = row.get(columns.get("answer_tamil"), "") if columns else ""
    tamil_exp = row.get(columns.get("explanation_tamil"), "") if columns else ""
    eng_question = row.get(columns.get("question_english"), "") if columns else ""
    eng_answer = row.get(columns.get("answer_english"), "") if columns else ""
    eng_exp = row.get(columns.get("explanation_english"), "") if columns else ""

    st.markdown('<div class="tw-card" style="padding: 1rem 1.25rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="flex flex-col lg:flex-row gap-4">
            <div class="flex-1">
                <div class="tw-pill" style="margin-bottom: 0.5rem;">தமிழ் - Reference</div>
                <div style="color: #374151; font-size: 0.875rem;">
                    <div style="margin-bottom: 0.75rem;"><span class="tw-badge">கேள்வி</span><div style="margin-top: 0.25rem;">{tamil_question or "—"}</div></div>
                    <div style="margin-bottom: 0.75rem;"><span class="tw-badge">விருப்பங்கள்</span><div style="margin-top: 0.25rem;">{options or "—"}</div></div>
                    <div style="margin-bottom: 0.75rem;"><span class="tw-badge">பதில்</span><div style="margin-top: 0.25rem;">{tamil_answer or "—"}</div></div>
                    <div><span class="tw-badge">விளக்கம்</span><div style="margin-top: 0.25rem;">{tamil_exp or "—"}</div></div>
                </div>
            </div>
            <div class="flex-1">
                <div class="tw-pill" style="margin-bottom: 0.5rem;">English - Reference</div>
                <div style="color: #374151; font-size: 0.875rem;">
                    <div style="margin-bottom: 0.75rem;"><span class="tw-badge">Question</span><div style="margin-top: 0.25rem;">{eng_question or "—"}</div></div>
                    <div style="margin-bottom: 0.75rem;"><span class="tw-badge">Answer</span><div style="margin-top: 0.25rem;">{eng_answer or "—"}</div></div>
                    <div style="margin-bottom: 0.75rem;"><span class="tw-badge">Explanation</span><div style="margin-top: 0.25rem;">{eng_exp or "—"}</div></div>
                    <div><span class="tw-badge">Question ID</span><div style="margin-top: 0.25rem;">{question_id or "N/A"}</div></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_glossary_editor(question_id: Optional[str]) -> None:
    glossary_df: Optional[pd.DataFrame] = st.session_state.get("glossary_df")
    mapping = st.session_state.get("glossary_columns", {})

    card = st.container()
    with card:
        st.markdown('<div class="tw-card" style="padding: 1rem 1.25rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="margin-bottom: 1rem;">
                <span class="tw-pill">Glossary</span>
                <h2 class="tw-section-title" style="margin-top: 0.5rem;">Curate supporting terminology</h2>
                <p class="tw-muted">Add, edit, or remove glossary entries associated with this question ID.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if glossary_df is None or mapping.get("question_id") is None:
            st.markdown(
                '<div class="tw-toast">Upload a glossary workbook to enable editing.</div>',
                unsafe_allow_html=True,
            )
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

    action_cols = st.columns([1, 3])
    with action_cols[0]:
        if st.button("Save glossary changes", key=f"save_glossary_{question_id or 'new'}", use_container_width=True):
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
            st.success("Glossary updated.")

    st.markdown("</div>", unsafe_allow_html=True)


# --- Main application flow -----------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="SME Review Tool", layout="wide")
    inject_tailwind_theme()
    st.markdown('<div class="tw-shell">', unsafe_allow_html=True)

    try:
        if st.session_state.get("flash_message"):
            st.success(st.session_state.pop("flash_message"))

        user = st.session_state.get("user")
        if not user:
            render_login()
            return

        bootstrap_state_from_disk(user["username"])
        render_top_banner()
        handle_uploads()

        question_df: Optional[pd.DataFrame] = st.session_state.get("question_df")

        if question_df is None or question_df.empty:
            st.info("Upload the bilingual questions workbook to begin reviewing.")
            return

        if st.session_state.get("question_columns") is None:
            st.session_state.question_columns = resolve_columns(question_df, QUESTION_COLUMN_CANDIDATES)

        row, question_id = current_row_and_id()
        if row is None:
            st.warning("No rows found in the uploaded workbook.")
            return

        render_navigation(question_id, len(question_df))
        render_question_editor(row)
        render_reference_block(row, question_id)
        render_glossary_editor(question_id)
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
