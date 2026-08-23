"""
Downloads mratanusarkar/Indian-Laws from Hugging Face, cleans formatting,
extracts section titles, tags with multi-label doc_types and saves to a clean CSV.

Usage:
    .\venv\Scripts\python.exe .\scripts\extract_legal_data.py
"""

import re
from pathlib import Path
from datasets import load_dataset
import pandas as pd

EXPECTED_COLUMNS = {"act_title", "section", "law"}

ACT_FILTERS = {
    # Core (general contract fundamentals)
    "indian contract act": ["rent_agreement", "offer_letter", "terms_conditions", "general"],

    # Rent & Tenancy Law
    "transfer of property act": ["rent_agreement", "general"],
    "model tenancy": ["rent_agreement"],
    "specific relief act": ["rent_agreement", "general"],
    "rent control": ["rent_agreement"],
    "delhi rent": ["rent_agreement"],
    "rent restriction": ["rent_agreement"],

    # Employment & Labour Law
    "industrial disputes act": ["offer_letter"],
    "payment of gratuity act": ["offer_letter"],
    "payment of wages act": ["offer_letter"],
    "code on wages": ["offer_letter"],
    "maternity benefit act": ["offer_letter"],
    "employees provident funds": ["offer_letter"],

    # Consumer & Digital Privacy
    "consumer protection act": ["terms_conditions", "general"],
    "information technology act": ["terms_conditions", "general"],
    "digital personal data protection": ["terms_conditions", "general"],
}


def matches_any_filter(act_title: str) -> list[str] | None:
    """Returns doc_types if act_title matches a target act, else None."""
    title_lower = act_title.lower()
    if "institutes of information technology" in title_lower:
        return None

    # Collect all matching doc_types
    matched_types = set()
    for keyword, doc_types in ACT_FILTERS.items():
        if keyword in title_lower:
            matched_types.update(doc_types)

    return sorted(matched_types) if matched_types else None


def clean_section_data(act_name: str, raw_section: str, raw_law: str) -> tuple[str, str, str]:
    """
    Cleans raw legal text:
    - Extracts section title from the top lines if available
    - Normalizes OCR / PDF line breaks and whitespace
    - Removes redundant headers from content
    """
    if not isinstance(raw_law, str) or not raw_law.strip():
        return (str(raw_section).strip(), "", "")

    lines = [l.strip() for l in raw_law.splitlines() if l.strip()]
    if not lines:
        return (str(raw_section).strip(), "", "")

    section_title = ""
    start_idx = 0

    # 1. Skip repeated Act Title in the first line
    if len(lines) > 0 and (act_name.lower() in lines[0].lower() or lines[0].lower() in act_name.lower()):
        start_idx += 1

    # 2. Extract Section Title if present in the next line (e.g., "27. Agreement in restraint of trade void")
    if start_idx < len(lines):
        candidate = lines[start_idx]
        match = re.match(
            r"^(?:Section\s+)?(?:\d+[A-Za-z]*|[IVXLCDM]+)\s*[\.\:\-\–\—]\s*(.+)$",
            candidate,
            re.IGNORECASE,
        )
        if match:
            section_title = match.group(1).strip()
            start_idx += 1
        elif len(candidate) < 90 and not candidate.startswith("(") and not candidate.endswith("."):
            section_title = candidate.strip()
            start_idx += 1

    # 3. Clean up the remaining content body
    body_lines = lines[start_idx:] if start_idx < len(lines) else lines
    content = " ".join(body_lines)

    # Fix broken hyphenated line breaks (e.g. "agree- ment" -> "agreement")
    content = re.sub(r"(\w+)-\s+(\w+)", r"\1\2", content)
    # Collapse multiple whitespaces into a single space
    content = re.sub(r"\s+", " ", content).strip()

    # Clean section number
    sec_num = str(raw_section).strip()
    sec_num_match = re.search(r"(\d+[A-Za-z]*)", sec_num)
    if sec_num_match:
        sec_num = sec_num_match.group(1)

    return (sec_num, section_title, content)


def main():
    print("Downloading mratanusarkar/Indian-Laws from Hugging Face...")
    ds = load_dataset("mratanusarkar/Indian-Laws", split="train")
    df = pd.DataFrame(ds)

    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing columns: {missing}. Found: {list(df.columns)}")

    print(f"Loaded {len(df)} total rows from dataset.")
    print("Filtering and formatting unique legal sections...\n")

    rows = []
    for _, row in df.iterrows():
        doc_types = matches_any_filter(row["act_title"])
        if doc_types is None:
            continue

        sec_num, sec_title, content = clean_section_data(
            act_name=row["act_title"],
            raw_section=row.get("section", ""),
            raw_law=row.get("law", ""),
        )

        if len(content) <= 10:
            continue

        # Single unique row per section with comma-separated multi-label doc_types
        rows.append({
            "act_name": row["act_title"].strip(),
            "section_number": sec_num,
            "section_title": sec_title,
            "content": content,
            "doc_types": ",".join(doc_types),
        })

    filtered_df = pd.DataFrame(rows)
    # Deduplicate by act_name and section_number (1 row per section)
    filtered_df = filtered_df.drop_duplicates(subset=["act_name", "section_number"])

    # Verification check
    matched_acts = set(filtered_df["act_name"].unique())
    if not any("contract" in a.lower() for a in matched_acts):
        raise RuntimeError("Verification failed: Indian Contract Act not found in filtered data.")

    if filtered_df.empty:
        raise RuntimeError("Filtering produced 0 rows. Check ACT_FILTERS keywords.")

    print(f"Successfully extracted {len(filtered_df)} UNIQUE sections across {len(matched_acts)} acts:")
    for act, count in filtered_df.groupby("act_name").size().items():
        print(f"  - {act}: {count} sections")

    data_dir = Path(__file__).resolve().parent.parent / "data" / "acts"
    data_dir.mkdir(parents=True, exist_ok=True)
    output_path = data_dir / "filtered_legal_sections.csv"
    filtered_df.to_csv(output_path, index=False)
    print(f"\nSaved clean CSV to: {output_path}")

    # Preview
    print("\n-- Preview (first 3 unique rows) --")
    for _, row in filtered_df.head(3).iterrows():
        print(f"Act:       {row['act_name']}")
        print(f"Section:   Section {row['section_number']}: {row['section_title']}")
        print(f"Doc Types: {row['doc_types']}")
        print(f"Content:   {row['content'][:140]}...\n")


if __name__ == "__main__":
    main()
