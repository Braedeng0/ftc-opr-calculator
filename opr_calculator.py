import numpy as np

def calculate_opr(matches: np.ndarray, scores: np.ndarray) -> np.ndarray:
    '''
    Calculate the OPR (Offensive Power Rating) for each team based on match scores.

    Parameters:
    matches (array-like): A 2D array where each row represents a match and each column represents a team.
    scores (array-like): A 1D array (column vector) where each element represents the score of the corresponding match.

    Returns:
    opr (array-like): A 1D array where each element represents the OPR of the corresponding team.

    Raises:
    ValueError: If the number of matches does not match the number of scores.
    '''
    # Make sure matches and scores are numpy arrays
    matches = np.array(matches)
    scores = np.array(scores)

    # Check if matches and scores have the same number of rows
    if matches.shape[0] != scores.shape[0]:
        raise ValueError("The number of matches must match the number of scores.")
    
    # Use the least squares method to solve for OPR
    A = matches
    b = scores.reshape(-1, 1)  # Reshape scores to be a column vector

    # Solve for OPR using numpy's least squares method
    opr, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

    # Flatten the result to get a 1D array
    opr = opr.flatten()
    return opr

# Example usage
if __name__ == "__main__":
    matches = [
        [1, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
    ]
    scores = [10, 13, 7, 15, 10]
    opr = calculate_opr(matches, scores)
    print("OPR:", opr)

    # Expected output:
    # OPR: [ 7.75 2.25 5. 7.5]
