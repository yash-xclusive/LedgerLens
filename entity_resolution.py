import re
from difflib import SequenceMatcher

LEGAL_SUFFIXES = {
    "private", "limited", "pvt", "ltd", "llp", "inc", "incorporated",
    "corporation", "corp", "company", "co"
}

def normalize_name(value: str) -> str:
    """Normalize a business name without discarding its original source value."""
    value = (value or "").lower()
    value = re.sub(r"[^a-z0-9 ]", " ", value)
    tokens = [t for t in value.split() if t not in LEGAL_SUFFIXES]
    return " ".join(tokens)

def similarity(a: str, b: str) -> float:
    na, nb = normalize_name(a), normalize_name(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()

def compare_records(a: dict, b: dict) -> dict:
    """Return transparent evidence and a heuristic score, not a calibrated probability."""
    name_score = similarity(a.get("name", ""), b.get("name", ""))
    reg_a, reg_b = str(a.get("registration_id", "")).strip(), str(b.get("registration_id", "")).strip()
    reg_match = bool(reg_a and reg_b and reg_a == reg_b)
    addr_score = similarity(a.get("address", ""), b.get("address", ""))
    # Registration ID is strong evidence; name and address are supporting evidence.
    score = 0.65 * name_score + 0.25 * float(reg_match) + 0.10 * addr_score
    reasons = [
        {"field": "name", "score": round(name_score, 3), "evidence": "normalized string similarity"},
        {"field": "registration_id", "match": reg_match, "evidence": "exact identifier comparison"},
        {"field": "address", "score": round(addr_score, 3), "evidence": "normalized string similarity"},
    ]
    if score >= 0.88:
        recommendation = "REVIEW_HIGH_SIMILARITY"
    elif score >= 0.68:
        recommendation = "REVIEW_POSSIBLE_MATCH"
    else:
        recommendation = "NO_AUTOMATIC_LINK"
    # Conflicting non-empty identifiers override the score and require investigation.
    if reg_a and reg_b and reg_a != reg_b:
        recommendation = "INVESTIGATE_IDENTIFIER_CONFLICT"
    return {
        "score": round(score, 4),
        "score_type": "heuristic_similarity_not_probability",
        "recommendation": recommendation,
        "evidence": reasons,
        "automatic_merge": False,
    }

def candidate_pairs(records):
    """Small-demo all-pairs candidate generation. Production systems need blocking/indexing."""
    out=[]
    for i in range(len(records)):
        for j in range(i+1, len(records)):
            result=compare_records(records[i], records[j])
            out.append({"record_a": records[i]["record_id"],
                        "record_b": records[j]["record_id"], **result})
    return out
