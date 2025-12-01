from pathlib import Path
from typing import List

from .models import Variant

def parse_info_field(info_str: str) -> dict:
    info_dict = {}
    if info_str == "." or not info_str:
        return info_dict
    
    for item in info_str.split(";"):
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            key,value = item.split("=", 1)
            info_dict[key.strip()] = value.strip()
        else:
            info_dict[item] = True
    return info_dict
    
    
def parse_vcf(path: str | Path) -> List[Variant]:
    path = Path(path)
    variants: List[Variant] = []
    
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            fields = line.split()
            if len(fields) < 8:
                continue
            
            chrom, pos, _id, ref, alt, _qual, _filter, info = fields[:8] 
            
            info_dict = parse_info_field(info)
            
            gene = info_dict.get("GENE") or info_dict.get("Gene") or info_dict.get("gene")
            info_upper = {k.upper(): v for k, v in info_dict.items()}
            
            af_raw = info_upper.get("GNOMAD_AF") or info_upper.get("AF")
            
            if af_raw is None:
                for k, v in info_dict.items():
                    ku = k.upper()
                    if "GNOMAD_AF" in ku or ku == "AF":
                        af_raw = v
                        break
            try: 
                gnomad_af = float(af_raw) if af_raw is not None else None
            except ValueError:
                gnomad_af = None

            
            variant = Variant(
                chrom = chrom,
                pos = int(pos),
                ref = ref,
                alt = alt,
                gene = gene, 
                gnomad_af = gnomad_af,
            )
            variants.append(variant)
            
        return variants   