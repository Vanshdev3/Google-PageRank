# Google PageRank — Linear Algebra Application

> **Unit 2 Project | Eigenvalues and Eigenvectors**
> Demonstrating how Google PageRank is built on matrix operations, Markov chains, and the Perron-Frobenius theorem.

---

## What This Project Is

Before 1998, search engines ranked pages by keyword frequency, a system trivially gamed by spammers. Larry Page and Sergey Brin solved this using **Linear Algebra**: treat every hyperlink as a vote, model the web as a stochastic matrix, and compute the steady-state eigenvector.

This project implements that math from scratch:

- A **Python terminal script** that walks through every matrix step with printed output
- An **interactive web simulator** (HTML + vanilla JS) where you draw a live network and watch PageRank converge

---

## Repository Structure

```
google-pagerank/
|
|-- pagerank_demo.py               Core Python implementation (NumPy)
|-- index.html                     Interactive web simulator (no dependencies)
|-- Explanation_and_Notes.md       Full mathematical walkthrough
|-- Presentation_Instructions.md  Demo guide for presenting
|-- PageRank_Pro_Presentation.pptx Final slide deck
|-- final_cover.png                Cover image used in the presentation
|-- terminal_screenshot.png        Output of pagerank_demo.py
|-- website_screenshot.png         Screenshot of the web simulator
|-- README.md
```

---

## The Mathematics

A 4-step pipeline from raw link data to a ranked probability vector.

### Step 1 - Adjacency Matrix (A)

Model the web as a directed graph. A[i][j] = 1 means page j links to page i.

4-node benchmark: CNN, Yahoo, TechCrunch, Amazon

Link structure:
  CNN        ->  Yahoo, TechCrunch
  Yahoo      ->  CNN
  TechCrunch ->  CNN, Amazon
  Amazon     ->  CNN

```
Adjacency Matrix A:
               CNN   Yahoo    TC   Amazon
  CNN            0       1     1        1
  Yahoo          1       0     0        0
  TechCrunch     1       0     0        0
  Amazon         0       0     1        0
```

### Step 2 - Stochastic Transition Matrix (S)

Normalize each column by its out-degree. Every column sums to 1.0.

```
S[i][j] = A[i][j] / sum(column j)

               CNN   Yahoo    TC   Amazon
  CNN         0.00    1.00  0.50     1.00
  Yahoo       0.50    0.00  0.00     0.00
  TechCrunch  0.50    0.00  0.00     0.00
  Amazon      0.00    0.00  0.50     0.00
```

### Step 3 - Google Matrix (M)

Pure transition matrices fail on dead ends and spider traps.
Fix: damping factor d = 0.85 + uniform teleportation matrix E.

```
M = d * S  +  (1 - d) / N * E

d = 0.85  ->  85% chance: follow a real link
1-d = 0.15 -> 15% chance: jump to a random page

               CNN    Yahoo     TC   Amazon
  CNN         0.038   0.888  0.463    0.888
  Yahoo       0.463   0.038  0.038    0.038
  TechCrunch  0.463   0.038  0.038    0.038
  Amazon      0.038   0.038  0.463    0.038
```

M is guaranteed to be irreducible, aperiodic, and primitive.

### Step 4 - Principal Eigenvector (PageRank)

By the Perron-Frobenius theorem, a primitive stochastic matrix has a unique dominant eigenvalue of exactly lambda = 1.
The corresponding eigenvector is the PageRank vector.

```
M * v = 1 * v

All eigenvalues of M: [1.0, -0.425, -0.425, 0.0]
The others have magnitude < 1, so they decay to zero during iteration.
```

### Step 5 - Power Iteration (Verification)

```
v_0     = [0.25, 0.25, 0.25, 0.25]   (uniform start)
v_(k+1) = M * v_k

Converges in 32 iterations to L1 norm < 1e-10
```

### Final Results

```
  Rank   Page          Score
  ----   ----------    -------
  #1     CNN           42.92%
  #2     Yahoo         21.99%
  #3     TechCrunch    21.99%
  #4     Amazon        13.10%

  np.linalg.eig() and Power Iteration agree to 12 decimal places.
```

CNN wins because it receives links from Yahoo, TechCrunch, and Amazon.

---

## Eigenvalue Convergence Analysis

```
  lambda_1 =  1.000  ->  PageRank (stationary distribution)
  lambda_2 = -0.425  ->  decays: (-0.425)^32 ~ 10^-12
  lambda_3 = -0.425  ->  decays
  lambda_4 =  0.000  ->  already zero

  Spectral gap = 1.0 - 0.425 = 0.575
  Convergence rate per iteration ~ 0.425
```

---

## How to Run

### Python Script

Requires Python 3.x and NumPy.

```bash
pip install numpy
python pagerank_demo.py
```

Press 1 (or Enter) for the default 4-node benchmark.
Press 2 to enter your own adjacency matrix.

Output steps:
```
Step 1  Adjacency Matrix       (raw link graph)
Step 2  Stochastic Matrix      (normalized probabilities)
Step 3  Google Matrix          (with damping factor)
Step 4  Eigenvector Method     (np.linalg.eig, exact)
Step 5  Power Iteration        (iterative, converges in 32 steps)
```

### Web Simulator

Open `index.html` in any browser. No server or installation needed.

Features:
- Draw your own network (click to add nodes, drag to connect)
- Real-time PageRank recalculation on every change
- Toggle matrix view (adjacency, stochastic, Google)
- Step-by-step power iteration mode
- AMOLED dark mode, Google color scheme

---

## Key Concepts

| Concept                      | Where Demonstrated              |
|------------------------------|---------------------------------|
| Matrix construction          | pagerank_demo.py Steps 1-3      |
| Column-stochastic normalize  | Step 2                          |
| Markov Chain / Random Surfer | Step 3, index.html              |
| Perron-Frobenius Theorem     | Step 4                          |
| np.linalg.eig()              | Step 4, Python output           |
| Power Iteration              | Step 5, web simulator           |
| Eigenvalue convergence       | Explanation_and_Notes.md        |

---

## Tech Stack

```
Python
  numpy          matrix operations, np.linalg.eig()

Web Simulator
  HTML5 Canvas   graph drawing and animation
  Vanilla JS     Power Iteration (no libraries)
  CSS            AMOLED dark mode, Google palette
  Google Fonts   Inter

Presentation
  python-pptx    programmatic slide generation
```

---

## Unit 2 Syllabus Concepts Used

- Matrices and Matrix Multiplication
- Column Normalization
- Eigenvalues and Eigenvectors
- Markov Chains (Stochastic Processes)
- Perron-Frobenius Theorem
- Power Iteration (Numerical Method)
- Spectral Gap and Convergence Rate

---

*Linear Algebra Unit 2 Project | Google PageRank*
