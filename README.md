# LedgerLens
### Explainable Financial Entity Resolution & Payment Intelligence

LedgerLens is a small, review-first prototype for comparing business records that may refer to the same real-world entity, surfacing duplicate transaction references and displaying supplied relationships.

## What is implemented
- Business-name normalization while retaining original values.
- Pairwise comparison using name similarity, exact registration-ID comparison and address similarity.
- Explicit investigation route when two non-empty registration IDs conflict.
- Evidence output for each pair and heuristic review bands.
- Duplicate transaction-reference flags.
- A simple median-absolute-deviation amount outlier signal.
- NetworkX relationship graph and Streamlit dashboard.
- 12 automated unit tests.

## What is not implemented
- No LLM or OCR extraction in the running prototype.
- No external company registry, bank integration or real customer data.
- No automated entity merging, fraud decision, payment block or adverse action.
- No calibrated production probability or real-world accuracy claim.
- No production authentication, authorization or immutable audit service.

## Run locally
Python 3.10+ recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app/dashboard.py
```

## Data and safety
All data under `data/synthetic/` is invented for demonstration. Similarity scores are heuristic scores, not probabilities. A duplicate or outlier flag is an investigation signal, not proof of fraud. No record pair is automatically merged.

## Architecture
See `docs/architecture_refined.png`. The pipeline is: ingest → normalize → compare candidates → produce evidence and review recommendation → show payment signals and graph → human review.

## Matching logic
The illustrative score is:
`0.65 × name similarity + 0.25 × exact registration-ID match + 0.10 × address similarity`.

If both registration IDs are present and differ, the recommendation is overridden to `INVESTIGATE_IDENTIFIER_CONFLICT`. Score bands are illustrative and require calibration on labelled, representative data. They are not probabilities.

## Test coverage
Run `python -m unittest discover -s tests -v`. The included tests cover normalization, matching behavior, identifier conflicts, no automatic merge, duplicate references, graph construction and score bounds. These are software unit tests, not a real-world model benchmark.

## Known limitations and next steps
The all-pairs candidate generator is quadratic and only suitable for this small dataset. Address comparison is simplistic. The heuristic score is not calibrated. Next steps are to create a larger labelled evaluation set, improve candidate blocking, measure precision/recall and false-match rates, add provenance and append-only review events, and evaluate any future LLM extraction against manually verified source documents.
