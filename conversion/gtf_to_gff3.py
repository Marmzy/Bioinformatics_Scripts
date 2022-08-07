#!/usr/bin/env python

import pandas as pd
import re

from datetime import datetime


def search(
    attr: str,
    entry: str
) -> str:
    """Checks if an attribute is present for a given .gtf entry

    Args:
        attr (str): .gtf attribute
        entry (str): .gtf attributes entry

    Returns:
        str: Attribute=value concatenation
    """

    #Check if attribute is present for given entry, and if it is, return it's value
    if re.search(f'{attr} "', entry):
        return "{}={}".format(attr, re.findall(rf"(?<={attr} \")[^\"]+", entry)[0])


def gtf_to_gff3(
    input: str,
    output: str
) -> None:
    """Convert .gtf file to .gff3 file (modeled after R's rtracklayer)

    Args:
        input (str): Input .bed file path
        output (str): Output .gff3 file path
    """

    #Initialising variables
    gtf_attributes = ["gene_id", "db_xref", "gbkey", "gene", "gene_biotype", "transcript_id",
                      "model_evidence", "product", "exon_number", "protein_id", "anticodon",
                      "inference", "note", "exception", "transl_except", "pseudo", "partial"]

    #Reading the .gtf file as a dataframe
    df = pd.read_csv(input, sep="\t", header=None, comment='#')
    df.iloc[:, 8] = [";".join([a for a in [search(attr, annot) for attr in gtf_attributes] if a is not None]) for annot in df.iloc[:, 8].values]

    #Outputting the gff3 dataframe
    with open(output, "w") as f_out:
        f_out.write("##gff-version 3\n")
        f_out.write("##source-version gtf_to_gff3.py\n")
        f_out.write(f"##date {datetime.today().strftime('%Y-%m-%d')}\n")
        df.to_csv(f_out, sep="\t", header=False, index=False, mode="a")