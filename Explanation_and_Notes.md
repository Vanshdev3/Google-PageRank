# Google PageRank: A Linear Algebra Application (Unit 2)

## 1. Project Background and History
Before 1998, search engines like Yahoo! and AltaVista ranked websites based on **keyword density**. If you searched for "Cars", the search engine simply looked for the website that had the word "Cars" written the most times. 
This was fundamentally flawed. Spammers realized they could just hide the word "Cars" invisibly on their page 10,000 times, and they would instantly rank #1.

### The Google Solution
Larry Page and Sergey Brin (founders of Google) solved this using **Linear Algebra**.
They realized that a hyperlink is a vote of confidence. If Apple.com links to CNN.com, Apple is saying "I trust CNN". Furthermore, a link from a highly trusted site (like Apple) should count for more than a link from a random blog.

This isn't just a simple counting problem. This is a recursive mathematical problem that is perfectly solved using **Matrices and Eigenvectors**.

---

## 2. The Mathematics (Step-by-Step Implementation)

Let's imagine a tiny internet with only 4 websites: **Apple**, **Bing**, **CNN**, and **Disney**.
Assume the following links exist:
- Apple links to Bing and CNN.
- Bing links to CNN.
- CNN links to Apple and Disney.
- Disney links to CNN.

How do we find which page is the most important using Linear Algebra?

### Step 1: The Adjacency Matrix ($A$)
First, we construct a square matrix (4x4 in this case) representing the raw structure of the web. 
- **Columns** represent where the link is coming *From*.
- **Rows** represent where the link is going *To*.

If Apple (Column 1) links to Bing (Row 2), we put a `1`. Otherwise, `0`.

```text
                 Apple       Bing        CNN     Disney
     Apple           0          0          1          0
      Bing           1          0          0          0
       CNN           1          1          0          1
    Disney           0          0          1          0
```

### Step 2: The Stochastic Matrix ($S$)
An Adjacency Matrix just tells us if a link exists. But we need probabilities. 
If Apple links to 2 websites (Bing and CNN), and a user is on Apple.com, there is a **50% chance** they click Bing and a **50% chance** they click CNN.
To find this matrix, we simply divide each column by the sum of that column (the number of outgoing links).

```text
                 Apple       Bing        CNN     Disney
     Apple        0.00       0.00       0.50       0.00
      Bing        0.50       0.00       0.00       0.00
       CNN        0.50       1.00       0.00       1.00
    Disney        0.00       0.00       0.50       0.00
```
This is a Markov Chain probability matrix. The sum of every column is exactly 1.0 (100%).

### Step 3: The Google Matrix ($G$)
In the real world, users don't *only* click links. Sometimes they get bored, open a new tab, and randomly type a new URL. This is called the "Random Surfer Model".
Google uses a **Damping Factor ($d$)** of usually 0.85 (85%). 
This means there is an 85% chance the user clicks a link (using Matrix S), and a 15% chance they randomly teleport anywhere else on the web.

The formula for the Google Matrix is:
$$G = 0.85 \cdot S + 0.15 \cdot \frac{1}{N} \cdot E$$
*(Where N is the number of pages, and E is a matrix of all 1s).*

```text
                 Apple       Bing        CNN     Disney
     Apple        0.04       0.04       0.46       0.04
      Bing        0.46       0.04       0.04       0.04
       CNN        0.46       0.89       0.04       0.89
    Disney        0.04       0.04       0.46       0.04
```

### Step 4: The Eigenvector (The Final PageRank!)
Now for the magic. We want to find the steady-state vector, which represents the long-term probability of a user landing on any specific page.
Mathematically, this equation is:
$$G \vec{v} = \lambda \vec{v}$$
Where $\lambda$ is the Eigenvalue, and $\vec{v}$ is the Eigenvector.

Because $G$ is a stochastic matrix, its largest Eigenvalue is **exactly 1**.
Therefore, we just need to find the **Eigenvector corresponding to $\lambda = 1$**.

Using `np.linalg.eig(G)` in Python, we find that Eigenvector, normalize it so it adds up to 100%, and get our final PageRank scores:

- **CNN**: 42.92%
- **Apple**: 21.99%
- **Disney**: 21.99%
- **Bing**: 13.10%

CNN receives links from Apple, Bing, *and* Disney, making it the most central node in this tiny internet! Apple and Disney tie exactly, because each receives exactly half of CNN's vote (CNN splits its importance between them).
(Other eigenvalues of G: 0, -0.425, -0.425 — all smaller than 1 in magnitude, which is why Power Iteration converges.)

---

## 3. Technology Used in this Project

1. **Python Backend (`pagerank_demo.py`)**:
   - Uses `numpy` (`np.linalg.eig`) to mathematically construct the matrices and calculate the Eigenvalues and Eigenvectors identically to how it is taught in Unit 2 of the syllabus.
   
2. **Interactive UI (`index.html`)**:
   - Built with Vanilla HTML5 Canvas, CSS (AMOLED Dark Mode), and JavaScript.
   - Calculates the exact same math in real-time using Power Iteration.
   - Allows users to dynamically add/remove nodes and draw edges, making the abstract math immediately visible.

3. **Presentation Generation (`create_comprehensive_ppt.py`)**:
   - Uses `python-pptx` to programmatically generate an aesthetically pleasing, Google-themed dark mode presentation explaining the math.
