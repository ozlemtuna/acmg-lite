import sys
import os

# Add project root (one level above 'scripts') to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from acmg_lite.vcf_parser import parse_vcf
from acmg_lite.acmg_rules import (classify_variant_simple, explain_ba1, explain_pm2)

if __name__ == "__main__":
    variants = parse_vcf("data/test_acmg.vcf")
    print(f"Parsed {len(variants)} variants from test_acmg.vcf\n")
    
    for v in variants:
        classification, evidence = classify_variant_simple(v)
        print(f"Variant: {v}")
        print(f"  Classification: {classification}")
        print(f"  Evidence: {', '.join(evidence) if evidence else 'None'}")
        print(f"  BA1 explanation: {explain_ba1(v)}")
        print(f"  PM2 explanation: {explain_pm2(v)}")

        print()
        