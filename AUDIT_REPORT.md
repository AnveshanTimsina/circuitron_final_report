# CIRCUITRON Report — Audit Report
### Discrepancies, Contradictions, and Issues
**Audited: March 10, 2026**

---

## SEVERITY LEGEND
- **CRITICAL** — Factually wrong or directly contradictory statements within the report
- **MAJOR** — Significant inconsistency that could undermine credibility if noticed
- **MINOR** — Cosmetic, stylistic, or structural issues
- **NOTE** — Observations and suggestions (not errors)

---

## 1. CRITICAL: OCR Training Epochs — 29 vs 50

| Location | Claim |
|---|---|
| `systemArchitectureAndMethodology.tex` line 697 | *"The training was done for **29 epochs**."* |
| `implementationDetails.tex` line 170 | *"The training was done for **29 epochs**."* |
| `resultAndAnalysis.tex` line 208 | *"the training loss decreases consistently throughout the **50 epochs**"* |
| `resultAndAnalysis.tex` line 412 | *"This model was trained from scratch for **50 epochs** using the DTRB framework."* |
| `resultAndAnalysis.tex` line 431 (Table) | Training Epochs: **50** |
| `resultAndAnalysis.tex` line 447 | *"despite requiring only 3 training epochs compared to **50**"* |

**Verdict:** Two chapters say 29 epochs, the results chapter consistently says 50. One of these numbers is wrong. The commented-out text on line 207 even preserves the old "29 epochs" statement that was replaced with "50 epochs." Likely the OCR was retrained later to 50 epochs, but the implementation chapters were never updated.

---

## 2. CRITICAL: Augmentation Self-Contradiction — "Rotation is Unwise" vs. "We Used Rotation"

| Location | Claim |
|---|---|
| `implementationDetails.tex` line 147 | *"geometric augmentation techniques, like spatial flipping...and rotation...proved to be **unwise** operations for this project...using rotation or flipping would simply **confuse the model**"* |
| `implementationDetails.tex` line 163 | *"Augmentations used in training: Mosaic Augmentation, HSV Augmentation, **Random rotating/flipping**"* |
| `systemArchitectureAndMethodology.tex` line 20 | *"geometric augmentations, especially rotation, is **not appropriate** for this project"* |
| `systemArchitectureAndMethodology.tex` line 674 | Same "unwise" paragraph as implementationDetails |
| `systemArchitectureAndMethodology.tex` line 690 | Same "Random rotating/flipping" in the training params list |

**Verdict:** The text explicitly argues that rotation and flipping confuse the model and are inappropriate. Then, 16 lines later in the same chapter, the training parameter list includes "Random rotating/flipping" as an augmentation actually used. This is a direct self-contradiction within the same section—twice (duplicated across two chapters).

---

## 3. CRITICAL: Training Data Split Inconsistency — 70/10/20 vs. 70/20/10

| Location | Claim |
|---|---|
| `implementationDetails.tex` line 157 | *"70% training, **10% validation, 20% testing**"* |
| `systemArchitectureAndMethodology.tex` line 684 | *"70% training, **10% validation, 20% testing**"* |
| `systemArchitectureAndMethodology.tex` line 811 (Dataset Analysis) | *"the dataset is to be split into **(70-20-10)%** of the entire data for training, validation and testing respectively"* |

**Verdict:** The Dataset Analysis section says 70-20-10 (train-val-test), but both the implementation sections say 70-10-20 (train-val-test). These are opposite val/test splits (10% vs. 20% for validation). One is wrong.

---

## 4. CRITICAL: Abstract Claims Contradicted by Actual Results

| Abstract Claim | Actual Result |
|---|---|
| *"mAP@0.5 of **83%** for component detection"* | The 61-class YOLOv7 achieves 83%, **but the retrained 15-class YOLOv7 achieves 95.62%**. The abstract reports the outdated, inferior result. |
| *"**expects** character accuracy of **75%** for text recognition"* | The custom CRNN actually achieved **65.96%**, and the fine-tuned TrOCR achieved **84.5%**. But the abstract says "expects 75%", which is neither the actual result nor the target—it's a speculative number from an earlier project stage. |
| *"deep learning models such as **YOLOv7** for component detection, **custom OCR** for text recognition"* | The results chapter explicitly concludes that **TrOCR is adopted as the final OCR model**, not the custom CRNN. |
| *"proper wire and node detection, for horizontal and vertical wires"* | No quantitative wire detection accuracy is provided anywhere in the report. This claim is unsubstantiated. |

**Verdict:** The abstract was written for an earlier report stage (progress/proposal) and was never updated to reflect the actual achieved results. It understates detection performance by 12+ percentage points and references the wrong OCR model as the primary one.

---

## 5. MAJOR: `cDocumentType` Set to "PROGRESS REPORT" but Content is a Final Report

| Location | Value |
|---|---|
| `vars.tex` line 5 | `\cDocumentType{A MAJOR PROJECT PROGRESS REPORT}` |

**Verdict:** The document type is still set to "PROGRESS REPORT," but the report contains a "Remaining Tasks" chapter (not a "Conclusion" chapter), final results with voltage divider end-to-end demonstrations, and the requirements chapter's Time Feasibility says *"Phase A has been completed and Phase B is also nearly done."* If this is the final report, `cDocumentType` should be updated. The commented-out `% \input{src/chapters/conclusion}` in `main.tex` further suggests the conclusion was never written.

---

## 6. MAJOR: `cTitleShort` Does Not Match Project Title

| Location | Value |
|---|---|
| `vars.tex` line 7 | `\cTitleShort{IEEE report Template and Guidelines}` |
| Expected | Should be a short form of "CIRCUITRON: Circuit Recognition, Transformation, and Analysis" |

**Verdict:** This is a leftover from the template and would appear anywhere the class uses `\cTitleShort` (e.g., page headers). It says "IEEE report Template and Guidelines" instead of anything related to CIRCUITRON.

---

## 7. MAJOR: "YOLOv7 (retrained)" May Actually Be a YOLOv26 Run

The `args.yaml` file for the best-performing "YOLOv7 (retrained)" model at `yolocomparision/circuitron_yolov7new/args.yaml` contains:

```yaml
model: /teamspace/studios/this_studio/runs/detect/circuitron_yolov264/weights/last.pt
name: circuitron_yolov264
```

The model was loaded from **`circuitron_yolov264`** weights — a YOLOv26 training run. This could mean:
- (a) The "retrained YOLOv7" was actually initialized from YOLOv26 weights (transfer learning), which is not stated anywhere in the report.
- (b) The naming is confusing and this is genuinely a different architecture than what's claimed.

**Verdict:** This needs clarification. If the best model is actually built on YOLOv26 architecture/weights, all claims about "YOLOv7 outperforming other architectures" become misleading. The entire comparative analysis narrative may be based on a misidentified model.

---

## 8. MAJOR: Content Duplicated Across Two Chapters

The following sections are **copy-pasted verbatim** between `systemArchitectureAndMethodology.tex` and `implementationDetails.tex`:

1. **Image Augmentation** subsection (word-for-word identical)
2. **Fine-tuning YOLOv5 and YOLOv7** subsection (identical training parameters list)
3. **Implementation of Text Recognition (OCR)** subsection (identical text)
4. **Line Detection Algorithm Implementation** subsection (identical algorithms and text)

Including the Wire Classification algorithm, Collinear Segment Merging algorithm, and Wire-Component Intersection Detection algorithm — all appear twice with identical content but **different LaTeX labels** (e.g., `\label{algo:wire-classification}` vs. `\label{algo:wire-classification-impl}`).

**Verdict:** This constitutes significant content duplication. An evaluator would notice the same text appearing in two different chapters. These should either be differentiated (methodology vs. implementation) or consolidated into one chapter.

---

## 9. MAJOR: TrOCR Contradicts "Fine-tuning Didn't Work" Claim

| Location | Claim |
|---|---|
| `implementationDetails.tex` line 170 | *"Initially, simply fine-tuning OCR models like **TrOCR** and EasyOCR were also attempted; however, **these didn't yield usable results**, ultimately requiring training from scratch."* |
| `systemArchitectureAndMethodology.tex` line 697 | Same statement |
| `implementationDetails.tex` line 179–192 | New subsection: "Fine-tuning TrOCR for Text Recognition" — achieves **84.5% accuracy** and is **adopted as the final OCR model** |
| `resultAndAnalysis.tex` line 458 | *"TrOCR the superior choice for this pipeline, and it is **adopted as the final OCR model** in the production system"* |

**Verdict:** The report first says TrOCR fine-tuning "didn't yield usable results," then later describes successful TrOCR fine-tuning that vastly outperforms the from-scratch model. The earlier statement was presumably true at one point but was never updated after the successful TrOCR fine-tuning was performed.

---

## 10. MAJOR: YOLOv7 Batch Size Contradiction

| Location | Claim |
|---|---|
| `implementationDetails.tex` line 160 | *"Batch size: 16 (for YOLOv5), **32 (for YOLOv7)**"* (61-class) |
| `implementationDetails.tex` line 195 | *"YOLOv7 (retrained): 100 epochs, batch size **16**"* (15-class) |
| `systemArchitectureAndMethodology.tex` line 687 | *"Batch size: 16 (for YOLOv5), **32 (for YOLOv7)**"* |
| Actual `args.yaml` | `batch: 16` for the retrained YOLOv7 |

**Verdict:** The original 61-class YOLOv7 is claimed to have used batch size 32, but the retrained 15-class YOLOv7 used batch size 16 (confirmed by args.yaml). This discrepancy is not acknowledged. Furthermore, the original 61-class YOLOv7's batch size of 32 cannot be verified from any config file in the workspace.

---

## 11. MAJOR: Image Size Discrepancy — 416×416 vs 640×640

| Location | Claim |
|---|---|
| `implementationDetails.tex` line 159 | Original YOLOv5/v7 (61-class): **416 × 416** pixels |
| `implementationDetails.tex` line 195 | Retrained YOLOv7 (15-class): **640 × 640** pixels |
| Actual `args.yaml` | `imgsz: 640` for all 15-class models |

**Verdict:** The 61-class models used 416×416, while the 15-class models used 640×640. This is a significant methodological difference that is **never acknowledged** in the comparative analysis. When comparing 61-class vs. 15-class YOLOv7 (Table: class-impact), the improvement is attributed entirely to class consolidation, but part of the improvement may be due to the **larger input resolution** (640 vs. 416). This makes the "Impact of Class Taxonomy Consolidation" analysis misleading.

---

## 12. MAJOR: Conclusion Chapter is a Template, Not Content

`conclusion.tex` contains only writing guidelines and commented-out template sections:
```latex
%  WRITING GUIDELINES FOR CONCLUSION CHAPTER
%  ==========================================
```
No actual conclusion content exists. It is also commented out in `main.tex`:
```latex
% \input{src/chapters/conclusion}
```

**Verdict:** The report has no conclusion. For a progress report, this might be acceptable (the "Remaining Tasks" chapter serves a similar purpose), but it contradicts having final results and a complete end-to-end pipeline demonstration.

---

## 13. MINOR: Chart.js Claimed but Not Used

| Report Claim | Reality |
|---|---|
| `implementationDetails.tex` line 460: *"The frontend system has been realized using React.js, **Chart.js**"* | `package.json` has **no Chart.js dependency** |
| `systemArchitectureAndMethodology.tex` line 200: *"**Chart.js** is to be used to map each component in JSON to a visual block"* | Chart.js is a charting library — it doesn't render circuit schematics |

**Verdict:** Chart.js appears to never have been installed or used. The claim that it was "realized using Chart.js" is likely false. The rendering may use Canvas/SVG directly or another approach entirely.

---

## 14. MINOR: "Remaining Tasks" Lists Items That Are Already Done

| Remaining Task Listed | Actual Status |
|---|---|
| "API and Frontend Integration" | The frontend is demonstrably working with the backend (voltage divider end-to-end demo shows full pipeline integration) |
| "System Refinement" | Comparative analysis with 4 new YOLO architectures and TrOCR fine-tuning show significant refinement already done |

**Verdict:** Some "remaining tasks" appear to have been partially or fully completed but the remaining tasks chapter was not updated.

---

## 15. MINOR: Undefined Glossary Entries

The following `\gls{}` references are used in the document but have **no corresponding `\newacronym` definition** in `abbreviations.tex`:

- `\gls{circuitron}` — used across multiple chapters
- `\gls{restful}` — used in implementationDetails.tex
- `\gls{python}` — used in requirements.tex
- `\gls{easyocr}` — used in resultAndAnalysis.tex
- `\gls{ltspice}` — used in intro.tex and literatureReview.tex
- `\gls{ngspice}` — used in requirements.tex
- `\gls{pyspice}` — used in implementationDetails.tex
- `\gls{uk}` — used in literatureReview.tex

These produce "??" or warnings in the compiled PDF.

---

## 16. MINOR: Requirements Chapter Uses Future Tense for Completed Work

The requirements chapter (`requirements.tex`) extensively uses phrases like:
- *"will serve as"*, *"is expected to"*, *"will be used"*, *"has not kicked into gear as of yet"*

These were written during the proposal/progress stage but are now contradicted by the working system demonstrated in the results chapter.

---

## 17. MINOR: Patience Parameter Inconsistency for YOLOv26

| Location | Claim |
|---|---|
| `implementationDetails.tex` line 198 | *"YOLOv26: 100 epochs, batch size 16, patience = 20"* — patience listed only for YOLOv26 |
| Actual `args.yaml` | **All** four 15-class models had `patience: 20` |

**Verdict:** The report implies only YOLOv26 used early stopping patience, but all models were configured identically with patience=20. This could mislead readers into thinking different stopping criteria were used.

---

## 18. NOTE: PySpice and MongoDB Not in Requirements.txt

The report discusses:
- PySpice integration for circuit simulation
- MongoDB for database needs

Neither `PySpice` nor `pymongo`/`mongodb` appears in `Webapp/requirements.txt`. Either these were installed but not captured in requirements, or they haven't been integrated yet.

---

## 19. NOTE: Date in vars.tex is "February 2026" — Current Date is March 2026

`vars.tex` line ~48: `\cDate{February 2026}` and `\cDateFull{February 15, 2026}`

If the submission date has passed or changed, these should be updated.

---

## SUMMARY

| Severity | Count | Description |
|---|---|---|
| **CRITICAL** | 4 | OCR epochs (29 vs 50), augmentation contradiction, training split (70/10/20 vs 70/20/10), outdated abstract |
| **MAJOR** | 8 | Wrong document type, template title, model identity question, content duplication, TrOCR contradiction, batch size, image size confound, no conclusion |
| **MINOR** | 5 | Chart.js not used, remaining tasks outdated, undefined glossary entries, future tense, patience inconsistency |
| **NOTE** | 2 | Missing dependencies, outdated date |
| **TOTAL** | **19 issues** | |

---

*This audit was performed by cross-referencing all LaTeX source files, actual training config YAML files, CSV result data, package.json/requirements.txt dependencies, and computational verification of all stated calculations and percentages.*
