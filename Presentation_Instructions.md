# PageRank Project - Presentation Guide

## 1. Files Included in this Zip
* **PageRank_Pro_Presentation.pptx**: The final presentation deck.
* **pagerank_demo.py**: The terminal application to calculate PageRank step-by-step.
* **index.html**: The interactive web simulator.
* **Explanation_and_Notes.md**: The in-depth mathematical explanation and project history.
* **create_comprehensive_ppt.py** (Optional): The script used to generate the PPT.

---

## 2. Setting Up the Demonstration

Before you start presenting, get your terminal and browser ready so you can seamlessly switch to them during the live demo part.

### Step A: Terminal Demo Setup
1. Open a terminal or command prompt in the extracted project folder.
2. Ensure you have Python and NumPy installed (\pip install numpy\).
3. Keep the terminal open. You will run this command later:
   \python pagerank_demo.py\

### Step B: Web Simulator Setup
1. Open a second terminal window in the project folder.
2. Run a local web server to host the HTML file:
   \python -m http.server 8080\
3. Open your web browser and go to: **http://localhost:8080**
4. Keep this tab open and ready to show.

---

## 3. How to Present (Slide by Slide Points)

### The Problem (Pre-1998 Search Engines)
* Explain how early search engines (like Yahoo) only used **Keyword Density**.
* Explain the flaw: Spammers could hide the word 'Cars' 10,000 times invisibly and rank #1 without having good content.

### The Google Solution
* Explain that Larry Page and Sergey Brin treated a hyperlink as a **vote of confidence**.
* A link from a trusted site (Apple) is worth more than a link from a spam blog.
* This isn't just counting; it's a recursive problem solved perfectly by **Linear Algebra (Eigenvectors)**.

### The Mathematics (Matrices)
* **Adjacency Matrix (A)**: Shows the raw 1s and 0s of who links to who.
* **Stochastic Matrix (S)**: Shows probabilities. If a page has 2 outgoing links, each link has a 50% chance of being clicked. Columns sum to 1.
* **Google Matrix (G)**: Introduces the **Random Surfer Model** (Damping factor = 0.85). There's an 85% chance a user clicks a link, and a 15% chance they get bored and type a random URL. This removes zeros and ensures a unique solution.

### The Eigenvector (PageRank)
* Explain the equation: **G · v = 1 · v**
* We are looking for the steady-state vector \\ (the PageRank).
* Because the matrix is stochastic, the largest eigenvalue (\λ\) is exactly **1.0**.
* Explain that computing this eigenvector solves the ranking.

---

## 4. Live Demonstration

When you reach the Live Demo slides, switch out of PowerPoint to show the code working!

### Part 1: Terminal Code Demo
1. Switch to your terminal.
2. Run: \python pagerank_demo.py\
3. Type \1\ and hit Enter to use the default 4-node matrix.
4. **Explain to the examiner**: "Here we see the exact same 4 steps printed out. Adjacency, Stochastic, Google Matrix, and finally the Principal Eigenvector. CNN gets 42.92% because it receives links from everyone."
5. (Optional) You can run it again and choose \2\ to show you can input a custom matrix.

### Part 2: Web Simulator Demo
1. Switch to your web browser (**http://localhost:8080**).
2. **Explain to the examiner**: "This is a custom Vanilla Canvas simulator computing the mathematics live using Power Iteration."
3. **Showcase features**:
   * Drag the nodes around the screen.
   * Draw a new link (e.g., from Bing to Disney) and watch the Math matrices and rankings update instantly.
   * Add a new node to show the matrix dynamically expanding from 4x4 to 5x5.

---

## 5. Wrapping Up
* Mention that this exact math is what organized the early internet.
* Briefly note that today, these graph algorithms are also used in Social Networks (Twitter influence) and Fraud Detection (spotting suspicious network hubs).
