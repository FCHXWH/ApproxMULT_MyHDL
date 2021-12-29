# Verilog Generator for Approximate Multiplier by MyHDL

Use Myhdl to generate approximate multipliers.

## Prerequisities

### Python >= 3.8 (use conda)

```bash
conda create --name=ApproxMult python=3.8
```

### Myhdl = 0.11 & Json 

```bash
conda activate ApproxMult
pip install Myhdl
```

## Usage

```bash
python ApproxMULT_MyHDL.py "CompressorTree_CEOA115.json" "ILP_ApproxMult" "error_output.txt" 8 1
```

