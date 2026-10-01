"""Evidence-based verification of the CSI 5810 midterm guideline requirements against the actual artifacts."""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\Andrew Aurand\ccsi5810_midterm_group")
PAPER, CODE = ROOT / "paper", ROOT / "code"
tex = (PAPER / "main.tex").read_text(encoding="utf-8")
bib = (PAPER / "references.bib").read_text(encoding="utf-8")
raw_pdf = subprocess.run(["pdftotext", str(PAPER / "main.pdf"), "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
pages = raw_pdf.split("\f")
# normalised text: join line breaks and collapse whitespace so phrases can be matched across lines; a line-end hyphen
# may be a soft hyphen (cam-/paign) or a real one (high-/volume), so both readings are searched
pdf_variants = [re.sub(r"\s+", " ", re.sub(r"-\n(?=[a-z])", "", raw_pdf)),
                re.sub(r"\s+", " ", re.sub(r"-\n(?=[a-z])", "-", raw_pdf))]
pdf_text = pdf_variants[0]
import nbformat
nb = nbformat.read(str(CODE / "bank_marketing_midterm.ipynb"), as_version=4)
nb_md = "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
nb_code = "\n".join(c.source for c in nb.cells if c.cell_type == "code")
results = json.loads((CODE / "outputs" / "results.json").read_text(encoding="utf-8"))

report = []
def check(ok, item, evidence=""):
    report.append(("PASS" if ok else "FAIL", item, evidence))
def in_pdf(pattern, flags=re.I):
    return any(re.search(pattern, v, flags) is not None for v in pdf_variants)

# ---------------- Report structure (deliverable 1) ----------------
check(in_pdf(r"Group 3"), "Title block names the group number")
for name in ["Andrew Aurand", "Christina Carvalho", "Cameron Clark", "Tyler Donovan"]:
    check(in_pdf(name), f"Member name present: {name}")
check(in_pdf(r"Abstract"), "Abstract present")
check(in_pdf(r"Index Terms"), "Index terms present")
for sec in ["INTRODUCTION", "DATASET AND PROBLEM DEFINITION", "DATA PREPARATION AND EXPLORATORY ANALYSIS",
            "METHODS AND EXPERIMENTAL DESIGN", "RESULTS AND DISCUSSION", "ERROR ANALYSIS, LIMITATIONS, AND RESPONSIBLE",
            "CONCLUSION", "REFERENCES", "CONTRIBUTION STATEMENT", "GENERATIVE-AI DISCLOSURE", "APPENDIX"]:
    check(in_pdf(re.escape(sec)), f"Section present: {sec}")
check(re.search(r"^\s*(I|II|III|IV|V|VI|VII)\.\s+[A-Z]", raw_pdf, re.M) is not None, "Sections are numbered (IEEE roman numerals)")
check("\\documentclass[conference]{IEEEtran}" in tex, "IEEE conference template, two columns")
check(in_pdf(r"\[1\] S\. Moro, P\. Cortez, and P\. Rita"), "IEEE-style numbered reference list")
cites = set(re.findall(r"\\cite\{([^}]*)\}", tex)); cite_keys = {k.strip() for c in cites for k in c.split(",")}
bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
check(cite_keys <= bib_keys, "All in-text citations resolve to bib entries", f"{len(cite_keys)} keys; missing={sorted(cite_keys - bib_keys)}")
check(bib_keys <= cite_keys, "All bib entries are cited", f"uncited={sorted(bib_keys - cite_keys)}")
labels = re.findall(r"\\label\{([^}]+)\}", tex)
body_no_floats = re.sub(r"\\begin\{(figure\*?|table\*?)\}.*?\\end\{\1\}", "", tex, flags=re.S)
unref = [l for l in labels if not re.search(r"\\ref\{" + re.escape(l) + r"\}", body_no_floats)]
check(not unref, "Every figure and table is referenced/discussed in the text", f"labels={len(labels)}; unreferenced={unref}")
floats = re.findall(r"\\begin\{(?:figure\*?|table\*?)\}.*?\\end\{(?:figure\*?|table\*?)\}", tex, flags=re.S)
check(all("\\caption{" in f for f in floats), f"Every float has a caption ({len(floats)} floats)")
check(not re.search(r"%%[A-Z]+%%", tex), "No unfilled placeholders left in main.tex", str(re.findall(r"%%[A-Z]+%%", tex)))

def page_of(pattern):
    for i, p in enumerate(pages, 1):
        if re.search(pattern, p): return i
    return None
p_concl, p_contrib, p_app = page_of(r"VII\. CONCLUSION"), page_of(r"CONTRIBUTION STATEMENT"), page_of(r"APPENDIX")
spill_lines = 0
if p_contrib and p_concl and p_contrib > p_concl:
    spill_lines = len(pages[p_contrib - 1].split("CONTRIBUTION STATEMENT")[0].strip().splitlines())
check(p_concl is not None and 4 <= p_contrib <= 7 and (p_contrib <= 6 or spill_lines <= 6),
      "Main technical content (Sections I-VII) within 4-6 pages",
      f"Conclusion starts p{p_concl}; contribution statement p{p_contrib}; {spill_lines} line(s) of conclusion on p{p_contrib}; appendix p{p_app}; {len(pages)-1} pages total")

# ---------------- Stage 1: problem formulation ----------------
check(in_pdf(r"Research question\. Can we predict"), "One focused, evaluable research question")
check(in_pdf(r"Each of the 41,188 rows is one client"), "Unit of analysis stated")
check(in_pdf(r"intended user is the campaign manager"), "Intended user / decision stated")
check(in_pdf(r"binary classification with an uncommon positive class"), "Task type stated")
check(in_pdf(r"Success means"), "Assumptions and success criteria stated")

# ---------------- Stage 2: data documentation ----------------
check(in_pdf(r"dataset 222") and in_pdf(r"archive\.ics\.uci\.edu"), "Dataset name, source and public URL")
check(in_pdf(r"accessed on 30 September 2026"), "Access date")
check(in_pdf(r"41,188") and in_pdf(r"20 inputs"), "Dataset size and attributes")
check(in_pdf(r"CC BY 4\.0"), "License stated")
check(in_pdf(r"no direct identifiers"), "Privacy / permitted use")
check(in_pdf(r"financial crisis") and in_pdf(r"one bank"), "Collection context and sampling limitations")
for kw, label in [(r"duplicate", "duplicates"), (r"unknown", "missing values (unknown)"), (r"sentinel", "inconsistent/sentinel values"),
                  (r"up to 56 times", "outliers"), (r"11\.3%", "imbalance"), (r"leakage", "leakage")]:
    check(in_pdf(kw), f"Data-quality issue discussed: {label}")

# ---------------- Stage 3: EDA ----------------
check("tab:dictionary" in labels, "Data dictionary table")
check(in_pdf(r"Class balance"), "Target distribution figure")
check("fig:cat" in labels and "fig:numeric" in labels, "Distributions of categorical and numeric variables")
check("fig:corr" in labels and in_pdf(r"Cram"), "Correlation / association analysis")
check(in_pdf(r"shows the two facts that shape the study"), "Written interpretation of EDA patterns")

# ---------------- Stage 4: preparation ----------------
for kw, label in [(r"one-hot", "encoding of categoricals"), (r"standardised", "scaling"), (r"prev.contacted", "feature construction"),
                  (r"stratified 20% test set", "train/test split"), (r"5-fold cross-validation", "cross-validation"),
                  (r"fitted only on the training portion", "leakage prevention (transformers fit on train folds)"),
                  (r"duplicates are dropped", "duplicates handled"), (r"outliers are kept", "outliers handled")]:
    check(in_pdf(kw), f"Preparation decision explained: {label}")

# ---------------- Stage 5: methods ----------------
check(in_pdf(r"Majority-class baseline"), "Simple baseline present")
n_models = sum(in_pdf(m) for m in [r"Logistic regression", r"k-NN", r"Random forest", r"gradient boosting"])
check(n_models >= 2, f"At least two comparison methods ({n_models} found)")
check(in_pdf(r"assumes additive effects") and in_pdf(r"assumes local smoothness"), "Assumptions stated per method")
check("tab:grids" in labels and in_pdf(r"selected rate 0\.03"), "Hyperparameters and selection documented")
check(in_pdf(r"trade-off is interpretability"), "Interpretability/complexity/computation/performance trade-off discussed")

# ---------------- Stage 6: evaluation ----------------
metrics = [m for m in ["AP", "ROC-AUC", "Brier", "log loss", "ECE", "precision", "recall", "F1", "balanced accuracy", "specificity"] if in_pdf(re.escape(m))]
check(len(metrics) >= 3, f"At least three suitable metrics reported ({len(metrics)})")
check("tab:cm" in labels, "Confusion matrix reported")
check(in_pdf(r"because it focuses on the rare positive class") and in_pdf(r"mean squared error of the probabilities"), "Metrics explained and justified")
check(in_pdf(r"bootstrap confidence interval") and in_pdf(r"fold-to-fold"), "Uncertainty: fold variation and bootstrap CIs")
check(in_pdf(r"paired bootstrap"), "Paired comparison between models")
check(in_pdf(r"false positive wastes one") and in_pdf(r"false negative forgoes"), "Consequences of FP and FN discussed")
check(in_pdf(r"88\.7% accurate and useless"), "Class imbalance consequences discussed")
check("fig:cal" in labels and in_pdf(r"isotonic"), "Calibration assessed (project-specific requirement)")
check("tab:strat" in labels and in_pdf(r"net value"), "Expected campaign cost / value evaluated (project-specific requirement)")
check("tab:ratio" in labels, "Sensitivity to cost assumptions")

# ---------------- Stage 7: interpretation / error analysis ----------------
check(in_pdf(r"false negatives") and in_pdf(r"false positives") and "tab:examples" in labels, "Concrete examples of incorrect predictions")
check(in_pdf(r"true positives") and in_pdf(r"TP: called and subscribed"), "Concrete examples of correct predictions")
check("fig:imp" in labels and in_pdf(r"Permutation importance"), "Most important variables")
check(in_pdf(r"recall of the rule is lowest in the high-?volume months"), "Patterns in errors")
check("fig:sub" in labels and "tab:subgroups" in labels, "Subgroup analysis")
check("tab:sens" in labels and in_pdf(r"Temporal validation") and in_pdf(r"Class weighting") and in_pdf(r"Leakage\."), "Effect of changing modelling choices (3 experiments)")
for kw, label in [(r"one bank, one country", "sampling/generalisation"), (r"de-?identified", "privacy"), (r"fairness", "fairness"),
                  (r"reproducible", "reproducibility"), (r"Computation is not a constraint", "computation"), (r"omits some attributes", "data quality")]:
    check(in_pdf(kw), f"Limitation discussed: {label}")
check(in_pdf(r"Next steps: \(1\)") and in_pdf(r"\(2\)"), "Two or more realistic improvements")
check(in_pdf(r"decision support for prioritising calls, not for denying service"), "Responsible-use statement")

# ---------------- Deliverable 2: notebook ----------------
check("How to run this notebook" in nb_md and "requirements.txt" in nb_md, "Notebook: setup instructions and packages")
check("BANK_DATA_PATH" in nb_code and "archive.ics.uci.edu" in nb_md, "Notebook: documented data path / download instructions")
check("SEED = 5810" in nb_code and nb_code.count("random_state=SEED") >= 5, "Notebook: random seeds set", f"random_state=SEED used {nb_code.count('random_state=SEED')} times")
secs = [s for s in ["## 2. Data acquisition", "## 3. Data-quality audit", "## 4. Exploratory", "## 5. Data preparation", "## 6. Baseline", "## 7. Held-out", "## 8. Probability calibration", "## 9. Cost-sensitive", "## 11. Model interpretation", "## 12. Error analysis", "## 13. Sensitivity"] if s in nb_md]
check(len(secs) == 11, f"Notebook: stages separated into sections ({len(secs)}/11 found)")
errs = [i for i, c in enumerate(nb.cells) if c.cell_type == "code" and any(o.get("output_type") == "error" for o in c.get("outputs", []))]
code_cells = [c for c in nb.cells if c.cell_type == "code"]
executed = sum(1 for c in code_cells if c.get("execution_count"))
check(not errs and executed == len(code_cells), "Notebook fully executed without errors", f"{executed}/{len(code_cells)} code cells executed; error cells={errs}")
figs = sorted(p.name for p in (CODE / "outputs" / "figures").glob("*.pdf")); tabs = sorted(p.name for p in (CODE / "outputs" / "tables").glob("*.tex"))
check(len(figs) == 11 and len(tabs) >= 20, "Notebook generates the report's figures and tables", f"{len(figs)} figures, {len(tabs)} tables")
paper_figs = set(re.findall(r"\\includegraphics\[[^\]]*\]\{([^}]+)\}", tex)); paper_tabs = set(re.findall(r"\\input\{tables/([^}]+)\}", tex))
missing_f = [f for f in paper_figs if f not in figs]; missing_t = [t for t in paper_tabs if t not in tabs]
check(not missing_f and not missing_t, "Every paper figure/table file is produced by the notebook", f"missing figures={missing_f}; missing tables={missing_t}")
same = all((PAPER / "tables" / t).read_bytes() == (CODE / "outputs" / "tables" / t).read_bytes() for t in paper_tabs if (CODE / "outputs" / "tables" / t).exists())
check(same, "Paper tables are byte-identical to the notebook outputs")
check((CODE / "README.md").exists() and "Manual steps" in (CODE / "README.md").read_text(encoding="utf-8"), "README explains manual steps / reproduction limits")
md_cells = sum(1 for c in nb.cells if c.cell_type == "markdown")
check(nb_code.count("#") >= 60 and md_cells >= 15, "Notebook documents important decisions (comments + markdown)", f"{nb_code.count('#')} comment markers, {md_cells} markdown cells")
check("Generative-AI disclosure" in nb_md, "Notebook contains the generative-AI disclosure")

# ---------------- Deliverable 3: collaboration record ----------------
log = (ROOT / "PROJECT_LOG.md").read_text(encoding="utf-8")
check("Meeting record" in log and "Roles" in log, "Project log with roles, meetings, task ownership (TEMPLATE: group must fill)", "[EDIT] markers present" if "[EDIT" in log else "")
check(in_pdf(r"Confirm the role split"), "Contribution statement present (TEMPLATE: group must confirm roles and remove the red note)")
check(in_pdf(r"Claude"), "Generative-AI disclosure in the report")
check((ROOT / ".git").exists(), "Version control / shared workspace with history", "no .git directory in the project folder")

# ---------------- consistency of key numbers between text and results.json ----------------
best = results["best_model"]; t = results["test"][best]
check(in_pdf(rf"{t['AP']['value']:.3f}") and in_pdf(rf"{t['ROC-AUC']['value']:.3f}"), "Headline test metrics in the text match results.json", f"AP={t['AP']['value']:.4f}, AUC={t['ROC-AUC']['value']:.4f}")
fr = results["final_rule"]
check(in_pdf(rf"{100*fr['call rate']:.1f}%") and in_pdf(rf"{100*fr['recall']:.1f}%") and in_pdf(rf"{fr['net value per 1000']:,.0f}"), "Final-rule numbers in the text match results.json", f"call rate={100*fr['call rate']:.1f}%, recall={100*fr['recall']:.1f}%, net={fr['net value per 1000']:,.0f}")
ev = results["cost"]["strategies"]["Call everyone (current practice)"]
check(in_pdf(rf"{ev['net value per 1000']:,.0f}"), "Call-everyone value in the text matches results.json", f"{ev['net value per 1000']:,.0f}")

fails = [r for r in report if r[0] == "FAIL"]
for status, item, ev_ in report:
    print(f"[{status}] {item}" + (f"  -- {ev_}" if ev_ else ""))
print(f"\n{len(report) - len(fails)} passed, {len(fails)} failed")
