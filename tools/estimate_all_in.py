"""Estimate the all-in monthly cost of one unit type in one building."""

import statistics


def estimate_all_in(rents, sqfts, costs, assumptions):
    """Combine base rent, actual fees and labeled estimates.

    Args:
        rents: Base rents for the unit type, USD per month.
        sqfts: Unit sizes in square feet for the same unit type.
        costs: Cost rows for the building (dicts using costs.csv columns).
        assumptions: Dict of item -> value from cost_assumptions.csv.

    Returns:
        A dict with each component as (amount, basis), plus "total" and
        "share_estimated", the fraction of non-rent cost that is estimated.
    """
    monthly = [c for c in costs if c["frequency"] == "monthly"
               and str(c["counted"]).lower() == "true" and c["amount_usd"] not in ("", None)]
    text = " ".join(f"{c['item']} {c['notes']}".lower() for c in costs)
    parts = {"rent": (statistics.median(rents), "actual"),
             "fees": (sum(float(c["amount_usd"]) for c in monthly), "actual")}
    if not monthly and any(c["item"] == "required_fees_unpublished" for c in costs):
        parts["fees"] = (assumptions["required_fees"], "estimate")
    if "electric" not in " ".join(c["item"] for c in monthly):
        kwh = assumptions["electricity_use"] * statistics.median(sqfts)
        parts["electricity"] = (kwh * assumptions["electricity_rate"], "estimate")
    if "water" not in " ".join(c["item"] for c in monthly) and "water included" not in text:
        parts["water_sewer"] = (assumptions["water_sewer"], "estimate")
    if not any(k in text for k in ("technology", "bulk internet", "internet included")):
        parts["internet"] = (assumptions["internet"], "estimate")
    parts["renters_insurance"] = (assumptions["renters_insurance"], "estimate")
    extra = sum(v for k, (v, _) in parts.items() if k != "rent")
    estimated = sum(v for _, (v, b) in parts.items() if b == "estimate")
    parts["total"] = (sum(v for v, _ in parts.values()), "mixed")
    parts["share_estimated"] = (estimated / extra if extra else 0.0, "ratio")
    return parts
