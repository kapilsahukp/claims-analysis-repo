# Claims Analysis

## Overview

Using NLP to flag possible violations in claims. 

## Setup

Install conda environment

```
conda env create -f environment.yml
```

Make environment available as Jupyter kernel

```
python -m ipykernel install --user --name claims-analysis --display-name claims-analysis
```

Run linters

```
make lint
```