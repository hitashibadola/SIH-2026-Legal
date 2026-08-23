"""
Reads filtered_legal_sections.csv, removes administrative/procedural
boilerplate (e.g. 'short title', 'power to make rules', 'repeals'),
drops obsolete/irrelevant acts, and saves cleaned_legal_sections.csv.

Usage:
    .\venv\Scripts\python.exe .\scripts\clean_legal_csv.py
"""

from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "acts"
INPUT_FILE = DATA_DIR / "filtered_legal_sections.csv"
OUTPUT_FILE = DATA_DIR / "cleaned_legal_sections.csv"

# Acts to explicitly exclude (obsolete, territorial military, or superseded)
EXCLUDED_ACT_KEYWORDS = [
    "cantonment",
    "east punjab",
    "delhi and ajmer",
    "consumer protection act, 1986",  # Superseded by Consumer Protection Act, 2019
]

# Section title keywords that indicate pure administrative/procedural boilerplate
BOILERPLATE_TITLE_KEYWORDS = [
    "short title",
    "extent and commencement",
    "commencement and application",
    "power to make rule",
    "power of central government to make rule",
    "power of state government to make rule",
    "power to make regulation",
    "laying of rule",
    "laying of regulation",
    "power to remove difficult",
    "repeal and saving",
    "repeals and saving",
    "repeal of act",
    "annual report",
    "accounts and audit",
    "audit of accounts",
    "members to be public servant",
    "protection of action taken in good faith",
    "vacancies not to invalidate",
    "authentication of order",
    "delegation of power",
]


def is_excluded_act(act_name: str) -> bool:
    """Returns True if the act is obsolete or irrelevant."""
    name_lower = act_name.lower()
    return any(kw in name_lower for kw in EXCLUDED_ACT_KEYWORDS)


def is_boilerplate_section(section_num: str, section_title: str, content: str) -> bool:
    """Returns True if the section is procedural/administrative boilerplate rather than substantive law."""
    title_lower = section_title.lower() if isinstance(section_title, str) else ""

    # Check title keywords
    if any(kw in title_lower for kw in BOILERPLATE_TITLE_KEYWORDS):
        return True

    # Drop Section 1 if it only contains short title / commencement text
    if str(section_num).strip() == "1":
        if not title_lower or any(kw in title_lower for kw in ["short title", "preliminary", "title", "chapter i"]):
            return True

    # Drop sections where content is just "Repealed" or "Omitted"
    content_clean = content.lower().strip()
    if content_clean.startswith("repealed by") or content_clean.startswith("[repealed") or content_clean == "repealed.":
        return True

    return False


def main():
    print(f"Reading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    initial_count = len(df)
    print(f"Initial count: {initial_count} sections across {df['act_name'].nunique()} acts.\n")

    # 1. Filter out obsolete/irrelevant acts
    df = df[~df["act_name"].apply(is_excluded_act)]
    after_act_filter = len(df)
    print(f"Removed {initial_count - after_act_filter} sections from obsolete/excluded acts.")

    # 2. Filter out boilerplate/procedural sections
    is_noise = df.apply(
        lambda r: is_boilerplate_section(
            section_num=str(r["section_number"]),
            section_title=str(r["section_title"]),
            content=str(r["content"]),
        ),
        axis=1,
    )
    cleaned_df = df[~is_noise].copy()
    removed_boilerplate = len(df) - len(cleaned_df)
    print(f"Removed {removed_boilerplate} boilerplate/administrative sections.")

    # 3. Verification: ensure essential substantive acts and sections exist
    matched_acts = set(cleaned_df["act_name"].unique())
    if not any("contract" in a.lower() for a in matched_acts):
        raise RuntimeError("Verification failed: Indian Contract Act missing after cleanup.")

    contract_sections = cleaned_df[cleaned_df["act_name"].str.contains("Contract", case=False)]
    if "27" not in contract_sections["section_number"].astype(str).values:
        raise RuntimeError("Verification failed: Section 27 (Non-compete) missing from Contract Act.")

    print(f"\nFinal count: {len(cleaned_df)} SUBSTANTIVE legal sections across {len(matched_acts)} acts:")
    for act, count in cleaned_df.groupby("act_name").size().items():
        print(f"  - {act}: {count} sections")

    cleaned_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved clean substantive dataset to: {OUTPUT_FILE}")

    # Preview
    print("\n-- Preview (3 sample substantive sections) --")
    for _, row in cleaned_df.head(3).iterrows():
        print(f"Act:       {row['act_name']}")
        print(f"Section:   Section {row['section_number']}: {row['section_title']}")
        print(f"Doc Types: {row['doc_types']}")
        print(f"Content:   {row['content'][:140]}...\n")


if __name__ == "__main__":
    main()
