import subprocess
from pathlib import Path

def run_cmd(cmd, cwd=None, stdout=None):
    """
    Run a shell command using subprocess.run.
    
    Parameters
    cmd: list
        The command to run, provided as a list of arguments.
    cmd: str or Path, optional
        Working directory where the command wiill be executed.
    stdout: file-like object, optional
        If provided, the command's stdout will be redireceted to this file.
    """

    print(f"[RUN] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=True, stdout=stdout)
    return result

def run_fastqc(single_fastq, outdir, threads=2):
    """
    Run FastQC on a single FASTQ file.
    
    Parameters
    ----------
    single_fastq : str or Path
        Path to the input FASTQ file.
    outdir : str or Path
        Directory where FastQC output will be saved.
    threads : int, optional
        Number of threads to use.
    """
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    run_cmd([
        "fastqc",
        "-t", str(threads),
        "-o", str(outdir),
        str(single_fastq)
    ])        
    
def run_bwa_mem(reference_fasta, fastq1, outdir, sample_id, threads=2):
    """
    Run BWA-MEM aligment on a single-end FASTQ file.
    """
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    sam_path = outdir / f"{sample_id}.sam"
    
    with sam_path.open("w") as sam_file:
        run_cmd(
            [
                "bwa", "mem",
                "-T", "0",
                "-t", str(threads),
                str(reference_fasta),
                str(fastq1),
            ],
            stdout=sam_file,
        )
    return sam_path

def run_samtools_sort_index(sam_path, outdir, sample_id, threads=2):
    """
    Convert SAM to sorted BAM create an index.
    """
    outdir= Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    sam_path = Path(sam_path)
    unsorted_bam = outdir / f"{sample_id}.unsorted.bam"
    sorted_bam = outdir / f"{sample_id}.sorted.bam"
    
    # SAM -> unsorted BAM
    run_cmd([
        "samtools", "view",
        "-b",
        "-@", str(threads),
        "-o", str(unsorted_bam),
        str(sam_path),
    ]) 
    
    # unsorted BAM -> sorted BAM
    run_cmd([
        "samtools", "view",
        "-b",
        "-@", str(threads),
        "-o", str(sorted_bam),
        str(unsorted_bam),
    ])
    
    run_cmd([
        "samtools", "index",
        str(sorted_bam),
    ])
    
    return sorted_bam


def run_bcftools_call(sorted_bam, reference_fasta, outdir, sample_id):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    vcf_out = outdir / f"{sample_id}.vcf"
    
    mpileup_cmd = [
        "bcftools", "mpileup",
        "-f", str(reference_fasta),
        str(sorted_bam),
    ]
    
    call_cmd = [
        "bcftools", "call",
        "-mv",
        "-Ov",
        "-o", str(vcf_out),
    ]
    
    print(f"[RUN] {' '.join(mpileup_cmd)} | {' '.join(call_cmd)}")
    
    p1 = subprocess.Popen(mpileup_cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(call_cmd, stdin=p1.stdout)
    p1.stdout.close()
    p2_returncode = p2.wait()
    p1_returncode = p1.wait()
    
    if p1_returncode != 0 or p2_returncode != 0:
        raise RuntimeError("Error in bcftools mpileup or call")
    return vcf_out

def run_pipeline_from_fastq(
    fastq1,
    outdir,
    sample_id="sample",
    threads=2,
    reference_fasta ="data/test_ref.fa",
):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    qc_dir = outdir / "fastqc"
    run_fastqc(fastq1, qc_dir, threads=threads)
    
    align_dir = outdir / "aligment"
    sam_path = run_bwa_mem(reference_fasta, fastq1, align_dir, sample_id, threads=threads)
    
    bam_path = run_samtools_sort_index(sam_path, align_dir, sample_id, threads=threads)
    
    vcf_dir = outdir / "vcf"
    vcf_path = run_bcftools_call(bam_path, reference_fasta, vcf_dir, sample_id)
    
    print(f"[DONE] VCF file generated at: {vcf_path}")
    return vcf_path
    
if __name__ == "__main__":
    
    vcf_out = run_pipeline_from_fastq(
        fastq1="data/test_R1.fastq",
        outdir="results/test",
        sample_id="test",
        threads=2,
        reference_fasta="data/test_ref.fa",
    )
    print(f"[DONE] Final VCF: {vcf_out}")
    