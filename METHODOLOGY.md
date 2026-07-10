# Methodology: Polymorphic Residue Analysis (RAPSF)

The Z13 cipher is analyzed not as a static linear string, but as a **Polymorphic Cryptographic Function**. This repository employs the **RAPSF (Residue-Analysis & Polymorphic Stream Filter)** runtime environment.

## 1. Architectural Logic
The cipher is ingested as a 13-byte packed payload with static structural anchors.
- **Static Anchors**: The '+' symbols at Index[3] and Index[10] are processed as **Jump Instructions (JMP)**, effectively partitioning the data stream into asynchronous memory tracks.
- **Twin-Track Processing**: The system executes two concurrent memory loops (Track Alpha and Track Beta), allowing for the identification of variable strings mapping to suspect-specific matrices.

## 2. Execution Engine
The engine utilizes low-level execution primitives:
- **C-Level Translation**: The system uses `str.maketrans` for high-throughput permutation testing, bypassing standard overhead.
- **Bitmask Filtering**: Suspect profiles are converted into static frequency tables (via `collections.Counter`), enabling real-time intersection checks against generated anagrams.
- **Low-Entropy Analysis**: By applying a score-threshold (>= 8 matches), the system collapses the memory state into meaningful identifiers, filtering out stochastic noise.

## 3. Polymorphism & Transposition
The engine evaluates three distinct memory layouts (transposition layers) via `apply_transposition()`. This accounts for potential encoding variations—such as reverse-stream or interleaved sequences—often utilized in naval/radio-frequency multiplexing protocols.
