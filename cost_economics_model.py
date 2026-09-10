"""
Cost Economics & ROI Model for Document Processing Pipeline
Calculates per-document costs and monthly enterprise savings.
"""

def compute_economics(monthly_volume=100000, human_hourly_rate=18.0, manual_min_per_doc=3.5):
    # Manual Cost
    manual_cost_per_doc = (manual_min_per_doc / 60.0) * human_hourly_rate # $1.05
    monthly_manual_total = monthly_volume * manual_cost_per_doc

    # Hybrid AI Model Parameters
    ai_inference_cost_per_doc = 0.02   # Vision token API call
    infra_cost_per_doc = 0.005         # Storage, database, compute
    ai_base_cost = ai_inference_cost_per_doc + infra_cost_per_doc

    # Human Review Queue Parameters
    human_review_min_per_doc = 0.75    # 45 seconds to verify pre-extracted bounding boxes
    review_cost_per_doc = (human_review_min_per_doc / 60.0) * human_hourly_rate # $0.225
    reject_handling_cost = 0.05        # Automated customer notification + manual exception check

    # Distribution based on 100-doc empirical benchmark
    pct_auto_accept = 0.74
    pct_human_review = 0.20
    pct_rejected = 0.06

    hybrid_cost_per_doc = (
        ai_base_cost + 
        (pct_human_review * review_cost_per_doc) + 
        (pct_rejected * reject_handling_cost)
    )

    monthly_hybrid_total = monthly_volume * hybrid_cost_per_doc
    monthly_savings = monthly_manual_total - monthly_hybrid_total
    savings_pct = (monthly_savings / monthly_manual_total) * 100.0

    print("=== ASSIGNMENT 5 DOCUMENT ECONOMICS MODEL ===")
    print(f"Monthly Processing Volume: {monthly_volume:,} documents")
    print(f"Manual Entry Cost: ${manual_cost_per_doc:.3f} / doc | Monthly: ${monthly_manual_total:,.2f}")
    print(f"Hybrid AI Cost:   ${hybrid_cost_per_doc:.3f} / doc | Monthly: ${monthly_hybrid_total:,.2f}")
    print(f"Monthly Operational Savings: ${monthly_savings:,.2f} ({savings_pct:.1f}% reduction)")

if __name__ == "__main__":
    compute_economics()
