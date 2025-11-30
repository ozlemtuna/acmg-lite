from dataclasses import dataclass
from typing import Optional

@dataclass
class Variant:
    chrom: str
    pos: int
    ref: str
    alt: str
    gene: Optional[str] = None
    consequence: Optional[str] = None
    gnomad_af: Optional[float] = None
    
    def __repr__(self):
        return (
            f"{self.chrom}:{self.pos} {self.ref}>{self.alt} "
            f"(gene={self.gene}, af={self.gnomad_af})"
        )  