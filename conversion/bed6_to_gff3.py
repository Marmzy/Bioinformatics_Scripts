#!/usr/bin/env python

import pandas as pd

from datetime import datetime


def bed6_to_gff3(
    input: str,
    output: str
) -> None:
    """Convert .bed file to .gff3 file (modeled after R's rtracklayer)

    Args:
        input (str): Input .bed file path
        output (str): Output .gff3 file path
    """

    #Reading the .bed file as a dataframe
    bed_df = pd.read_csv(input, sep="\t", header=None, comment='#')

    #Converting the .bed dataframe to a .gff3 dataframe
    gff_df = pd.DataFrame({
        "seqid": bed_df.iloc[:, 0],
        "source": ["."]*len(bed_df),
        "type": ["sequence_feature"]*len(bed_df),
        "start": bed_df.iloc[:, 1]+1,
        "end": bed_df.iloc[:, 2],
        "score": bed_df.iloc[:, 4],
        "strand": bed_df.iloc[:, 5],
        "phase": ["."]*len(bed_df),
        "attributes": "name="+bed_df.iloc[:, 3]
    })

    #Outputting the gff3 dataframe
    with open(output, "w") as f_out:
        f_out.write("##gff-version 3\n")
        f_out.write("##source-version bed6_to_gff3.py\n")
        f_out.write(f"##date {datetime.today().strftime('%Y-%m-%d')}\n")
        gff_df.to_csv(f_out, sep="\t", header=False, index=False, mode="a")