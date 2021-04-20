# code-similarity-parser
A source code similarity parser writen in Python, which can extract common headers and function calls.

## Usage
```bash
# To get function calls of a c source file
python getFunc.py /path/to/source

# To parse the code similarity of P1, P2 and Library(Which P1, P2 may all import)
python similarityParser.py /path/to/P1 /path/to/P2 [/path/to/Library]
```