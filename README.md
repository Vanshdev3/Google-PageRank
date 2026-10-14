<div align="center">

<img src="final_cover.png" alt="GOOGLE PAGERANK" width="100%" style="border-radius: 12px; margin-bottom: 24px; box-shadow: 0 8px 30px rgba(0,0,0,0.5);" />

# GOOGLE PAGERANK
### *Mathematical Formulation, Markov Chains & Real-Time Graph Simulation*

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](pagerank_demo.py)
[![NumPy](https://img.shields.io/badge/NumPy-Linear%20Algebra-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![HTML5 / Canvas](https://img.shields.io/badge/Web%20Simulator-HTML5%20%7C%20Canvas%20%7C%20Vanilla%20JS-E34F26?style=for-the-badge&logo=html5&logoColor=white)](index.html)
[![Linear Algebra](https://img.shields.io/badge/Linear%20Algebra-Eigenvalues%20%26%20Eigenvectors-4285F4?style=for-the-badge)]()
[![Perron-Frobenius](https://img.shields.io/badge/Perron--Frobenius-λ%20%3D%201.0-34A853?style=for-the-badge)]()
[![Power Iteration](https://img.shields.io/badge/Convergence-32%20Steps%20(1e--10)-FBBC05?style=for-the-badge)]()

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#proofs--visual-demonstrations">Visual Proofs</a> •
  <a href="#mathematical-architecture">Mathematical Architecture</a> •
  <a href="#benchmark-network--exact-derivation">Benchmark Derivation</a> •
  <a href="#interactive-web-simulator">Web Simulator</a> •
  <a href="#quickstart--execution">Quickstart</a> •
  <a href="#repository-structure">Repository Structure</a>
</p>

</div>

---

## Overview

Prior to 1998, first-generation web search engines (such as AltaVista and early Yahoo!) ranked results using **lexical keyword frequency**. This simplistic design made indexing vulnerable to adversarial manipulation: page creators could repeat keywords thousands of times in hidden text to artificially capture the top ranking.

Google co-founders Larry Page and Sergey Brin resolved this architectural vulnerability through **applied linear algebra**:
1. **Hyperlinks as Endorsements:** A directed hyperlink from page $j$ to page $i$ is treated as an explicit vote of confidence.
2. **Recursive Authority:** An endorsement originating from an authoritative website carries far greater weight than one from an obscure page.
3. **Equilibrium State:** The authority of every node is determined simultaneously by finding the stationary probability distribution of a discrete-time Markov chain governed by the **Perron-Frobenius theorem**.

This repository contains an end-to-end implementation and numerical proof of the algorithm:
* **Terminal Engine (`pagerank_demo.py`):** A NumPy-based linear algebra solver that prints every matrix phase and proves exact correspondence between analytical eigensolvers and numerical power iteration.
* **Interactive Visual Simulator (`index.html`):** A zero-dependency browser application featuring real-time graph editing, dynamic matrix computation, particle surfer flows, and step-by-step power iteration playback.

---

## Proofs & Visual Demonstrations

The analytical results obtained from matrix diagonalization correspond identically to the numerical power iteration and the live browser simulator.

### 1. Interactive Graph & Matrix Web Simulator (`index.html`)

<p align="center">
  <img src="website_screenshot.png" alt="Interactive Web Simulator Proof" width="100%" style="border-radius: 8px; border: 1px solid #333333; box-shadow: 0 4px 20px rgba(0,0,0,0.4);" />
</p>
<p align="center"><em>Live canvas simulation: Dynamic node manipulation, real-time matrix decomposition, animated random-surfer flows, and live PageRank score distribution.</em></p>

---

### 2. Numerical Terminal Verification (`pagerank_demo.py`)

<p align="center">
  <img src="terminal_screenshot.png" alt="Python Terminal Execution Proof" width="100%" style="border-radius: 8px; border: 1px solid #333333; box-shadow: 0 4px 20px rgba(0,0,0,0.4);" />
</p>
<p align="center"><em>Terminal execution: Step-by-step matrix derivation displaying identical distribution between the principal eigenvector ($\mathbf{M}\mathbf{v} = \mathbf{v}$) and 32-step power iteration (maximum absolute difference: $6.36 \times 10^{-12}$).</em></p>

---

## Mathematical Architecture

The PageRank algorithm models web navigation as a random walk on a directed graph $G = (V, E)$, structured as a 5-step computational pipeline:

```
[ Directed Web Graph ]
          │
          ▼
┌──────────────────────────────────────────────┐
│  Step 1: Adjacency Matrix (A)                │
│  A[i, j] = 1 if page j links to page i       │
└──────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────┐
│  Step 2: Stochastic Transition Matrix (S)    │
│  Normalize columns by out-degree:            │
│  S[i, j] = A[i, j] / out_degree(j)           │
│  Each column sums to 1.0 (Markov property)   │
└──────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────┐
│  Step 3: Google Matrix (M)                   │
│  Apply Damping Factor (d = 0.85):            │
│  M = d·S + ((1 - d) / N)·E                   │
│  Guarantees irreducibility & aperiodicity     │
└──────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────┐
│  Step 4: Principal Eigenvector Solution      │
│  Solve linear system: M·v = 1·v              │
│  Dominant eigenvalue λ₁ = 1.0                │
└──────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────┐
│  Step 5: Power Iteration Verification        │
│  Iterate: v_(k+1) = M·v_k                    │
│  Monitored via L1 norm until Δ < 1e-10       │
└──────────────────────────────────────────────┘
```

### 1. Adjacency Matrix ($A$)
For an $N$-node graph, the adjacency matrix $A \in \{0, 1\}^{N \times N}$ is defined with destination pages as rows and source pages as columns:
$$A_{ij} = \begin{cases} 1 & \text{if page } j \text{ contains a hyperlink to page } i \\ 0 & \text{otherwise} \end{cases}$$

### 2. Stochastic Transition Matrix ($S$)
To convert the network structure into transition probabilities, each column is normalized by the out-degree $L(j) = \sum_{i=1}^N A_{ij}$:
$$S_{ij} = \begin{cases} \frac{A_{ij}}{L(j)} & \text{if } L(j) > 0 \\ \frac{1}{N} & \text{if } L(j) = 0 \text{ (dangling node)} \end{cases}$$
By construction, every column of $S$ satisfies $\sum_{i=1}^N S_{ij} = 1$, forming a valid column-stochastic Markov transition matrix.

### 3. Google Matrix ($M$) & The Random Surfer Model
Pure link structures frequently contain singularities:
* **Dead Ends (Rank Sinks):** Nodes with zero out-links leak probability mass from the system.
* **Spider Traps:** Disconnected cyclical subgraphs trap the random surfer in an infinite loop, preventing convergence to a global equilibrium.

To resolve these anomalies, a **damping factor** $d \in (0, 1)$ (conventionally $d = 0.85$) introduces uniform teleportation:
$$M = d \cdot S + \frac{1 - d}{N} E$$
where $E$ is an $N \times N$ matrix of all ones. 

**Significance:** Because $M_{ij} > 0$ for all entries, the matrix is strictly positive, **irreducible**, and **primitive**. By the **Perron-Frobenius theorem**, $M$ is mathematically guaranteed to possess a unique, positive stationary eigenvector corresponding to the dominant eigenvalue $\lambda_1 = 1$.

### 4. Principal Eigenvector Formulation
The steady-state PageRank vector $\mathbf{v}$ satisfies:
$$M \mathbf{v} = 1 \cdot \mathbf{v} \iff (M - I) \mathbf{v} = \mathbf{0}$$
normalized such that $\sum_{i=1}^N v_i = 1$.

### 5. Power Iteration & Convergence Analysis
Google computes this distribution at planetary scale via **Power Iteration**:
$$\mathbf{v}^{(0)} = \left[ \frac{1}{N}, \frac{1}{N}, \dots, \frac{1}{N} \right]^T, \quad \mathbf{v}^{(k+1)} = M \mathbf{v}^{(k)}$$

The rate of convergence is governed by the **spectral gap**:
$$\left| \frac{\lambda_2}{\lambda_1} \right| \le d = 0.85$$
After $k$ iterations, the error decays as $O(d^k)$. For a 4-node network with non-dominant eigenvalues $|\lambda_2| = 0.425$, error drops to machine precision ($< 10^{-10}$) in only 32 iterations ($0.425^{32} \approx 8.09 \times 10^{-13}$).

---

## Benchmark Network & Exact Derivation

The benchmark model consists of a 4-node directed network: **CNN**, **Yahoo**, **TechCrunch**, and **Amazon**.

```
    ┌──────────┐ ───(0.50)───▶ ┌──────────┐
    │  Yahoo   │               │   CNN    │ ◀───(1.00)─── ┌──────────┐
    └──────────┘ ◀───(0.50)─── └──────────┘               │  Amazon  │
                                    │                     └──────────┘
                                 (0.50)                        ▲
                                    ▼                        (0.50)
                               ┌──────────┐                    │
                               │TechCrunch│ ───────────────────┘
                               └──────────┘
```

### 1. Matrix Formulations

```text
Adjacency Matrix (A):                 Stochastic Matrix (S):
             CNN  Yahoo   TC   Amz                 CNN  Yahoo   TC   Amz
  CNN         0     1      1    1       CNN       0.00   1.00  0.50  1.00
  Yahoo       1     0      0    0       Yahoo     0.50   0.00  0.00  0.00
  TechCrunch  1     0      0    0       TechCrunch0.50   0.00  0.00  0.00
  Amazon      0     0      1    0       Amazon    0.00   0.00  0.50  0.00

Google Matrix (M) with d = 0.85:
             CNN     Yahoo   TechCrunch  Amazon
  CNN       0.0375  0.8875     0.4625    0.8875
  Yahoo     0.4625  0.0375     0.0375    0.0375
  TechCrunch0.4625  0.0375     0.0375    0.0375
  Amazon    0.0375  0.0375     0.4625    0.0375
```

### 2. Eigenvalue Spectrum & Final Rankings

| Rank | Node | Analytical PageRank (`np.linalg.eig`) | Numerical Power Iteration (32 steps) | Structural Authority Justification |
| :---: | :--- | :---: | :---: | :--- |
| **#1** | **CNN** | **42.9209%** | **42.9209%** | Direct recipient of links from Yahoo, TechCrunch, and Amazon |
| **#2** | **Yahoo** | **21.9914%** | **21.9914%** | Receives exactly 50% of CNN's outgoing voting authority |
| **#3** | **TechCrunch** | **21.9914%** | **21.9914%** | Symmetric distribution partner to Yahoo |
| **#4** | **Amazon** | **13.0963%** | **13.0963%** | Single inbound link from TechCrunch; zero direct CNN feed |

* **Full Eigenvalue Spectrum:** $\Lambda(M) = \{ 1.0000, -0.4250, -0.4250, 0.0000 \}$
* **Numerical Agreement:** Maximum discrepancy $|\mathbf{v}_{\text{eig}} - \mathbf{v}_{\text{iter}}|_\infty = 6.36 \times 10^{-12}$.

---

## Interactive Web Simulator

The browser application (`index.html`) is completely self-contained and operates without backend dependencies, npm builds, or external frameworks:

* **Real-Time Graph Manipulation:** Click on the canvas to instantiate nodes; drag between nodes to construct directed hyperlinks.
* **Dynamic Matrix Inspector:** Live toggle panel displaying the Adjacency, Column-Stochastic, and Google matrices updating on every graph modification.
* **Interactive Physics Engine:** Visualized node springs, glowing selection rings, and animated particle packets illustrating probability density flow along edges.
* **Damping Factor Controller:** Slider ($0.00 \le d \le 1.00$) providing immediate visual demonstration of how teleportation mitigates spider traps.
* **Step-by-Step Playback:** Controls to advance Power Iteration single-step by single-step to observe vector convergence in real time.
* **Halftone Wordmark Stage:** Integrated Google 4-color physics halftone particle banner with cursor repulsion mechanics.

---

## Quickstart & Execution

### 1. Python Terminal Engine

Requires Python 3.8+ and NumPy:

```bash
# Clone the repository
git clone https://github.com/Vanshdev3/google-pagerank.git
cd google-pagerank

# Install numerical dependencies
pip install numpy

# Execute the solver
python pagerank_demo.py
```

**Interactive Prompts:**
* **Option 1 (Default):** Runs the 4-node benchmark web (CNN, Yahoo, TechCrunch, Amazon), printing all 5 mathematical stages and verification logs.
* **Option 2 (Custom):** Prompts for an arbitrary $N \times N$ adjacency matrix row-by-row to compute any custom topology.

---

### 2. Browser Simulator

No web server or compilation required:
* **Option A (Direct):** Double-click `index.html` to open in Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari.
* **Option B (Local Server):**
  ```bash
  python -m http.server 8080
  ```
  Navigate to `http://localhost:8080` in your web browser.

---

## Repository Structure

```
google-pagerank/
├── final_cover.png                     # High-resolution 16:9 presentation banner
├── terminal_screenshot.png             # Python numerical execution proof
├── website_screenshot.png              # Interactive browser simulator proof
├── pagerank_demo.py                    # Complete Python linear algebra engine
├── index.html                          # Self-contained HTML5 Canvas web simulator
├── HOW_TO_RUN.txt                      # Step-by-step terminal execution manual
├── Explanation_and_Notes.md            # Comprehensive theoretical derivations
├── STUDENT_PRESENTATION_CHEATSHEET.md  # Detailed oral defense & viva reference guide
├── Presentation_Instructions.md        # Live demo walkthrough & speaking outline
├── PageRank_Pro_Presentation.pptx      # Professional 16:9 widescreen presentation deck
├── .gitignore                          # Standard development exclusions
└── README.md                           # Project documentation & mathematical proofs
```

---

## Technical Specifications

| Component | Technologies |
| :--- | :--- |
| **Numerical Engine** | Python 3.x, NumPy (`np.linalg.eig`, matrix algebra, vector operations) |
| **Visualization UI** | Vanilla HTML5, Canvas 2D API, Modern CSS (AMOLED dark theme), Vanilla JavaScript |
| **Typography** | Google Fonts (Inter) |
| **Presentation** | Microsoft PowerPoint (`.pptx`), 16:9 Widescreen Google dark aesthetic |
| **Mathematical Domain** | Linear Algebra, Graph Theory, Markov Chains, Perron-Frobenius Theorem, Power Iteration |

---

<div align="center">
  <sub>Mathematical formulation and computational implementation of Google's PageRank algorithm.</sub>
</div>
