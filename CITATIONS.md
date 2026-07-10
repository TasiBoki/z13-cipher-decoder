# Citations & Technical Context

This analysis acknowledges established cryptographic methods and investigation frameworks as the foundation for the RAPSF implementation.

## 1. Cryptographic Methodology
- **Frequency Analysis (Residue-Analysis)**: The engine relies on standard frequency distribution models modified for low-entropy datasets (n=13).[cite: 2]
- **Permutation Theory**: The system uses exhaustive permutation testing, as implemented by Python's `itertools.permutations`, to identify patterns within the limited Z13 alphabet.[cite: 2]

## 2. Investigation Frameworks
- **Suspect Matrices**: The bitmask datasets for Arthur Leigh Allen, Gary Francis Poste, and Lawrence Kane are derived from high-profile investigative files. The system allows for the integration of further matrices (e.g., Gaikowski, Sullivan) as provided by public records.[cite: 2]
- **Case Breakers/Oranchak Context**: While this tool operates independently, it is designed to complement existing automated testing environments (such as AZdecrypt) by providing an alternative, algorithm-driven look at the Z13 suspect profiles.[cite: 2]

## 3. Implementation Credits
- The source code (`kodolo.py`) utilizes optimized memory addressing and translation tables designed for maximum throughput during high-iteration hot loops.[cite: 2]
