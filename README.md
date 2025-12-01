# ACMG-Lite

ACMG-Lite is a minimal, educational variant interpretation pipeline that demonstrates the core logic of an ACMG-like workflow:

**FASTQ → Alignment → Variant Calling → VCF Parsing → ACMG Classification**

This lightweight project is ideal for learning, teaching, and building custom genomics annotation pipelines.

---

##  Features

### 1) FASTQ → BAM → VCF Pipeline  
Implemented in `acmg_lite/pipeline_fastq.py` using:
- FastQC
- BWA-MEM
- Samtools (sort + index)
- Bcftools (mpileup + call)

Example outputs:
```
results/test/alignment/test.sorted.bam
results/test/vcf/test.vcf
```

---

## 2) Variant Dataclass  

Defined in `acmg_lite/models.py`:

```python
@dataclass
class Variant:
    chrom: str
    pos: int
    ref: str
    alt: str
    gene: Optional[str] = None
    gnomad_af: Optional[float] = None
```

---

## 3) VCF Parser  

`acmg_lite/vcf_parser.py` extracts:

- CHROM, POS, REF, ALT  
- GENE fields (`GENE=`)  
- Allele frequency (`GNOMAD_AF` or `AF`)  

Usage example:

```python
from acmg_lite.vcf_parser import parse_vcf
variants = parse_vcf("data/test_acmg.vcf")
```

---

## 4) Minimal ACMG Rules  
Rules implemented:

- **BA1** → Benign if AF ≥ 0.05  
- **PM2** → Likely pathogenic if AF < 0.0001  

Classification logic:

```python
if BA1:
    Benign
elif PM2:
    Likely pathogenic
else:
    VUS
```

---

## 5) End-to-End ACMG Demonstration  

Run:

```bash
python scripts/test_acmg_from_vcf.py
```

Example output:

```
Variant: chr1:1000 A>G (gene=GENE1, af=0.1)
  Classification: Benign

Variant: chr1:2000 C>T (gene=GENE2, af=0.0001)
  Classification: VUS
```

---

## 🔧 Installation  

```bash
git clone https://github.com/ozlemtuna/acmg-lite.git
cd acmg-lite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Install external tools (macOS)
```bash
brew install fastqc bwa samtools bcftools
```

---

## ▶ Running the Full Pipeline  

### 1) FASTQ → VCF
```bash
python -m acmg_lite.pipeline_fastq
```

### 2) ACMG classification
```bash
python scripts/test_acmg_from_vcf.py
```

---

##  Project Structure

```
acmg-lite/
├── acmg_lite/
│   ├── acmg_rules.py
│   ├── models.py
│   ├── pipeline_fastq.py
│   ├── vcf_parser.py
├── data/
│   ├── test_R1.fastq
│   ├── test_ref.fa
│   └── test_acmg.vcf
├── scripts/
│   ├── test_acmg_from_vcf.py
│   └── run_acmg.py (coming soon)
└── results/   (ignored in git)
```

---

##  Roadmap

- Add more ACMG rules (PP3, BP4, PVS1)  
- Add dbNSFP / VEP annotation support  
- Add HTML/TSV reporting  
- Add a CLI tool (`acmg-lite run`)  
- Support for paired-end FASTQ  
- Add unit tests  

---

##  Author

**Özlem Tuna**

---

##  License

MIT License
