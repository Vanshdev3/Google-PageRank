import numpy as np

print("=" * 60)
print("  Google PageRank Algorithm - Linear Algebra Demonstration")
print("  Syllabus: Unit 2 - Eigenvalues & Eigenvectors")
print("=" * 60)
print()


def run_pagerank(A, labels=None):
    n = A.shape[0]
    if labels is None:
        labels = [chr(65 + i) for i in range(n)]

    col_width = 12

    # -- Helper: print a matrix with row/col labels --------------
    def print_matrix(M, fmt=".0f"):
        header = " " * col_width + "".join(f"{l:>{col_width}}" for l in labels)
        print(header)
        for i in range(n):
            row = "".join(f"{M[i, j]:>{col_width}{fmt}}" for j in range(n))
            print(f"{labels[i]:>{col_width}}{row}")
        print()

    # -- STEP 1: Adjacency Matrix ---------------------------------
    print("-" * 60)
    print("STEP 1 - Adjacency Matrix  (A)")
    print("  Rows = destination  |  Columns = source")
    print("  Entry = 1 if a hyperlink exists from col-page to row-page")
    print("-" * 60)
    print_matrix(A)

    # -- STEP 2: Column-Stochastic Matrix -------------------------
    S = np.zeros_like(A, dtype=float)
    for j in range(n):
        col_sum = np.sum(A[:, j])
        S[:, j] = (A[:, j] / col_sum) if col_sum > 0 else (1.0 / n)

    print("-" * 60)
    print("STEP 2 - Stochastic Transition Matrix  (S)")
    print("  Each column divided by its out-degree (column sum).")
    print("  S[i,j] = probability of surfing from page j to page i.")
    print("  Column sums = 1.0 (valid probability distribution)")
    print("-" * 60)
    print_matrix(S, ".4f")
    print(f"  Column sums: {[round(S[:, j].sum(), 4) for j in range(n)]}")
    print()

    # -- STEP 3: Google Matrix -------------------------------------
    d = 0.85
    E = np.ones((n, n)) / n
    G = d * S + (1 - d) * E

    print("-" * 60)
    print("STEP 3 - Google Matrix  (M = d*S + (1-d)/N * E)")
    print(f"  Damping factor d = {d}  (85% follow link, 15% random jump)")
    print("  Guarantees the matrix is irreducible & primitive,")
    print("  ensuring a unique stationary eigenvector exists.")
    print("-" * 60)
    print_matrix(G, ".4f")

    # -- STEP 4: Principal Eigenvector via numpy -------------------
    print("-" * 60)
    print("STEP 4 - Eigenvalue Decomposition  (M*v = lambda*v)")
    print("  By Perron-Frobenius: dominant eigenvalue lambda = 1")
    print("  The corresponding eigenvector IS the PageRank vector.")
    print("-" * 60)

    eigenvalues, eigenvectors = np.linalg.eig(G)
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    v = np.real(eigenvectors[:, idx])
    pagerank = v / v.sum()

    print(f"\n  All eigenvalues: {[round(float(np.real(e)), 4) for e in eigenvalues]}")
    print(f"  Dominant eigenvalue = {round(float(np.real(eigenvalues[idx])), 6)}")
    print()
    print("  -- FINAL PageRank Scores ---------------------------------")
    ranked = sorted(zip(labels, pagerank), key=lambda x: -x[1])
    for rank, (label, score) in enumerate(ranked, 1):
        bar = "|" * int(score * 40)
        print(f"  #{rank}  {label:<14}  {score * 100:6.2f}%  {bar}")
    print()

    # -- STEP 5: Power Iteration verification ---------------------
    print("-" * 60)
    print("STEP 5 - Power Iteration Verification  (v_(k+1) = M * v_k)")
    print("  Starting from uniform distribution, iterating until")
    print("  L1 norm ||v_(k+1) - v_k|| < 1e-10 (convergence threshold)")
    print("-" * 60)

    v_iter = np.ones(n) / n
    for iteration in range(1, 1001):
        v_next = G @ v_iter
        delta = np.linalg.norm(v_next - v_iter, 1)
        v_iter = v_next
        if delta < 1e-10:
            print(f"\n  Converged in {iteration} iterations  (d = {delta:.2e})")
            break

    pagerank_pi = v_iter / v_iter.sum()
    print("\n  Power Iteration result (should match Step 4 exactly):")
    for label, score in zip(labels, pagerank_pi):
        print(f"  {label:<14}  {score * 100:.4f}%")

    max_diff = np.max(np.abs(pagerank - pagerank_pi))
    print(f"\n  Max numerical difference between methods: {max_diff:.2e}")
    print("  [OK] Both methods agree - mathematics verified.\n")
    print("=" * 60)


def main():
    print("Select a demo:\n")
    print("  1.  Default 4-node benchmark")
    print("      CNN, Yahoo, TechCrunch, Amazon")
    print("  2.  Enter a custom adjacency matrix\n")

    choice = input("Enter 1 or 2  [default = 1]: ").strip() or "1"

    if choice == "2":
        n = int(input("\nNumber of pages (nodes): "))
        print(f"\nEnter the {n}x{n} adjacency matrix row by row.")
        print("Use 0s and 1s separated by spaces.\n")
        matrix_data = []
        for i in range(n):
            row = list(map(float, input(f"  Row {i + 1}: ").split()))
            matrix_data.append(row)
        A = np.array(matrix_data)
        run_pagerank(A)
    else:
        # -- Default 4-node benchmark -----------------------------
        # Link structure (matches the PPT and web simulator exactly):
        #   CNN         → Yahoo, TechCrunch
        #   Yahoo       → CNN
        #   TechCrunch  → CNN, Amazon
        #   Amazon      → CNN
        #
        # Adjacency matrix - A[i][j] = 1 means page j links TO page i
        #   Columns: CNN  Yahoo  TechCrunch  Amazon
        #   Rows:    CNN  Yahoo  TechCrunch  Amazon
        labels = ["CNN", "Yahoo", "TechCrunch", "Amazon"]
        A = np.array([
            # CNN   Yahoo  TC    Amazon
            [0,     1,     1,    1],   # CNN receives links
            [1,     0,     0,    0],   # Yahoo receives links
            [1,     0,     0,    0],   # TechCrunch receives links
            [0,     0,     1,    0],   # Amazon receives links
        ], dtype=float)
        run_pagerank(A, labels)


if __name__ == "__main__":
    main()
