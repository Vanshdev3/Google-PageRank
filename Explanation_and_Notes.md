# Google PageRank: A Linear Algebra Application (Unit 2)

## 1. Project Background and History
Before 1998, search engines like Yahoo! and AltaVista ranked websites based on **keyword density**. If you searched for "Cars", the search engine simply looked for the website that had the word "Cars" written the most times. 
This was fundamentally flawed. Spammers realized they could just hide the word "Cars" invisibly on their page 10,000 times, and they would instantly rank #1.

### The Google Solution
Larry Page and Sergey Brin (founders of Google) solved this using **Linear Algebra**.
They realized that a hyperlink is a vote of confidence. If Yahoo links to CNN, Yahoo is saying "I trust CNN". Furthermore, a link from a highly trusted site should count for more than a link from an obscure blog.

This is not a simple counting problem. This is a recursive mathematical system solved via **Markov Chains, Stochastic Matrices, and Eigenvectors**.

---

## 2. The Mathematics (Step-by-Step Implementation)

Let's consider a benchmark network with 4 web nodes: **CNN**, **Yahoo**, **TechCrunch**, and **Amazon**.

Assume the following hyperlink structure:
- **CNN** links to **Yahoo** and **TechCrunch**.
- **Yahoo** links to **CNN**.
- **TechCrunch** links to **CNN** and **Amazon**.
- **Amazon** links to **CNN**.

How do we determine the structural authority of each page using Linear Algebra?

### Step 1: The Adjacency Matrix ($A$)
First, we construct a square $4 \times 4$ adjacency matrix representing the link graph.
- **Columns** represent the source page (*From*).
- **Rows** represent the destination page (*To*).
- An entry is `1` if a link exists from column $j$ to row $i$, else `0`.

```text
                 CNN       Yahoo  TechCrunch      Amazon
       CNN         0           1           1           1
     Yahoo         1           0           0           0
TechCrunch         1           0           0           0
    Amazon         0           0           1           0
```

### Step 2: The Stochastic Transition Matrix ($S$)
An adjacency matrix only records connectivity. To model web navigation probabilities, we normalize each column by the total number of outgoing links (the column sum).
If CNN links to 2 websites (Yahoo and TechCrunch), a user on CNN has a **50% probability** of navigating to Yahoo and **50%** to TechCrunch.

```text
                 CNN       Yahoo  TechCrunch      Amazon
       CNN      0.00        1.00        0.50        1.00
     Yahoo      0.50        0.00        0.00        0.00
TechCrunch      0.50        0.00        0.00        0.00
    Amazon      0.00        0.00        0.50        0.00
```
Every column sum equals exactly $1.0$, satisfying the requirement of a column-stochastic Markov transition matrix.

### Step 3: The Google Matrix ($M$)
In practice, web users do not exclusively follow hyperlinks. Occasionally, a user teleports by typing a completely new address into the browser bar. This behavior is captured by the **Random Surfer Model**.

Google applies a **Damping Factor ($d$)**, typically set to $0.85$ (85%).
This implies an 85% probability that the surfer follows an outgoing link, and a 15% probability ($1 - d = 0.15$) that they teleport uniformly to any page in the network.

The Google Matrix is defined as:
$$M = d \cdot S + \frac{1 - d}{N} \cdot E$$
*(where $N = 4$ is the number of nodes, and $E$ is an $N \times N$ matrix of all ones).*

```text
                 CNN       Yahoo  TechCrunch      Amazon
       CNN    0.0375      0.8875      0.4625      0.8875
     Yahoo    0.4625      0.0375      0.0375      0.0375
TechCrunch    0.4625      0.0375      0.0375      0.0375
    Amazon    0.0375      0.0375      0.4625      0.0375
```
By adding teleportation, $M$ is guaranteed to be **irreducible** and **primitive**, ensuring the existence of a unique positive stationary distribution (Perron-Frobenius theorem).

### Step 4: The Eigenvector (PageRank Calculation)
The long-term stationary probability distribution satisfies:
$$M \mathbf{v} = \lambda \mathbf{v}$$
where $\lambda$ is the eigenvalue, and $\mathbf{v}$ is the stationary eigenvector.

Because $M$ is column-stochastic, its dominant eigenvalue is strictly $\lambda = 1$. The corresponding principal eigenvector, normalized such that $\sum v_i = 1$, yields the final PageRank scores:

- **CNN**: **42.92%**
- **Yahoo**: **21.99%**
- **TechCrunch**: **21.99%**
- **Amazon**: **13.10%**

**Analysis:**
- **CNN** receives incoming links from Yahoo, TechCrunch, and Amazon, establishing it as the most authoritative node in this network.
- **Yahoo** and **TechCrunch** tie at 21.99% because CNN evenly distributes its high voting authority between them.
- **Amazon** receives only half of TechCrunch's outlinks and has no other inlinks, ranking at 13.10%.

The non-dominant eigenvalues of $M$ are $\lambda \in \{ -0.425, -0.425, 0.0 \}$. Since $|\lambda_i| < 1$ for all $i \ge 2$, iterative matrix multiplication (**Power Iteration**) is guaranteed to converge rapidly to the principal eigenvector.

---

## 3. Technology Used in this Project

1. **Python CLI Application (`pagerank_demo.py`)**:
   - Uses `numpy` (`np.linalg.eig`) to construct all matrices and compute the analytical eigenvalues and eigenvectors.
   - Includes numerical verification via Power Iteration ($v^{(k+1)} = M v^{(k)}$), showing convergence in 32 iterations.

2. **Interactive Web Simulator (`index.html`)**:
   - Built with Vanilla HTML5 Canvas, modern AMOLED dark mode CSS, and JavaScript.
   - Computes PageRank dynamically in real time as nodes and edges are added, moved, or deleted.
   - Includes interactive controls for damping factors, live step-by-step matrix visualization, and convergence traces.

3. **Presentation Generation (`PageRank_Pro_Presentation.pptx`)**:
   - Professionally formatted 16:9 slides with Google aesthetics detailing the mathematics, applications, and demonstration.
