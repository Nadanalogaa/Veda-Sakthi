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
            --brand-primary: #1c64f2;
            --brand-accent: #2563eb;
            --brand-surface: #f8fafc;
            --brand-card: #ffffff;
            --brand-border: #e2e8f0;
            --brand-text: #0f172a;
        }
        body, .block-container {
            background: var(--brand-surface);
        }
        .tw-card {
            background: var(--brand-card);
            border-radius: 1rem;
            border: 1px solid var(--brand-border);
            box-shadow: 0 24px 48px -32px rgba(15, 23, 42, 0.35);
        }
        .tw-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(28, 100, 242, 0.12);
            color: var(--brand-primary);
            padding: 0.3rem 0.9rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .tw-section-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #0f172a;
        }
        .tw-muted {
            font-size: 0.95rem;
            color: #64748b;
        }
        .tw-chip {
            border-radius: 0.95rem;
            border: 1px solid var(--brand-border);
            background: #f1f5f9;
            padding: 0.7rem 1rem;
            box-shadow: 0 18px 32px -28px rgba(15, 23, 42, 0.35);
        }
        .tw-chip .label {
            display: block;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.65rem;
            font-weight: 600;
            color: #475569;
            margin-bottom: 0.35rem;
        }
        .tw-chip .value {
            display: block;
            font-size: 1rem;
            font-weight: 600;
            color: #0f172a;
        }
        .tw-field-label {
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0.45rem;
            font-size: 0.95rem;
        }
        .tw-toast {
            border-radius: 0.9rem;
            padding: 0.6rem 0.95rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
        }
        .tw-toast.success {
            background: rgba(34, 197, 94, 0.12);
            color: #15803d;
            border: 1px solid rgba(34, 197, 94, 0.35);
        }
        .tw-badge {
            border-radius: 0.75rem;
            padding: 0.3rem 0.8rem;
            background: rgba(37, 99, 235, 0.12);
            color: #1d4ed8;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .stTextArea textarea, .stTextInput input, .stNumberInput input {
            border-radius: 0.85rem !important;
            border: 1px solid var(--brand-border) !important;
            background: #f1f5f9 !important;
            padding: 0.9rem 1.1rem !important;
            font-size: 1rem !important;
            color: var(--brand-text);
            height: auto !important;
            min-height: 120px !important;
        }
        .stTextArea textarea:focus, .stTextInput input:focus, .stNumberInput input:focus {
            border-color: rgba(28, 100, 242, 0.7) !important;
            box-shadow: 0 0 0 4px rgba(28, 100, 242, 0.15) !important;
            background: #ffffff !important;
        }
        .stButton>button {
            border-radius: 0.9rem;
            padding: 0.65rem 1.4rem;
            border: none;
            font-weight: 600;
            font-size: 0.95rem;
            background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent));
            color: white;
            transition: transform 0.12s ease, box-shadow 0.2s ease;
            width: 100%;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 32px -18px rgba(37, 99, 235, 0.55);
        }
        .stButton>button:disabled {
            background: #cbd5f5;
            color: #475569;
            box-shadow: none;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 1rem;
            border: 1px solid var(--brand-border);
            overflow: hidden;
            box-shadow: 0 18px 28px -25px rgba(15, 23, 42, 0.18);
        }
        header, footer {visibility: hidden;}
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

    st.markdown(
        f"""
        <div class="tw-card p-6 mb-6">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
                <div>
                    <div class="tw-pill mb-3">SME Workspace</div>
                    <h1 class="text-2xl md:text-3xl font-semibold text-slate-900 mb-2">
                        Hello, {teacher_name}{f' · {role}' if role else ''}
                    </h1>
                    <p class="tw-muted">
                        Continue refining questions, answers, and glossary entries for your bilingual content set.
                    </p>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 w-full md:w-auto">
                    <div class="tw-chip">
                        <span class="label">Current time</span>
                        <span class="value">{now.strftime('%d %b %Y • %H:%M:%S')}</span>
                    </div>
                    <div class="tw-chip">
                        <span class="label">Logged in at</span>
                        <span class="value">{login_at}</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def handle_uploads() -> None:
    upload_card = st.container()
    upload_card.markdown(
        """
        <div class="tw-card p-6 mb-6">
            <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4 mb-6">
                <div>
                    <div class="tw-pill mb-3">Content sources</div>
                    <h2 class="tw-section-title mb-2">Upload workbook links</h2>
                    <p class="tw-muted">Bring in the latest bilingual question bank and glossary provided by the admin.</p>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    question_col, glossary_col = upload_card.columns(2, gap="large")

    with question_col:
        upload_card.markdown('<div class="tw-field-label">Bilingual Q&A workbook (.xlsx)</div>', unsafe_allow_html=True)
        question_file = st.file_uploader("Bilingual workbook", type=["xlsx"], key="questions_upload")
        q_controls = st.columns([1, 1])
        with q_controls[0]:
            if st.button("Load questions", key="load_questions"):
                if question_file:
                    qdf = pd.read_excel(question_file)
                    qdf.columns = [col.strip() for col in qdf.columns]
                    st.session_state.question_df = qdf
                    st.session_state.question_columns = resolve_columns(qdf, QUESTION_COLUMN_CANDIDATES)
                    st.session_state.current_idx = 0
                    st.session_state.row_cache_id = None
                    st.session_state["questions_status"] = "Questions workbook loaded."
                else:
                    st.session_state["questions_status"] = "Please attach the workbook before loading."
        with q_controls[1]:
            status = st.session_state.get("questions_status")
            if status:
                tone = "success" if "loaded" in status.lower() else ""
                st.markdown(
                    f'<div class="tw-toast {"success" if tone else ""}">{status}</div>',
                    unsafe_allow_html=True,
                )

    with glossary_col:
        upload_card.markdown('<div class="tw-field-label">Glossary workbook (.xlsx)</div>', unsafe_allow_html=True)
        glossary_file = st.file_uploader("Glossary workbook", type=["xlsx"], key="glossary_upload")
        g_controls = st.columns([1, 1])
        with g_controls[0]:
            if st.button("Load glossary", key="load_glossary"):
                if glossary_file:
                    gdf = pd.read_excel(glossary_file)
                    gdf.columns = [col.strip() for col in gdf.columns]
                    st.session_state.glossary_df = gdf
                    st.session_state.glossary_columns = resolve_columns(gdf, GLOSSARY_COLUMN_CANDIDATES)
                    st.session_state["glossary_status"] = "Glossary workbook loaded."
                else:
                    st.session_state["glossary_status"] = "Please attach the glossary workbook before loading."
        with g_controls[1]:
            status = st.session_state.get("glossary_status")
            if status:
                tone = "success" if "loaded" in status.lower() else ""
                st.markdown(
                    f'<div class="tw-toast {"success" if tone else ""}">{status}</div>',
                    unsafe_allow_html=True,
                )

    upload_card.markdown("</div>", unsafe_allow_html=True)


def render_navigation(question_id: Optional[str], total_rows: int) -> None:
    nav_card = st.container()
    nav_card.markdown('<div class="tw-card p-4 mb-6">', unsafe_allow_html=True)

    controls = nav_card.columns([1, 3, 1])
    with controls[0]:
        if st.button("Previous", key="nav_prev", disabled=st.session_state.current_idx <= 0):
            st.session_state.current_idx = max(0, st.session_state.current_idx - 1)
            st.session_state.row_cache_id = None
            _trigger_rerun()

    with controls[1]:
        chips_html = f"""
        <div class="flex flex-wrap items-center justify-center gap-3">
            <div class="tw-chip">
                <span class="label">Current Row</span>
                <span class="value">{st.session_state.current_idx + 1}</span>
            </div>
            <div class="tw-chip">
                <span class="label">Question ID</span>
                <span class="value">{question_id or "N/A"}</span>
            </div>
            <div class="tw-chip">
                <span class="label">Total Rows</span>
                <span class="value">{total_rows}</span>
            </div>
        </div>
        """
        nav_card.markdown(chips_html, unsafe_allow_html=True)

    with controls[2]:
        if st.button("Next", key="nav_next", disabled=st.session_state.current_idx >= total_rows - 1):
            st.session_state.current_idx = min(total_rows - 1, st.session_state.current_idx + 1)
            st.session_state.row_cache_id = None
            _trigger_rerun()

    actions = nav_card.columns([2, 1, 1])
    with actions[1]:
        if st.button("Save Progress", key="save_file_btn"):
            persist_state(st.session_state.user["username"])
            st.success("Progress saved to session storage.")
    with actions[2]:
        if st.button("Logout", key="logout_nav_btn"):
            logout_and_rerun("You have been logged out.")

    nav_card.markdown("</div>", unsafe_allow_html=True)


def render_question_editor(row: pd.Series) -> None:
    ensure_row_buffer(row)
    cache = st.session_state.row_cache

    form_card = st.container()
    form_card.markdown('<div class="tw-card p-6 mb-6">', unsafe_allow_html=True)

    with form_card.form("question_editor"):
        st.markdown('<div class="tw-pill mb-3">Question editor</div>', unsafe_allow_html=True)
        st.markdown('<h2 class="tw-section-title mb-4">Review bilingual question content</h2>', unsafe_allow_html=True)

        bilingual_cols = st.columns(2, gap="large")
        with bilingual_cols[0]:
            st.markdown('<div class="tw-field-label">கேள்வி (Tamil)</div>', unsafe_allow_html=True)
            cache["tamil_question"] = st.text_area(
                "tamil_question_edit",
                value=cache.get("tamil_question", ""),
                label_visibility="collapsed",
            )
        with bilingual_cols[1]:
            st.markdown('<div class="tw-field-label">Question (English)</div>', unsafe_allow_html=True)
            cache["question_english"] = st.text_area(
                "english_question_edit",
                value=cache.get("question_english", ""),
                label_visibility="collapsed",
            )

        st.markdown('<div class="tw-field-label mt-4">Options</div>', unsafe_allow_html=True)
        option_cols = st.columns(4, gap="small")
        option_labels = ["Option A", "Option B", "Option C", "Option D"]
        option_keys = ["optA", "optB", "optC", "optD"]
        for idx, col in enumerate(option_cols):
            with col:
                st.markdown(f'<div class="tw-badge mb-2">{option_labels[idx]}</div>', unsafe_allow_html=True)
                cache[option_keys[idx]] = st.text_area(
                    f"{option_keys[idx]}_edit",
                    value=cache.get(option_keys[idx], ""),
                    label_visibility="collapsed",
                )

        answer_cols = st.columns(2, gap="large")
        with answer_cols[0]:
            st.markdown('<div class="tw-field-label">Tamil answer</div>', unsafe_allow_html=True)
            cache["answer_tamil"] = st.text_area(
                "answer_tamil_edit",
                value=cache.get("answer_tamil", ""),
                label_visibility="collapsed",
            )
        with answer_cols[1]:
            st.markdown('<div class="tw-field-label">Answer (English)</div>', unsafe_allow_html=True)
            cache["answer_english"] = st.text_area(
                "answer_english_edit",
                value=cache.get("answer_english", ""),
                label_visibility="collapsed",
            )

        glossary_cols = st.columns([1, 1], gap="large")
        with glossary_cols[0]:
            st.markdown('<div class="tw-field-label">Glossary keyword(s)</div>', unsafe_allow_html=True)
            cache["glossary"] = st.text_area(
                "glossary_edit",
                value=cache.get("glossary", ""),
                label_visibility="collapsed",
            )
        with glossary_cols[1]:
            st.markdown(
                '<div class="tw-muted text-sm">Link terms to glossary entries. Use commas for multiples.</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="tw-field-label mt-4">விளக்கம் (Tamil)</div>', unsafe_allow_html=True)
        cache["explanation_tamil"] = st.text_area(
            "explanation_tamil_edit",
            value=cache.get("explanation_tamil", ""),
            label_visibility="collapsed",
        )

        st.markdown('<div class="tw-field-label">Explanation (English)</div>', unsafe_allow_html=True)
        cache["explanation_english"] = st.text_area(
            "explanation_english_edit",
            value=cache.get("explanation_english", ""),
            label_visibility="collapsed",
        )

        control_cols = st.columns([1, 1, 1], gap="medium")
        save_continue = control_cols[0].form_submit_button("Save & Continue")
        save_next = control_cols[1].form_submit_button("Save & Next")
        save_exit = control_cols[2].form_submit_button("Save & Exit")

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

    st.markdown('<div class="tw-card p-6 mb-6">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="flex flex-col lg:flex-row gap-6">
            <div class="flex-1">
                <div class="tw-pill mb-2">தமிழ் - Reference</div>
                <div class="space-y-2 text-slate-700">
                    <div><span class="tw-badge">கேள்வி</span><div class="mt-1">{tamil_question or "—"}</div></div>
                    <div><span class="tw-badge">விருப்பங்கள்</span><div class="mt-1">{options or "—"}</div></div>
                    <div><span class="tw-badge">பதில்</span><div class="mt-1">{tamil_answer or "—"}</div></div>
                    <div><span class="tw-badge">விளக்கம்</span><div class="mt-1">{tamil_exp or "—"}</div></div>
                </div>
            </div>
            <div class="flex-1">
                <div class="tw-pill mb-2">English - Reference</div>
                <div class="space-y-2 text-slate-700">
                    <div><span class="tw-badge">Question</span><div class="mt-1">{eng_question or "—"}</div></div>
                    <div><span class="tw-badge">Answer</span><div class="mt-1">{eng_answer or "—"}</div></div>
                    <div><span class="tw-badge">Explanation</span><div class="mt-1">{eng_exp or "—"}</div></div>
                    <div><span class="tw-badge">Question ID</span><div class="mt-1">{question_id or "N/A"}</div></div>
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
        st.markdown('<div class="tw-card p-6 mb-10">', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-5">
                <div>
                    <div class="tw-pill mb-3">Glossary</div>
                    <h2 class="tw-section-title mb-2">Curate supporting terminology</h2>
                    <p class="tw-muted">Add, edit, or remove glossary entries associated with this question ID.</p>
                </div>
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
            if st.button("Save glossary changes", key=f"save_glossary_{question_id or 'new'}"):
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


if __name__ == "__main__":
    main()
