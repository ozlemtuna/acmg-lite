from typing import List
from .models import Variant

def rule_ba1(variant: Variant) -> bool:
    if variant.gnomad_af is None:
        return False
    return variant.gnomad_af >= 0.05

def explain_ba1(variant: Variant) -> str:
    if variant.gnomad_af is None:
        return "BA1 not satisfied: frequency missing."

    if rule_ba1(variant):
        return (
            f"BA1: gnomAD AF={variant.gnomad_af} is >= 0.05 "
            f"(too common to cause a rare Mendelian disorder)."
        )

    return f"BA1 not satisfied: gnomAD AF={variant.gnomad_af} is < 0.05."
    
def rule_pm2(variant: Variant) -> bool:
    if variant.gnomad_af is None:
        return True
    return variant.gnomad_af < 0.0001


def explain_pm2(variant: Variant) -> str:
    

    if variant.gnomad_af is None:
        return "PM2: gnomAD AF is missing (possible absence from controls)."

    if rule_pm2(variant):
        return (
            f"PM2: gnomAD AF={variant.gnomad_af} is < 0.0001 "
            f"(extremely rare or absent in population databases)."
        )

    return (
        f"PM2 not satisfied: gnomAD AF={variant.gnomad_af} is >= 0.0001 "
        f"(not extremely rare)."
    )
def classify_variant_simple(variant: Variant) -> tuple[str, List[str]]:
    evidence: List[str] = []
    
    if rule_ba1(variant):
        evidence.append("BA1")
        classification = "Benign"
    elif rule_pm2(variant):
        evidence.append("PM2")
        classification = "Likely pathogenic"
    else:
        classification = "VUS"
        
    return classification, evidence