# CSI 5810 Midterm — Group 3 — Requirement-to-deliverable map

This file maps every item in `CSI_5810_Midterm_Project_Guidelines.pdf` to where it is satisfied.
`NB §x` = section x of `code/bank_marketing_midterm.ipynb`; `Paper §x` = section x of `paper/main.tex` / `paper/main.pdf`.
Paper numbering (main body): Fig. 1 target & drift; Fig. 2 ROC/PR; Fig. 3 reliability diagrams; Fig. 4 cost curves & gains;
Table I model comparison; Table II campaign policies; Table III cost-ratio sensitivity; Table IV confusion matrices;
Table V prediction examples (confident TP, TN, FN, FP); Table VI sensitivity analyses. Appendix: Fig. 5 categorical rates; Fig. 6 correlation; Fig. 7 numeric
distributions; Fig. 8 feature importance; Fig. 9 partial dependence; Fig. 10 subgroups; Table VII audit; Table VIII grids;
Table IX temporal cost view; Table X data dictionary; Table XI subgroup table.

## Deliverables

| Deliverable | Location | Status |
|---|---|---|
| IEEE-format technical report (4–6 pages main content, two columns, numbered sections, IEEE citations) | `paper/main.tex` + `paper/references.bib` + `paper/figures/` + `paper/tables/`; Overleaf upload: `paper/overleaf_group3_bank_marketing.zip`; compiled: `paper/main.pdf` (Sections I–VII end at the top of page 7; contribution statement, AI disclosure and references follow; appendix on pages 8–12) | done |
| Reproducible notebook with setup instructions, data paths, seeds, separated stages, generated tables/figures | `code/bank_marketing_midterm.ipynb` (executed, 44 cells, no errors), `code/README.md`, `code/requirements.txt`, `code/outputs/` | done |
| Contribution statement | Paper, "Contribution Statement" (red note to remove); `PROJECT_LOG.md` | **template — group must confirm roles** |
| Project log / meeting record | `PROJECT_LOG.md` | **template — group must fill dates/decisions** |
| Link/archive of shared workspace | `PROJECT_LOG.md` (placeholder) | **group must add link** |
| Generative-AI disclosure | Paper, "Generative-AI Disclosure"; NB §14; `code/README.md`; `PROJECT_LOG.md` | done |
| Group presentation / narrated walkthrough (final checklist item) | not produced | **group must record** |

## Stage 1 — Problem formulation (10 pts)

| Requirement | Where |
|---|---|
| One focused, evaluable question | Paper §I (bold research question); NB header |
| Practical motivation | Paper §I |
| Unit of analysis | Paper §II-B (one contacted client) |
| Inputs and target | Paper §II-B; Table X; NB §2 |
| Task type | Paper §II-B (binary classification, rare positive) |
| Intended user / decision supported | Paper §II-B (campaign manager, whom to call) |
| Assumptions and success criteria | Paper §II-B (cost model c = €5, v = €50; AP, ECE < 0.02, net value > call-everyone) |

## Stage 2 — Data acquisition and documentation (10 pts)

| Requirement | Where |
|---|---|
| Dataset name, source, public URL, access date | Paper §II-A; NB §2; `code/README.md` |
| Size, attributes, labels, data types | Paper §II-B + Table X (data dictionary); NB §2 |
| Collection context, sampling limitations | Paper §II-A, §VI-E |
| License, privacy, permitted use | Paper §II-A (CC BY 4.0, no identifiers) |
| Missing values, duplicates, inconsistent values, outliers, imbalance, leakage | Paper §II-C + Table VII; NB §3 |

## Stage 3 — Exploratory data analysis (15 pts)

| Requirement | Where |
|---|---|
| Data dictionary / variable summary | Paper Table X; NB §2 |
| Target distribution | Paper Fig. 1(a); NB §4.1 |
| Distributions of important numeric and categorical variables | Paper Fig. 5 (categorical), Fig. 7 (numeric by class); NB §4.2–4.3 |
| Relationships between features and target | Paper Fig. 5, §III-A; NB §4.3–4.4 (Cramér's V, point-biserial table) |
| Correlation / association analysis | Paper Fig. 6, §III-A; NB §4.4 |
| Written interpretation of patterns and data-quality findings | Paper §III-A, §II-C; NB §3–4 interpretation cells |
| Readable labels, units, legends, captions, purpose | all figures captioned and discussed in text |

## Stage 4 — Data preparation and feature engineering (part of 15 pts)

| Requirement | Where |
|---|---|
| Missing values, duplicates, outliers, invalid records | Paper §III-B; NB §5 |
| Encoding of categorical values | Paper §III-B (one-hot / ordinal + native categorical); NB §5 |
| Scaling of numeric features | Paper §III-B (standardised for LR/k-NN); NB §5 |
| Text preprocessing | n/a (no text) |
| Feature selection / transformation / construction | `pdays` sentinel → indicator; `duration` removed (Paper §III-B; NB §5) |
| Train/validation/test splitting or cross-validation | stratified 80/20 + 5-fold CV inside training (Paper §III-B; NB §5–6) |
| Leakage prevention | pipelines fitted per fold; OOF thresholds; CV calibration (Paper §III-B, §IV-B/C; NB §5, §8, §9) |

## Stage 5 — Baseline and analytical methods

| Requirement | Where |
|---|---|
| At least one simple baseline | majority-class / prior baseline (Paper §IV-A; NB §6) |
| At least two meaningful approaches | LR, k-NN, RF, GB (Paper §IV-A; NB §6) |
| For each method: appropriateness, assumptions, hyperparameters and selection, trade-offs | Paper §IV-A + Table VIII (grids); NB §6 table |

## Stage 6 — Evaluation and comparison (20 pts)

| Requirement | Where |
|---|---|
| Metrics matching the task (≥ 3) | AP, ROC-AUC, Brier, log loss, ECE, precision, recall, F1, balanced accuracy, specificity (Paper Table I, §V-D; NB §7, §10) |
| Confusion matrix | Paper Table IV + §V-D text; NB §10 (figure + table) |
| Explain what the metric measures and why appropriate | Paper §IV-B, §IV-C |
| Uncertainty / variation across folds / sensitivity | CV s.d. and bootstrap CIs (Table I), paired differences (§V-A), cost-ratio sensitivity (Table III), modelling-choice sensitivity (Table VI) |
| Class imbalance and consequences of FP/FN | Paper §II-C, §IV-C, §V-D (asymmetric costs), §VI-D (class weighting) |
| Precision, recall, calibration, expected campaign cost (project-specific) | Paper §V-B (Fig. 3), §V-C (Fig. 4, Tables II–III); NB §8–9 |

## Stage 7 — Interpretation, error analysis, limitations (15 pts)

| Requirement | Where |
|---|---|
| Examples of correct and incorrect predictions | Paper Table V (two confident TP, TN, FN and FP each) and §VI-B; NB §12 (five of each kind) |
| Most important variables | Paper §VI-A, Fig. 8 (permutation importance, LR coefficients), Fig. 9 (PDP); NB §11 |
| Patterns in errors, class imbalance, subgroup performance | Paper §VI-B (by month, previous outcome), §VI-C + Fig. 10 + Table XI; NB §12 |
| Effect of changing at least one modelling choice | Paper §VI-D, Table VI, Table IX (leakage variable, temporal vs random split, class weighting); NB §13 |
| Limitations (data quality, sampling, generalisation, privacy, fairness, computation, reproducibility) | Paper §VI-E |
| Two or more realistic improvements | Paper §VI-E (four next steps) |
| Responsible use / fairness / privacy | Paper §VI-C, §VI-E |

## Reproducibility and report quality (10 pts)

| Requirement | Where |
|---|---|
| Setup instructions and packages | `code/README.md`, `code/requirements.txt`, NB header |
| Documented data path / download instructions | `code/README.md`, NB §1 (`BANK_DATA_PATH`) |
| Random seeds | `SEED = 5810` everywhere (NB §1) |
| Separation of preparation / EDA / modelling / evaluation / visualisation | NB §2–§14 |
| Generates principal tables, figures, metrics | `code/outputs/` (tables as CSV + .tex, figures as PDF + PNG, `results.json`); the paper `\input`s these tables and includes these figures |
| Manual steps / unavailable data explained | `code/README.md` (none beyond the public download) |
| Comments for important decisions | NB code comments and markdown cells |

## Automated verification (2026-09-30)

`code/verify_requirements.py` checks the compiled paper, the executed notebook and the generated outputs against
the guideline items above (section presence, every figure/table referenced in the text, citations resolving to the
bib file, page budget, required analyses, notebook execution without errors, paper tables byte-identical to notebook
outputs, headline numbers in the text matching `results.json`). The full output is in `VERIFICATION_REPORT.txt`.
Every check passes except "version control / shared workspace with history": the project folder is not a git
repository (`git init` plus a commit by the group satisfies that guideline). `code/scan_writing.py` checks the paper
source for em dashes and machine-sounding phrasing; the paper contains none (remaining matches are the title's
question, the research question itself, and LaTeX float specifiers).

Citations (2026-10-01): all 15 entries in `paper/references.bib` were checked against Crossref/DataCite DOI records,
OpenAlex, the UCI dataset page, JMLR, Project Euclid, the AAAI and NeurIPS proceedings pages and library records
(titles, authors, venues, volumes, pages, years). Each entry is cited at least once, and each citation supports a
specific claim or method (dataset provenance, leakage, the four learners, AP for imbalanced data, Brier score,
ECE, bootstrap intervals, calibration and isotonic regression, the Bayes cost threshold, permutation importance,
partial dependence, dataset shift). The LightGBM paper is cited without page numbers because the official NeurIPS
proceedings are unpaginated and secondary sources disagree.

## Items the group must complete before submission

1. Confirm or replace the role split in the paper's Contribution Statement (remove the red note) and fill `PROJECT_LOG.md` (dates, decisions, owners, workspace link).
2. Add the other members' e-mail addresses to the author block if the instructor expects them.
3. Record the group presentation / narrated walkthrough.
4. Upload `paper/overleaf_group3_bank_marketing.zip` to Overleaf (New Project → Upload Project, compiler pdfLaTeX) and recompile, or submit `paper/main.pdf` directly.
5. Confirm the project-selection e-mail to the instructor was sent with all members CC'ed.
