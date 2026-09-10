# Assignment 5: Document Extraction Pipeline with Accuracy Measurement

**Student Name:** Deshagani Sreevalli  
**Roll Number:** 23EG107F63  
**Institution:** Anurag University  
**Email:** 23eg107f63@anurag.edu.in  
**Status:** Completed and verified  

---

## Overview
A production document extraction architecture for BFSI back-office operations enforcing field-level accuracy, confidence calibration, automated optical quality gates, and human-in-the-loop exception routing.

## Deliverables
- Assignment_5_Solution.pdf: Executive 3-page visual report with calibration gap chart and routing economics.
- schemas.py: Pydantic v2 schemas with arithmetic validation and regex checks for Invoices, Claims, and IDs.
- ground_truth_100.json: 100-document dataset with verified ground truth and quality degradation attributes.
- pipeline_orchestrator.py: End-to-end extraction and routing simulation engine.
- pipeline_evaluation_report.json: Field-level accuracy and calibration report.
- cost_economics_model.py: Financial model comparing manual entry (.050) vs hybrid AI (.073 / 93% savings).

## How to Run
`ash
python pipeline_orchestrator.py
python cost_economics_model.py
`
