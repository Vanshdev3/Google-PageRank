# PageRank Project - Presentation Guide

## 1. Files Included in this Project
* **PageRank_Pro_Presentation.pptx**: The final presentation deck (16:9).
* **pagerank_demo.py**: The terminal application to calculate PageRank step-by-step.
* **index.html**: The interactive web simulator.
* **HOW_TO_RUN.txt**: Quick start instructions and command guide.
* **README.md**: Complete project overview with mathematical ASCII diagrams.
* **Explanation_and_Notes.md**: The in-depth mathematical explanation and theory.

---

## 2. Setting Up the Demonstration

Before you start presenting, get your terminal and browser ready so you can seamlessly switch to them during the live demo part.

### Step A: Terminal Demo Setup
1. Open a terminal or command prompt in the extracted project folder.
2. Ensure you have Python and NumPy installed (`pip install numpy`).
3. Keep the terminal open. You will run this command later:
   `python pagerank_demo.py`

### Step B: Web Simulator Setup
1. Open a second terminal window in the project folder.
2. Run a local web server to host the HTML file:
   `python -m http.server 8080`
   *(Alternatively, simply double-click `index.html` to open it in your browser).*
3. Open your web browser and go to: **http://localhost:8080**
4. Keep this tab open and ready to show.

---

## 3. How to Present (Slide by Slide Points)

### The Problem (Pre-1998 Search Engines)
* Explain how early search engines (like Yahoo and AltaVista) only used **Keyword Density**.
* Explain the flaw: Spammers could hide the word 'Cars' 10,000 times invisibly and rank #1 without having good content.

### The Google Solution
* Explain that Larry Page and Sergey Brin treated a hyperlink as a **vote of confidence**.
* A link from a trusted authority site is worth more than a link from a random spam blog.
* This is not just counting; it is a recursive problem solved by **Linear Algebra (Eigenvalues & Eigenvectors)**.

### The Mathematics (Matrices)
* **Adjacency Matrix (A)**: Shows the raw connectivity of who links to whom.
* **Stochastic Matrix (S)**: Shows transition probabilities. If a page has 2 outgoing links, each link has a 50% probability of being clicked. Columns sum to 1.
* **Google Matrix (M)**: Introduces the **Random Surfer Model** (Damping factor $d = 0.85$). There is an 85% chance a user clicks a link, and a 15% chance they teleport to a random page. This eliminates zero-probability sinks and guarantees a unique solution.

### The Eigenvector (PageRank)
* Explain the equation: **$M \mathbf{v} = 1 \cdot \mathbf{v}$**
* We are finding the steady-state probability vector $\mathbf{v}$ (the PageRank).
* Because the matrix is column-stochastic and primitive, the dominant eigenvalue $\lambda$ is exactly **1.0** (Perron-Frobenius theorem).
* Explain that computing this principal eigenvector provides the definitive ranking.

---

## 4. Live Demonstration

When you reach the Live Demo slides, switch out of PowerPoint to show the code working!

### Part 1: Terminal Code Demo
1. Switch to your terminal.
2. Run: `python pagerank_demo.py`
3. Type `1` and hit Enter to use the default 4-node benchmark.
4. **Explain to the examiner**: "Here we see all 5 steps: Adjacency, Stochastic, Google Matrix, Principal Eigenvector via np.linalg.eig(), and Power Iteration verification. CNN ranks #1 at 42.92% because it receives links from Yahoo, TechCrunch, and Amazon."
5. (Optional) You can run it again and choose `2` to show you can input any custom matrix.

### Part 2: Web Simulator Demo
1. Switch to your web browser (**http://localhost:8080**).
2. **Explain to the examiner**: "This is a custom Vanilla Canvas simulator computing the mathematics live using Power Iteration."
3. **Showcase features**:
   * Drag the nodes around the screen.
   * Draw a new link (e.g., from Yahoo to Amazon) and watch the matrices and rankings update instantly.
   * Adjust the damping factor slider to demonstrate the effect of random teleportation.
   * Add a new node to show the matrix dynamically expanding from 4x4 to 5x5.

---

## 5. Wrapping Up
* Mention that this exact math is what organized the early internet.
* Briefly note that today, these graph algorithms are also applied in Social Networks (identifying key influencers), Recommendation Engines, and Fraud Detection (spotting suspicious transaction hubs).
