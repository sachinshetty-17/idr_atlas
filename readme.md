# IDR Atlas V1 (prototype)

IDR Atlas is a web-based project to explore intrinsically disordered regions (IDRs)
in reviewed human proteins using sequence-derived biophysical parameters.

## What is done so far
- Extracted IDRs from reviewed human proteins from uniprot 
- Computed basic parameters (start,end,sequence,length,f +/-,FCR,NCPR,kappa,hydropathy,aromatic density,pro fraction,gly fraction, full sequence)
- User can search using (idr_id, accession, gene name) 
- Can select card or table format 
- Built a fastapi backend
- Created a basic frontend to search IDRs

## what is planned next
- Better UI and validation using known software

### Per-IDR visualizations
- IDR length context (histogram + violin + boxplot)
- Hydropathy profile (Kyte–Doolittle sliding window)
- Mean hydropathy vs mean net charge
- FCR vs NCPR phase diagram
- Positive vs negative charge composition (2D density / hexbin)
- κ (charge patterning) vs FCR
- Proline vs glycine composition
- Correlation heatmap of IDR parameters

### Dataset-level visualizations
- Global IDR length distribution
- IDR chemical space mapping (PCA/UMAP, planned)

## Interactive Sequence Analysis (Planned)

### Sequence Mutation Explorer
Allows users to introduce point mutations or small edits into existing IDR sequences and observe changes in parameters.

Parameters compared:
- Length
- FCR, NCPR
- Charge patterning (κ)
- hydropathy
- Proline and glycine fractions
- Aromatic residue density

### Amino Acid Builder (Sequence Growth Simulator)
An interactive tool to construct IDR sequences residue-by-residue and observe the evolution of parameters as the sequence grows.

Tracked outputs:
- Parameter trajectories (FCR, κ, hydropathy, composition)
- Emergence of disorder-related features
- Comparison with natural idr
- experimental validation 

