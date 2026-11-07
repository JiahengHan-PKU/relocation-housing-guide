"""Give rental rules from different research files one shape."""

KEYS = {
    "min_lease": ("min_lease_months", "min_lease_term", "minimum_lease"),
    "leases_per_year": ("leases_per_year",),
    "approval": ("association_approval",),
    "approval_time": ("approval_time",),
    "application_fee": ("association_application_fee_usd", "association_application_fee"),
    "deposit": ("security_deposit",),
    "pets": ("pet_policy", "pets"),
    "income": ("income_or_credit_requirements", "income_credit", "income_or_credit"),
    "short_term": ("short_term_rentals",),
}


def normalize_rules(rules):
    """Map a raw rules object to fixed keys holding {value, source_url}.

    Args:
        rules: The `rules` dict from a raw building JSON, or None.

    Returns:
        A dict with every key in KEYS; missing values are None.
    """
    rules = rules or {}
    shared_sources = rules.get("sources") or []
    out = {}
    for key, names in KEYS.items():
        raw = next((rules[n] for n in names if n in rules), None)
        if isinstance(raw, dict):
            value = raw.get("value")
            source = raw.get("source_url") or (shared_sources[0] if shared_sources else None)
        else:
            value, source = raw, (shared_sources[0] if shared_sources else None)
        out[key] = {"value": value, "source_url": source} if value not in (None, "", []) else None
    return out
