# 🎓 Google PageRank — Complete Math Guide & Presentation Script
**Linear Algebra (Unit 2: Eigenvalues & Eigenvectors, Markov Chains)**

---

## 📌 Table of Contents
1. [Core Math Explained (From Zero to Mastery)](#1-core-math-explained)
2. [Step-by-Step 4-Node Benchmark Walkthrough](#2-step-by-step-4-node-benchmark-walkthrough)
3. [Why the Algorithm Works (Mathematical Proofs & Theorems)](#3-why-the-algorithm-works)
4. [Word-for-Word Oral Presentation Script](#4-word-for-word-oral-presentation-script)
5. [Live Demonstration Script (Terminal + Website)](#5-live-demonstration-script)
6. [Top 10 Viva Questions & Winning Answers](#6-top-10-viva-questions--winning-answers)

---

# 1. Core Math Explained

### 💡 The Big Picture Intuition
Imagine 4 friends: **CNN, Yahoo, TechCrunch, and Amazon**.
- If Yahoo puts a link to CNN on its website, Yahoo is giving CNN a **vote of confidence**.
- But not all votes are equal! If a famous website with thousands of votes links to you, that single vote is worth much more than a vote from an unknown blog.
- **The recursive catch:** To know how important CNN is, you must know how important Yahoo is. To know how important Yahoo is, you must know who links to Yahoo!
- **How Linear Algebra solves this:** It translates this infinite loop into an **Eigenvector equation**:
  $$M \mathbf{v} = 1 \cdot \mathbf{v}$$

---

### 🔹 Step 1: The Adjacency Matrix ($A$)
We represent the web as a **directed graph**:
- **Nodes (Vertices)** = Web pages.
- **Arrows (Edges)** = Hyperlinks.

We build a square matrix $A$ of size $N \times N$:
$$\text{Convention: } A[i][j] = \begin{cases} 1 & \text{if page } j \text{ links to page } i \\ 0 & \text{otherwise} \end{cases}$$
- **Columns = SOURCE (From)**
- **Rows = DESTINATION (To)**

> **Why this convention?**  
> Because in linear algebra, matrix-vector multiplication $y = A x$ computes linear combinations of the columns of $A$. Placing the source on the columns makes outgoing probabilities sum to 1 vertically!

---

### 🔹 Step 2: The Stochastic Transition Matrix ($S$)
An adjacency matrix only records raw connections ($0$s and $1$s). But a web surfer randomly clicks one link on a page.
If a page has $2$ outgoing links, the user has a **$50\%$ probability** ($1/2$) of clicking each.

We normalize each column by dividing each entry by the sum of that column (the out-degree):
$$S_{ij} = \frac{A_{ij}}{\sum_{k=1}^{N} A_{kj}}$$

**Properties of $S$:**
1. Every entry is between $0$ and $1$: $0 \le S_{ij} \le 1$.
2. **Every column sums to exactly $1.0$**: $\sum_{i=1}^N S_{ij} = 1$.
3. This is called a **Column-Stochastic Matrix** (representing a **discrete-time Markov Chain**).

---

### 🔹 Step 3: The Google Matrix ($M$) & The Random Surfer Model
If we only use $S$, two huge problems break the web:

1. **Dead Ends (Dangling Nodes):**  
   A page with 0 outgoing links (like a PDF file). Once a surfer lands there, they can never leave. In matrix terms, the column sum is $0$, which causes probability to leak out to $0$.
2. **Spider Traps:**  
   A loop of pages that only link to each other (e.g., Page A $\leftrightarrow$ Page B). Probability enters the loop and gets trapped forever, making all other pages score $0$.

#### 💡 The Solution: Teleportation & Damping Factor ($d = 0.85$)
Larry Page and Sergey Brin introduced the **Random Surfer Model**:
- **85% of the time ($d = 0.85$):** The user clicks a hyperlink on the current page.
- **15% of the time ($1 - d = 0.15$):** The user gets bored, opens a new browser tab, and types a completely random web address.

The **Google Matrix ($M$)** is defined as:
$$M = d \cdot S + \frac{1 - d}{N} \cdot E$$
- $N$ = total number of pages.
- $E$ = an $N \times N$ matrix of all ones ($E_{ij} = 1$).
- $\frac{1 - d}{N} = \frac{0.15}{4} = 0.0375$ (every single page receives a minimum baseline probability).

**Why this is mathematically crucial:**
Adding teleportation ensures **every entry in $M$ is strictly positive ($M_{ij} > 0$)**. This guarantees that the matrix is **irreducible** and **primitive** (no traps, no dead ends).

---

### 🔹 Step 4: The Eigenvector (PageRank Vector)
After surfing for hours, what is the probability that the user is on page $i$?
This long-term stationary distribution is a vector $\mathbf{v}$ that satisfies:
$$M \mathbf{v} = \mathbf{v}$$
In standard linear algebra notation ($M \mathbf{v} = \lambda \mathbf{v}$):
$$M \mathbf{v} = 1 \cdot \mathbf{v}$$
- The **eigenvalue $\lambda$ is strictly $1.0$**.
- The corresponding **eigenvector $\mathbf{v}$ is the PageRank vector**.
- We normalize $\mathbf{v}$ so that its components sum to $1$ (or $100\%$):
  $$\sum_{i=1}^N v_i = 1$$

---

### 🔹 Step 5: Power Iteration (How to Compute for Billions of Pages)
Calculating eigenvalues analytically using determinants $\det(M - \lambda I) = 0$ requires $O(N^3)$ operations. With billions of web pages, this is computationally impossible!

Instead, Google uses **Power Iteration**:
1. Start with an equal guess for all pages:
   $$\mathbf{v}^{(0)} = \left[ \frac{1}{N}, \frac{1}{N}, \dots, \frac{1}{N} \right]^T$$
2. Repeatedly multiply by the Google Matrix:
   $$\mathbf{v}^{(k+1)} = M \cdot \mathbf{v}^{(k)}$$
3. Stop when the change is smaller than a threshold:
   $$\| \mathbf{v}^{(k+1)} - \mathbf{v}^{(k)} \|_1 < 10^{-10}$$

**Why Power Iteration is guaranteed to converge:**
Any vector can be written as a linear combination of eigenvectors:
$$\mathbf{v}^{(0)} = c_1 \mathbf{u}_1 + c_2 \mathbf{u}_2 + \dots + c_N \mathbf{u}_N$$
Multiplying by $M$ repeatedly $k$ times:
$$M^k \mathbf{v}^{(0)} = c_1 (\lambda_1)^k \mathbf{u}_1 + c_2 (\lambda_2)^k \mathbf{u}_2 + \dots + c_N (\lambda_N)^k \mathbf{u}_N$$
- Since $\lambda_1 = 1$, $(\lambda_1)^k = 1^k = 1$ (stays constant).
- Since $|\lambda_i| < 1$ for all other eigenvalues, $(\lambda_i)^k \to 0$ as $k \to \infty$!
- Everything except the principal eigenvector decays to zero!

---

# 2. Step-by-Step 4-Node Benchmark Walkthrough

In our project (`pagerank_demo.py` and `index.html`), we model 4 pages:
- **CNN** links to **Yahoo** and **TechCrunch**
- **Yahoo** links to **CNN**
- **TechCrunch** links to **CNN** and **Amazon**
- **Amazon** links to **CNN**

### 1. Adjacency Matrix ($A$)
```
             CNN   Yahoo    TC   Amazon
CNN            0       1     1        1    <-- CNN receives from Yahoo, TC, Amazon
Yahoo          1       0     0        0    <-- Yahoo receives from CNN
TechCrunch     1       0     0        0    <-- TechCrunch receives from CNN
Amazon         0       0     1        0    <-- Amazon receives from TC
```

### 2. Stochastic Matrix ($S$)
Divide each column by its column sum:
- CNN has 2 outlinks: column is divided by 2 $\to [0, 0.5, 0.5, 0]^T$
- Yahoo has 1 outlink: column is divided by 1 $\to [1, 0, 0, 0]^T$
- TechCrunch has 2 outlinks: column is divided by 2 $\to [0.5, 0, 0, 0.5]^T$
- Amazon has 1 outlink: column is divided by 1 $\to [1, 0, 0, 0]^T$

```
             CNN   Yahoo    TC   Amazon
CNN         0.00    1.00  0.50     1.00
Yahoo       0.50    0.00  0.00     0.00
TechCrunch  0.50    0.00  0.00     0.00
Amazon      0.00    0.00  0.50     0.00
```
*(Every column sums to $1.0$)*

### 3. Google Matrix ($M$) with $d = 0.85$
Each entry: $M_{ij} = 0.85 \cdot S_{ij} + \frac{0.15}{4} = 0.85 \cdot S_{ij} + 0.0375$
- If $S_{ij} = 0 \implies 0.85(0) + 0.0375 = \mathbf{0.0375}$
- If $S_{ij} = 0.5 \implies 0.85(0.5) + 0.0375 = \mathbf{0.4625}$
- If $S_{ij} = 1.0 \implies 0.85(1.0) + 0.0375 = \mathbf{0.8875}$

```
             CNN    Yahoo     TC   Amazon
CNN        0.0375  0.8875  0.4625  0.8875
Yahoo      0.4625  0.0375  0.0375  0.0375
TechCrunch 0.4625  0.0375  0.0375  0.0375
Amazon     0.0375  0.0375  0.4625  0.0375
```

### 4. Eigenvalues of $M$
Calculated via `np.linalg.eig(M)`:
$$\lambda_1 = 1.000, \quad \lambda_2 = -0.425, \quad \lambda_3 = -0.425, \quad \lambda_4 = 0.000$$
- $\lambda_1 = 1.000$ is the dominant eigenvalue.
- The **spectral gap** is $1.0 - 0.425 = 0.575$.
- Rate of convergence = $0.425$. In 32 iterations: $(-0.425)^{32} \approx 6.4 \times 10^{-13}$ (machine precision!).

### 5. Final PageRank Scores
$$\mathbf{v} = \begin{bmatrix} \text{CNN} \\ \text{Yahoo} \\ \text{TechCrunch} \\ \text{Amazon} \end{bmatrix} = \begin{bmatrix} \mathbf{42.92\%} \\ \mathbf{21.99\%} \\ \mathbf{21.99\%} \\ \mathbf{13.10\%} \end{bmatrix}$$

**Why CNN wins so clearly:**
- CNN receives incoming links from Yahoo, TechCrunch, and Amazon.
- Yahoo and TechCrunch tie at 21.99% because CNN evenly splits its high authority between them.
- Amazon receives only 1 incoming link (from TechCrunch) and ranks last at 13.10%.

---

# 3. Why the Algorithm Works

### 1. The Perron-Frobenius Theorem
> **Theorem Statement:**  
> If $M$ is a real, square matrix with strictly positive entries ($M_{ij} > 0$), then:
> 1. There exists a unique, real, largest eigenvalue $\lambda_1 > 0$.
> 2. For a column-stochastic matrix, this largest eigenvalue is **strictly $\lambda_1 = 1$**.
> 3. All other eigenvalues satisfy $|\lambda_i| < \lambda_1$.
> 4. The eigenvector associated with $\lambda_1 = 1$ has **strictly positive components** ($v_i > 0$).

**What this guarantees for Google:**
- There is **always exactly one unique ranking**.
- No web page will ever get a negative score.
- The algorithm will never oscillate or fail to converge.

### 2. Syllabus Mapping (Unit 1 & Unit 2)
- **Unit 2 (Eigenvalues & Eigenvectors):** Solving $M \mathbf{v} = 1 \cdot \mathbf{v}$.
- **Unit 2 (Markov Chains):** Long-term steady-state probability vector.
- **Unit 2 (Power Iteration):** Numerical iterative method for dominant eigenvector.
- **Unit 2 (Vector Norms):** Normalizing $\mathbf{v}$ using the $L_1$ norm ($\sum |v_i| = 1$).
- **Unit 1 (Matrix Multiplication):** Dot products between rows of $M$ and vector $\mathbf{v}$.
- **Unit 1 (Rank & Null Space):** $(M - I)\mathbf{v} = \mathbf{0}$ means finding the 1-dimensional null space of $(M - I)$.

---

# 4. Word-for-Word Oral Presentation Script

Use this exact flow when speaking:

### Slide 1 & 2: Title & Roadmap
> *"Good morning, Sir. Today I am presenting our project on **Google PageRank: A Linear Algebra Application** under Unit 2.*
> *We will cover the problem with early search engines, Google's hyperlink insight, the 5-step matrix derivation, and a live demonstration of both our Python engine and our interactive web simulator."*

### Slide 3: The Problem Before Google
> *"Before 1998, search engines like Yahoo and AltaVista used **keyword density**. If you searched for 'Cars', the page that repeated the word 'Cars' the most was ranked #1. Spammers exploited this by hiding keywords thousands of times in invisible text. Content quality did not matter."*

### Slide 4: The Google Idea
> *"Larry Page and Sergey Brin solved this using linear algebra. They realized that a hyperlink is a **vote of confidence**. If CNN links to another site, CNN is endorsing it. Furthermore, votes are weighted: a link from CNN is worth much more than a link from a personal blog. Because this is recursive, it is modeled as an eigenvalue problem."*

### Slides 5 to 9: The Matrices ($A \to S \to M$)
> *"We implement this in 4 matrix steps:*
> 1. *First, the **Adjacency Matrix $A$**, recording raw connections where columns represent source pages and rows represent destination pages.*
> 2. *Second, the **Stochastic Matrix $S$**, where each column is divided by its out-degree so each column sums to 1. This represents the probability of a user following a link.*
> 3. *Third, to prevent users getting trapped in dead ends or spider loops, we apply the **Random Surfer model** with a **damping factor $d = 0.85$** to create the **Google Matrix $M$**.*
> *This means an 85% chance of following a link and a 15% chance of teleporting to any random page."*

### Slides 10 to 12: The Eigenvector & Power Iteration
> *"By the **Perron-Frobenius theorem**, because $M$ is column-stochastic and strictly positive, its dominant eigenvalue is **strictly $\lambda = 1$**.*
> *The eigenvector corresponding to $\lambda = 1$ gives the exact PageRank score.*
> *To compute this efficiently, we implement **Power Iteration** ($v_{k+1} = M \cdot v_k$), which starts with equal probabilities and converges in 32 iterations."*

### Slide 13: Results
> *"In our benchmark, **CNN ranks #1 at 42.92%** because it receives links from Yahoo, TechCrunch, and Amazon. Yahoo and TechCrunch tie at 21.99%, and Amazon finishes at 13.10%."*

---

# 5. Live Demonstration Script

### Step 1: Terminal Demonstration
1. Open terminal in the project folder.
2. Run:
   ```powershell
   python pagerank_demo.py
   ```
3. Press **Enter** (Option 1).
4. **Say to Sir:**
   > *"Sir, here is our complete terminal pipeline:*
   > - *Step 1 shows our $4 \times 4$ Adjacency Matrix.*
   > - *Step 2 shows our column-stochastic matrix $S$, where all column sums equal exactly 1.0.*
   > - *Step 3 shows the Google Matrix $M$ with damping factor $0.85$.*
   > - *Step 4 uses NumPy's `np.linalg.eig` to find the analytical eigenvalues. As you can see, the dominant eigenvalue is exactly $1.0$, and the other eigenvalues are $-0.425$ and $0.0$.*
   > - *Step 5 verifies the result using Power Iteration. It converges in 32 iterations, matching the analytical eigenvector to 12 decimal places."*

### Step 2: Interactive Web Simulator Demonstration
1. Open `http://localhost:8080` (or double-click `index.html`).
2. **Say to Sir:**
   > *"Sir, we also engineered this interactive web simulator using HTML5 Canvas and JavaScript to visualize the mathematics in real time:*
   > 1. *I can drag nodes around to reorganize the graph.*
   > 2. *If I click **'Draw Link'** and connect Yahoo to Amazon, you can see on the right panel that the Adjacency, Stochastic, and Google matrices update instantly.*
   > 3. *The simulator runs Power Iteration on every frame, dynamically updating the ranking cards."*

---

# 6. Top 10 Viva Questions & Winning Answers

#### 1. Why is the dominant eigenvalue $\lambda = 1$?
> **Answer:** Because the Google Matrix $M$ is **column-stochastic** (each column sums to $1.0$). By the Perron-Frobenius theorem, the spectral radius of any stochastic matrix is $1$, so its largest eigenvalue is guaranteed to be $\lambda = 1$.

#### 2. What is a Dead End (Dangling Node) and how is it handled?
> **Answer:** A dead end is a page with no outgoing links. Its column sum would be 0, causing probability to leak out. We handle this by replacing zero columns with $\frac{1}{N}$ (uniform distribution over all pages) before applying the damping factor.

#### 3. What is a Spider Trap?
> **Answer:** A group of pages that only link to each other. Surfers get stuck in the loop forever. The 15% random teleportation ($1-d$) allows surfers to escape spider traps.

#### 4. Why is the damping factor chosen as $d = 0.85$?
> **Answer:** Larry Page and Sergey Brin experimentally determined $0.85$. It balances real link structure (85%) with fast mathematical convergence. A higher $d$ slows down convergence; a lower $d$ gives too much weight to random teleportation.

#### 5. What is the Spectral Gap?
> **Answer:** It is the difference between the dominant eigenvalue and the second-largest eigenvalue:
> $$\text{Spectral Gap} = |\lambda_1| - |\lambda_2| = 1.0 - 0.425 = 0.575$$
> A larger spectral gap means faster convergence during Power Iteration.

#### 6. Why use Power Iteration instead of solving $(M - I)\mathbf{v} = 0$ via Gaussian Elimination?
> **Answer:** Gaussian elimination takes $O(N^3)$ time and requires storing a dense matrix. With billions of web pages, $N^3$ is impossible. Power Iteration only takes $O(k \cdot E)$ where $E$ is the number of links, which is sparse and fast.

#### 7. Why do we normalize columns instead of rows?
> **Answer:** Because we set $A_{ij} = 1$ for a link from column $j$ to row $i$. This makes outgoing links sum along columns, leading to the column-stochastic formulation $M \mathbf{v} = \mathbf{v}$. (If rows were used, we would write $\mathbf{v}^T M = \mathbf{v}^T$).

#### 8. What norm is used to normalize the PageRank vector?
> **Answer:** The **$L_1$ norm** ($\sum_{i=1}^N |v_i| = 1$), because the vector represents probabilities that must add up to $1$ (or $100\%$).

#### 9. What happens if $d = 1$ and what if $d = 0$?
> **Answer:**
> - If $d = 1$: No teleportation. Dead ends cause probability loss, and spider traps trap the rank.
> - If $d = 0$: Pure teleportation. Every page gets an identical score of $\frac{1}{N} = 25\%$, ignoring links entirely.

#### 10. Where is this algorithm used today outside of Google?
> **Answer:**
> - **Social Networks:** Twitter/X's recommendation engine ("Who to follow") to identify top influencers.
> - **Bioinformatics:** Identifying critical proteins and gene interactions in disease pathways.
> - **Finance:** Fraud detection and anti-money laundering by finding anomalous transaction hubs.

---
*Created for your presentation. Keep this open during your prep and viva!*
