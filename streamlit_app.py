import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st

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
    st.session_state.user = {
        "username": username,
        "display_name": USER_DIRECTORY[username]["display_name"],
        "role": USER_DIRECTORY[username]["role"],
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
        st.experimental_rerun()
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
    banner = st.container()
    with banner:
        cols = st.columns([1, 2, 1])
        cols[0].markdown(f"**Date:** {now.strftime('%d-%m-%Y')}")
        user = st.session_state.get("user", {})
        cols[1].markdown(f"**Subject Matter Expert (SME) Panel for:** {user.get('display_name', 'Unknown')}")
        cols[2].markdown(f"**Time:** {now.strftime('%H:%M:%S')}")


def handle_uploads() -> None:
    st.subheader("Upload workbook links")
    prompt_cols = st.columns([2, 0.8, 2, 0.8])

    with prompt_cols[0]:
        question_file = st.file_uploader("Bilingual Q&A workbook (.xlsx)", type=["xlsx"], key="questions_upload")
    with prompt_cols[1]:
        if st.button("Load", key="load_questions") and question_file:
            qdf = pd.read_excel(question_file)
            qdf.columns = [col.strip() for col in qdf.columns]
            st.session_state.question_df = qdf
            st.session_state.question_columns = resolve_columns(qdf, QUESTION_COLUMN_CANDIDATES)
            st.session_state.current_idx = 0
            st.session_state.row_cache_id = None
            st.success("Questions workbook loaded.")

    with prompt_cols[2]:
        glossary_file = st.file_uploader("Glossary workbook (.xlsx)", type=["xlsx"], key="glossary_upload")
    with prompt_cols[3]:
        if st.button("Load", key="load_glossary") and glossary_file:
            gdf = pd.read_excel(glossary_file)
            gdf.columns = [col.strip() for col in gdf.columns]
            st.session_state.glossary_df = gdf
            st.session_state.glossary_columns = resolve_columns(gdf, GLOSSARY_COLUMN_CANDIDATES)
            st.success("Glossary workbook loaded.")


def render_navigation(question_id: Optional[str], total_rows: int) -> None:
    nav_cols = st.columns([1, 1, 1, 1, 1, 1, 1])

    with nav_cols[0]:
        if st.button("Previous", disabled=st.session_state.current_idx <= 0):
            st.session_state.current_idx = max(0, st.session_state.current_idx - 1)
            st.session_state.row_cache_id = None
            st.experimental_rerun()

    with nav_cols[1]:
        st.markdown(f"**Row # A**<br>{st.session_state.current_idx + 1}", unsafe_allow_html=True)

    with nav_cols[2]:
        st.markdown(f"**_id Number**<br>{question_id or 'N/A'}", unsafe_allow_html=True)

    with nav_cols[3]:
        st.markdown(f"**Row # z**<br>{total_rows}", unsafe_allow_html=True)

    with nav_cols[4]:
        if st.button("Next", disabled=st.session_state.current_idx >= total_rows - 1):
            st.session_state.current_idx = min(total_rows - 1, st.session_state.current_idx + 1)
            st.session_state.row_cache_id = None
            st.experimental_rerun()

    with nav_cols[5]:
        if st.button("Save File"):
            persist_state(st.session_state.user["username"])
            st.success("Current workbook snapshot saved.")

    with nav_cols[6]:
        if st.button("Logout"):
            logout_and_rerun("You have been logged out.")


def render_question_editor(row: pd.Series) -> None:
    ensure_row_buffer(row)
    cache = st.session_state.row_cache

    with st.form("question_editor"):
        st.markdown('<div class="tight-label">கேள்வி</div>', unsafe_allow_html=True)
        cache["tamil_question"] = st.text_area(
            "கேள்வி", value=cache.get("tamil_question", ""), height=64, label_visibility="collapsed"
        )

        st.markdown('<div class="tight-label">Question (English)</div>', unsafe_allow_html=True)
        cache["question_english"] = st.text_area(
            "Question (English)", value=cache.get("question_english", ""), height=64, label_visibility="collapsed"
        )

        st.markdown('<div class="tight-label">விருப்பங்கள்</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="small")
        cache["optA"] = col1.text_area(
            "Option A", value=cache.get("optA", ""), height=44, label_visibility="collapsed"
        )
        cache["optB"] = col2.text_area(
            "Option B", value=cache.get("optB", ""), height=44, label_visibility="collapsed"
        )

        col3, col4 = st.columns(2, gap="small")
        cache["optC"] = col3.text_area(
            "Option C", value=cache.get("optC", ""), height=44, label_visibility="collapsed"
        )
        cache["optD"] = col4.text_area(
            "Option D", value=cache.get("optD", ""), height=44, label_visibility="collapsed"
        )

        extra_cols = st.columns(2, gap="small")
        cache["glossary"] = extra_cols[0].text_area(
            "Glossary", value=cache.get("glossary", ""), height=44, label_visibility="collapsed"
        )
        cache["answer_tamil"] = extra_cols[1].text_area(
            "Answer", value=cache.get("answer_tamil", ""), height=44, label_visibility="collapsed"
        )

        cache["answer_english"] = st.text_area(
            "Answer (English)", value=cache.get("answer_english", ""), height=44, label_visibility="visible"
        )

        st.markdown('<div class="tight-label">விளக்கம்</div>', unsafe_allow_html=True)
        cache["explanation_tamil"] = st.text_area(
            "விளக்கம்", value=cache.get("explanation_tamil", ""), height=180, label_visibility="collapsed"
        )

        cache["explanation_english"] = st.text_area(
            "Explanation (English)", value=cache.get("explanation_english", ""), height=180, label_visibility="visible"
        )

        control_cols = st.columns(3)
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


def render_reference_block(row: pd.Series, question_id: Optional[str]) -> None:
    columns = st.session_state.question_columns
    tamil_question = row.get(columns.get("tamil_question"), "") if columns else ""
    options = row.get(columns.get("options"), "") if columns else ""
    tamil_answer = row.get(columns.get("answer_tamil"), "") if columns else ""
    tamil_exp = row.get(columns.get("explanation_tamil"), "") if columns else ""
    eng_question = row.get(columns.get("question_english"), "") if columns else ""
    eng_answer = row.get(columns.get("answer_english"), "") if columns else ""
    eng_exp = row.get(columns.get("explanation_english"), "") if columns else ""

    st.markdown(
        f"""
        <div class="cw-min">
          <b>தமிழ்</b><br>
          <strong>கேள்வி:</strong> {tamil_question}<br>
          <strong>விருப்பங்கள்:</strong> {options}<br>
          <strong>பதில்:</strong> {tamil_answer}<br>
          <strong>விளக்கம்:</strong> {tamil_exp}
        </div>
        <div style="height: 0.3em;"></div>
        <div class="cw-min">
          <b>English</b><br>
          <strong>Question:</strong> {eng_question}<br>
          <strong>Answer:</strong> {eng_answer}<br>
          <strong>Explanation:</strong> {eng_exp}<br>
          <strong>Question ID:</strong> {question_id or 'N/A'}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_glossary_editor(question_id: Optional[str]) -> None:
    st.subheader("Glossary entries linked to this question")
    glossary_df: Optional[pd.DataFrame] = st.session_state.get("glossary_df")
    mapping = st.session_state.get("glossary_columns", {})

    if glossary_df is None or mapping.get("question_id") is None:
        st.info("Upload a glossary workbook to edit glossary terms.")
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

    if st.button("Save Glossary Changes", key=f"save_glossary_{question_id or 'new'}"):
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


# --- Main application flow -----------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="SME Review Tool", layout="wide")
    st.markdown(
        """
        <style>
        .block-container { padding-bottom: 0 !important; padding-top: 0.2rem !important; }
        .main { padding-bottom: 0 !important; margin-bottom: 0 !important; }
        .tight-label {
            font-size: 0.85em !important;
            font-weight: 500 !important;
            line-height: 1.08;
            margin-bottom: -0.34em !important;
            margin-top: -0.51em !important;
            padding-bottom:0 !important;
            padding-top:0 !important;
        }
        .stTextArea { margin-top: -0.44em !important; margin-bottom: -0.55em !important; }
        textarea[data-baseweb="textarea"] { min-height: 44px !important; font-size: 0.98em !important; }
        .stTextArea label { display:none !important; }
        body, html { margin-bottom: 0 !important; padding-bottom: 0 !important;}
        footer {visibility: hidden;}
        .cw-min {
            line-height: 1.06 !important;
            margin: 0 !important;
            padding: 0 !important;
            font-size: 1.01em !important;
        }
        .cw-min strong { font-weight: 600 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

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
