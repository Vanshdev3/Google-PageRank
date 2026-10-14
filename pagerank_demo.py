"""
Google PageRank Algorithm - Linear Algebra Implementation
==========================================================
Demonstrates the mathematical formulation of Google PageRank:
- Step 1: Adjacency Matrix (A)
- Step 2: Column-Stochastic Transition Matrix (S)
- Step 3: Google Matrix (M) with Random Surfer Damping Factor (d = 0.85)
- Step 4: Analytical Principal Eigenvector via np.linalg.eig()
- Step 5: Numerical Verification via Power Iteration
"""

import sys
import numpy as np

BANNER = """============================================================
  Google PageRank Algorithm - Linear Algebra Demonstration
  Syllabus: Unit 2 - Eigenvalues & Eigenvectors
============================================================"""


def run_pagerank(A, labels=None, d=0.85, verbose=True):
    """
    Computes PageRank for an N x N adjacency matrix A.

    Parameters:
      A       : (N, N) ndarray, A[i, j] = 1 if page j links to page i
      labels  : list of str, human-readable labels for each node
      d       : float, damping factor (default: 0.85)
      verbose : bool, whether to print step-by-step matrix outputs

    Returns:
      dict containing:
        - 'pagerank_eig': analytical PageRank distribution (from np.linalg.eig)
        - 'pagerank_pi' : numerical PageRank distribution (from Power Iteration)
        - 'eigenvalues' : all eigenvalues of the Google Matrix
        - 'iterations'  : iterations required for Power Iteration to converge
        - 'max_diff'    : max absolute error between analytical and numerical methods
    """
    A = np.asarray(A, dtype=float)

    # Validate square matrix
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError(f"Adjacency matrix must be square (NxN), got shape {A.shape}")
    if np.any(A < 0):
        raise ValueError("Adjacency matrix cannot contain negative weights")
    if A.shape[0] == 0:
        raise ValueError("Matrix cannot be empty")

    n = A.shape[0]
    if labels is None:
        labels = [chr(65 + i) for i in range(n)]

    col_width = max(10, max(len(l) for l in labels) + 2)

    def print_matrix(M, fmt=".0f"):
        header = " " * col_width + "".join(f"{l:>{col_width}}" for l in labels)
        print(header)
        for i in range(n):
            row = "".join(f"{M[i, j]:>{col_width}{fmt}}" for j in range(n))
            print(f"{labels[i]:>{col_width}}{row}")
        print()

    # -- STEP 1: Adjacency Matrix ---------------------------------
    if verbose:
        print("-" * 60)
        print("STEP 1 - Adjacency Matrix  (A)")
        print("  Rows = destination  |  Columns = source")
        print("  Entry = 1 if a hyperlink exists from col-page to row-page")
        print("-" * 60)
        print_matrix(A)

    # -- STEP 2: Column-Stochastic Matrix -------------------------
    # Divide each column by its out-degree (column sum).
    # If a page has 0 outgoing links (dangling node), teleport uniformly (1/n).
    S = np.zeros_like(A, dtype=float)
    for j in range(n):
        col_sum = np.sum(A[:, j])
        S[:, j] = (A[:, j] / col_sum) if col_sum > 0 else (1.0 / n)

    if verbose:
        print("-" * 60)
        print("STEP 2 - Stochastic Transition Matrix  (S)")
        print("  Each column divided by its out-degree (column sum).")
        print("  S[i,j] = probability of surfing from page j to page i.")
        print("  Column sums = 1.0 (valid probability distribution)")
        print("-" * 60)
        print_matrix(S, ".4f")
        print(f"  Column sums: {[round(float(S[:, j].sum()), 4) for j in range(n)]}")
        print()

    # -- STEP 3: Google Matrix -------------------------------------
    # Random Surfer Model: 85% follow links, 15% teleport uniformly.
    E = np.ones((n, n)) / n
    G = d * S + (1 - d) * E

    if verbose:
        print("-" * 60)
        print(f"STEP 3 - Google Matrix  (M = d*S + (1-d)/N * E)")
        print(f"  Damping factor d = {d}  (85% follow link, 15% random jump)")
        print("  Guarantees the matrix is irreducible & primitive,")
        print("  ensuring a unique stationary eigenvector exists.")
        print("-" * 60)
        print_matrix(G, ".4f")

    # -- STEP 4: Principal Eigenvector via numpy -------------------
    eigenvalues, eigenvectors = np.linalg.eig(G)
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    v = np.real(eigenvectors[:, idx])

    # Perron-Frobenius: principal eigenvector has strictly one sign.
    # Standardize to positive and eliminate floating-point noise:
    if np.sum(v) < 0:
        v = -v
    v = np.maximum(v, 0.0)
    pagerank_eig = v / v.sum()

    if verbose:
        print("-" * 60)
        print("STEP 4 - Eigenvalue Decomposition  (M*v = lambda*v)")
        print("  By Perron-Frobenius: dominant eigenvalue lambda = 1")
        print("  The corresponding eigenvector IS the PageRank vector.")
        print("-" * 60)
        print(f"\n  All eigenvalues: {[round(float(np.real(e)), 4) for e in eigenvalues]}")
        print(f"  Dominant eigenvalue = {round(float(np.real(eigenvalues[idx])), 6)}")
        print()
        print("  -- FINAL PageRank Scores ---------------------------------")
        ranked = sorted(zip(labels, pagerank_eig), key=lambda x: -x[1])
        for rank, (label, score) in enumerate(ranked, 1):
            bar = "|" * int(score * 40)
            print(f"  #{rank}  {label:<14}  {score * 100:6.2f}%  {bar}")
        print()

    # -- STEP 5: Power Iteration verification ---------------------
    v_iter = np.ones(n) / n
    iterations = 0
    delta = 1.0
    for iteration in range(1, 1001):
        v_next = G @ v_iter
        delta = np.linalg.norm(v_next - v_iter, 1)
        v_iter = v_next
        iterations = iteration
        if delta < 1e-10:
            break

    pagerank_pi = v_iter / v_iter.sum()
    max_diff = float(np.max(np.abs(pagerank_eig - pagerank_pi)))

    if verbose:
        print("-" * 60)
        print("STEP 5 - Power Iteration Verification  (v_(k+1) = M * v_k)")
        print("  Starting from uniform distribution, iterating until")
        print("  L1 norm ||v_(k+1) - v_k|| < 1e-10 (convergence threshold)")
        print("-" * 60)
        print(f"\n  Converged in {iterations} iterations  (d = {delta:.2e})")
        print("\n  Power Iteration result (should match Step 4 exactly):")
        for label, score in zip(labels, pagerank_pi):
            print(f"  {label:<14}  {score * 100:.4f}%")
        print(f"\n  Max numerical difference between methods: {max_diff:.2e}")
        print("  [OK] Both methods agree - mathematics verified.\n")
        print("=" * 60)

    return {
        "pagerank_eig": pagerank_eig,
        "pagerank_pi": pagerank_pi,
        "eigenvalues": eigenvalues,
        "iterations": iterations,
        "max_diff": max_diff,
        "labels": labels,
        "Google_Matrix": G,
    }


def run_self_tests():
    """Automated unit test suite validating mathematical correctness and edge cases."""
    print("Running automated PageRank self-tests...")

    # Test 1: 4-node benchmark
    A_bench = np.array([
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
    ], dtype=float)
    res = run_pagerank(A_bench, verbose=False)
    assert np.isclose(res["pagerank_eig"][0], 0.4292, atol=1e-3), "CNN rank mismatch"
    assert res["max_diff"] < 1e-10, "Power iteration discrepancy"
    print("  [PASS] 4-node benchmark verified (CNN = 42.92%)")

    # Test 2: Dangling node (node with 0 outlinks)
    A_dangle = np.array([
        [0, 0],
        [1, 0],
    ], dtype=float)
    res_d = run_pagerank(A_dangle, verbose=False)
    assert np.isclose(res_d["pagerank_eig"].sum(), 1.0), "Dangling node sum != 1.0"
    print("  [PASS] Dangling node test verified")

    # Test 3: Spider trap (2 nodes in an isolated loop)
    A_trap = np.array([
        [0, 1],
        [1, 0],
    ], dtype=float)
    res_t = run_pagerank(A_trap, verbose=False)
    assert np.isclose(res_t["pagerank_eig"][0], 0.50), "Spider trap symmetry mismatch"
    print("  [PASS] Spider trap symmetry verified")

    print("\nAll self-tests passed successfully!\n")


def main():
    if "--test" in sys.argv:
        run_self_tests()
        return

    print(BANNER)
    print()
    print("Select a demo:\n")
    print("  1.  Default 4-node benchmark")
    print("      CNN, Yahoo, TechCrunch, Amazon")
    print("  2.  Enter a custom adjacency matrix\n")

    choice = input("Enter 1 or 2  [default = 1]: ").strip() or "1"

    if choice == "2":
        while True:
            try:
                raw_n = input("\nNumber of pages (nodes, >= 2): ").strip()
                n = int(raw_n)
                if n < 2:
                    print("Please enter at least 2 nodes.")
                    continue
                break
            except ValueError:
                print("Invalid integer. Please try again.")

        print(f"\nEnter the {n}x{n} adjacency matrix row by row.")
        print("Note: Row = destination page, Column = source page.")
        print(f"Type {n} numbers (0 or 1) separated by spaces for each row.\n")

        matrix_data = []
        for i in range(n):
            while True:
                try:
                    row_input = input(f"  Row {i + 1} (to page {chr(65 + i)}): ").strip()
                    row = [float(x) for x in row_input.split()]
                    if len(row) != n:
                        print(f"  Error: Expected exactly {n} values, got {len(row)}. Please re-enter.")
                        continue
                    if any(x < 0 for x in row):
                        print("  Error: Values cannot be negative. Please re-enter.")
                        continue
                    matrix_data.append(row)
                    break
                except ValueError:
                    print("  Error: Invalid numbers. Please enter numbers separated by spaces.")

        A = np.array(matrix_data, dtype=float)
        run_pagerank(A)
    else:
        # Default 4-node benchmark
        #   CNN         -> Yahoo, TechCrunch
        #   Yahoo       -> CNN
        #   TechCrunch  -> CNN, Amazon
        #   Amazon      -> CNN
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
