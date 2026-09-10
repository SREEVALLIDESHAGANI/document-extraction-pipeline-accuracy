"""
Pipeline Orchestrator & Accuracy Evaluator for Assignment 5
Simulates extraction with quality pre-checks, schema enforcement, confidence scoring,
and human-in-the-loop routing.
"""
import json
import random

def run_pipeline():
    with open("ground_truth_100.json", "r", encoding="utf-8") as f:
        docs = json.load(f)

    # Threshold parameters derived from calibration
    ACCEPT_CONF_THRESHOLD = 0.88
    REJECT_QUALITY_DPI = 120
    REJECT_BLUR_THRESHOLD = 0.60

    results = []
    field_stats = {}

    routed_counts = {"AUTO_ACCEPT": 0, "HUMAN_REVIEW": 0, "REJECT": 0}

    for doc in docs:
        doc_id = doc["doc_id"]
        gt = doc["ground_truth"]
        deg = doc["degradation_profile"]
        dpi = doc["dpi"]
        blur = doc["blur_score"]

        # Step 1: Quality Gate / Rejection Path
        if dpi < REJECT_QUALITY_DPI or blur > REJECT_BLUR_THRESHOLD:
            routed_counts["REJECT"] += 1
            results.append({
                "doc_id": doc_id,
                "status": "REJECTED",
                "reason": f"DPI {dpi} < 120 or Blur {blur} > 0.60",
                "extracted": None,
                "confidence": 0.40
            })
            continue

        # Step 2: Extraction Simulation (Vision LLM / Document AI)
        extracted = {}
        confidences = []

        for field, gt_val in gt.items():
            if field not in field_stats:
                field_stats[field] = {"total": 0, "exact_match": 0, "conf_sum": 0.0}

            field_stats[field]["total"] += 1

            # Determine accuracy based on degradation
            if deg == "CLEAN_DIGITAL":
                acc_prob = 0.98 if field != "line_items_count" else 0.85
                field_conf = random.uniform(0.92, 0.99)
            elif deg == "SKEWED_MOBILE_SCAN":
                acc_prob = 0.88 if field != "line_items_count" else 0.65
                field_conf = random.uniform(0.82, 0.91)
            elif deg == "HANDWRITTEN_ANNOTATIONS":
                acc_prob = 0.76 if field != "line_items_count" else 0.50
                field_conf = random.uniform(0.74, 0.87)
            else:
                acc_prob = 0.45
                field_conf = random.uniform(0.50, 0.70)

            is_correct = random.random() < acc_prob
            if is_correct:
                extracted[field] = gt_val
                field_stats[field]["exact_match"] += 1
            else:
                # Corrupted field extraction
                if isinstance(gt_val, (int, float)):
                    extracted[field] = round(gt_val * random.uniform(0.85, 1.15), 2)
                else:
                    extracted[field] = str(gt_val)[:-1] + "?"

            field_stats[field]["conf_sum"] += field_conf
            confidences.append(field_conf)

        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        # Step 3: Confidence Routing Policy
        if avg_conf >= ACCEPT_CONF_THRESHOLD:
            route = "AUTO_ACCEPT"
            routed_counts["AUTO_ACCEPT"] += 1
        else:
            route = "HUMAN_REVIEW"
            routed_counts["HUMAN_REVIEW"] += 1

        results.append({
            "doc_id": doc_id,
            "status": route,
            "confidence": round(avg_conf, 3),
            "extracted": extracted
        })

    # Compile field accuracy report
    field_report = {}
    for field, data in field_stats.items():
        total = data["total"]
        if total > 0:
            acc = round((data["exact_match"] / total) * 100, 1)
            mean_conf = round(data["conf_sum"] / total, 3)
            field_report[field] = {
                "evaluated_samples": total,
                "exact_match_accuracy_pct": acc,
                "mean_confidence": mean_conf,
                "calibration_gap": round(mean_conf - (acc / 100.0), 3)
            }

    with open("pipeline_evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump({
            "routing_summary": routed_counts,
            "field_level_accuracy": field_report
        }, f, indent=2)

    print("Pipeline evaluation completed. Summary:")
    print(f"  Auto-Accept: {routed_counts['AUTO_ACCEPT']} docs")
    print(f"  Human Review: {routed_counts['HUMAN_REVIEW']} docs")
    print(f"  Rejected: {routed_counts['REJECT']} docs")

if __name__ == "__main__":
    run_pipeline()
