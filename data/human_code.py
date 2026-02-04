import re

input_fasta = "data/UP000005640_9606.fasta"
output_tsv = "data/uniprot_human.tsv"

with open(input_fasta) as f, open(output_tsv, "w") as out:
    out.write("accession\tgene_name\torganism\tlength\tsequence\n")

    accession = gene = organism = None
    seq = []

    for line in f:
        line = line.strip()

        if line.startswith(">"):
            if accession:
                sequence = "".join(seq)
                out.write(
                    f"{accession}\t{gene}\t{organism}\t{len(sequence)}\t{sequence}\n"
                )

            header = line

            # accession
            parts = header.split("|")
            accession = parts[1] if len(parts) > 1 else "NA"

            # gene name
            g = re.search(r"GN=([^\s]+)", header)
            gene = g.group(1) if g else "NA"

            # organism
            o = re.search(r"OS=([^=]+?) OX=", header)
            organism = o.group(1) if o else "NA"

            seq = []

        else:
            seq.append(line)

    # write last protein
    if accession:
        sequence = "".join(seq)
        out.write(
            f"{accession}\t{gene}\t{organism}\t{len(sequence)}\t{sequence}\n"
        )

print("Done. Data saved to data/uniprot_human.tsv")
