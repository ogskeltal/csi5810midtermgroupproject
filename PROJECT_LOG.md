# CSI 5810 Midterm Project — Group 3 — Project Log and Contribution Record

**Project:** Predicting term-deposit subscription with cost-sensitive evaluation (Bank Marketing, UCI dataset 222)
**Members:** Andrew Aurand (G), Christina Carvalho (U), Cameron Clark (U), Tyler Donovan (U)

> **[EDIT BEFORE SUBMISSION]** The roles, dates and task ownership below are a template filled with the
> role assignment suggested by the guidelines (coordinator = graduate student). Replace every bracketed item
> with what the group actually did. The same statement must appear, in condensed form, in the
> "Contribution statement" section of the report (`paper/main.tex`).

## Roles

| Role | Member | Notes |
|---|---|---|
| Group coordinator | Andrew Aurand | [EDIT] schedules meetings, maintains this log, owns the shared workspace |
| Data-preparation lead | [EDIT: e.g., Christina Carvalho] | [EDIT] |
| Modeling lead | [EDIT: e.g., Cameron Clark] | [EDIT] |
| Evaluation lead | [EDIT: e.g., Tyler Donovan] | [EDIT] |
| Report lead | [EDIT] | [EDIT] |

Roles may overlap; every member must have a documented technical contribution.

## Shared workspace

* Code and report: private GitHub repository <https://github.com/ogskeltal/csi5810midtermgroupproject> (owner: Andrew Aurand; add the other members and, if required, the instructor as collaborators)
* Report source: Overleaf project [EDIT: link], built from `paper/overleaf_group3_bank_marketing.zip`.

## Meeting record

| Date | Attendees | Decisions | Action items (owner) |
|---|---|---|---|
| [EDIT: date] | all | Reviewed the three Set C options; selected **Bank Marketing** (richest dataset, clear cost-sensitive angle); emailed the instructor for approval with all members CC'ed. | Download data and draft research question (Andrew) |
| [EDIT: date] | all | Research question fixed: *Can we predict, before a call, which clients will subscribe, and does targeting calls with the model reduce campaign cost versus calling everyone?* Decided to drop `duration` (leakage), keep `unknown` as a category, use a stratified 80/20 split with 5-fold CV inside the training set. | Data audit + EDA ([EDIT]); modeling pipeline ([EDIT]) |
| [EDIT: date] | all | Cost model agreed: EUR 5 per call, EUR 50 per subscription (ratio 0.10), with a sensitivity grid 0.05-0.30. Metrics: AP (primary), ROC-AUC, Brier, ECE, precision/recall at policy thresholds, net value per 1,000 clients. | Calibration + cost analysis ([EDIT]); sensitivity analyses ([EDIT]) |
| [EDIT: date] | all | Reviewed results; chose the final rule (selected model, isotonic calibration, threshold = cost ratio). Agreed on the temporal-drift limitation as a key finding. Assigned report sections. | Report draft ([EDIT]); figure polish ([EDIT]) |
| [EDIT: date] | all | Final review of notebook, report, checklist; verified every member can explain the methods. | Submission (Andrew) |

## Task ownership and code contributions

| Task | Owner(s) | Evidence |
|---|---|---|
| Data acquisition, documentation, quality audit (notebook Sections 2-3) | [EDIT] | commits / notebook cells |
| Exploratory analysis and figures (Section 4) | [EDIT] | |
| Preparation pipelines and leakage controls (Section 5) | [EDIT] | |
| Model selection and hyperparameter search (Section 6) | [EDIT] | |
| Test evaluation, bootstrap CIs, calibration (Sections 7-8) | [EDIT] | |
| Cost-sensitive evaluation and operating points (Sections 9-10) | [EDIT] | |
| Interpretation, error analysis, subgroups (Sections 11-12) | [EDIT] | |
| Sensitivity analyses (Section 13) | [EDIT] | |
| Report writing and LaTeX (paper/) | [EDIT] | |

## Unresolved issues / open questions

* [EDIT] e.g., whether to re-tune hyperparameters under the temporal split (currently reuses the random-split configuration).
* [EDIT] e.g., which cost ratio the "bank" would actually face; the EUR 5 / EUR 50 assumption is illustrative.

## Generative-AI disclosure

Anthropic's Claude (Claude Code) was used to draft and debug the analysis notebook, to structure the
experiments, and to draft and edit the report text and LaTeX. All generated code, results, explanations and
citations were reviewed by the group; the group is responsible for all methodological choices, the
interpretation and the conclusions. [EDIT if other tools were used, e.g., for proofreading.]
