import subprocess
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """
    Run a shell command using subprocess.run.
    
    Parameters
    cmd: list
        The command to run, provided as a list of arguments.
    cmd: str or Path, optional
        Working directory where the command wiill be executed.
    """

    print(f"[RUN] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=True)
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
    
def run_pipeline_from_fastq(
    fastq1,
    outdir,
    sample_id="sample",
    threads=2,
):
    """
    Minimal pipeline starting from FASTQ.
    
    Currently runs only FastQC on the input FASTQ file.
    Additional steps (trimming, aligment, variant calling, ACMG classification)
    will be added later.
    

    Args:
        fastq1 (_type_): _description_
        outdir (_type_): _description_
        sample_id (str, optional): _description_. Defaults to "sample".
        threads (int, optional): _description_. Defaults to 2.
    """
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    qc_dir = outdir / "fastqc"
    run_fastqc(fastq1, qc_dir, threads=threads)
    
if __name__ == "__main__":
    run_pipeline_from_fastq(
        fastq1="data/test_R1.fastq",
        outdir="results/test",
        sample_id="test",
        threads=2,
    )