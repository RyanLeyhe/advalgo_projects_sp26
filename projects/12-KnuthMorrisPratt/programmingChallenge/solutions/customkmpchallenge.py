import sys
from typing import Sequence

def buildTable(pattern: Sequence) -> list[int]:
    """Builds the fallback table for KMP."""
    m = len(pattern)
    table = [0] * (m + 1)
    pos = 1 
    cnd = 0 
    table[0] = -1 

    while (pos < m):
        if (pattern[pos] == pattern[cnd]):
            table[pos] = table[cnd]
        else:
            table[pos] = cnd
            while (cnd >= 0) and (pattern[pos] != pattern[cnd]):
                cnd = table[cnd]
        pos += 1
        cnd += 1
    
    table[pos] = cnd
    return table

def kmpSearch(text: Sequence, pattern: Sequence) -> list[int]:
    """Searches 'text' for all occurrences of 'pattern'."""
    if (not pattern) or (not text):
        return []
    
    table = buildTable(pattern)
    matches = []
    j = 0 
    k = 0 

    while (j < len(text)):
        if (pattern[k] == text[j]):
            k += 1
            j += 1
            if (k == len(pattern)):
                matches.append(j - k)
                k = table[k]
        else:
            k = table[k]
            if (k < 0):
                j += 1
                k += 1
    
    return matches


def find_2d_pattern(page_matrix: list[str], pattern_matrix: list[str]) -> list[tuple[int, int]]:
    """
    Finds all occurrences of a 2D pattern inside a larger 2D page matrix.
    Returns a list of (row, col) coordinates where the top-left of the pattern appears.
    """
    if not page_matrix or not pattern_matrix:
        return []

    R, C = len(page_matrix), len(page_matrix[0]) if page_matrix else 0
    r, c = len(pattern_matrix), len(pattern_matrix[0]) if pattern_matrix else 0

    # If pattern is larger than the page, can't exist
    if r > R or c > C:
        return []

    # Map unique rows in the pattern to integer "states" to stop redundant KMP searches if pattern has repeating rows
    unique_pattern_rows = list(set(pattern_matrix))
    row_to_state = {row: idx for idx, row in enumerate(unique_pattern_rows)}
    
    # 1D list of integers representing the patterns row structure
    target_vertical_pattern = [row_to_state[row] for row in pattern_matrix]
    
    # state_matrix[i][j] will hold a state ID if a pattern row starts at page_matrix[i][j], else -1
    state_matrix = [[-1] * C for _ in range(R)]
    
    # HORIZONTAL KMP
    for unique_row in unique_pattern_rows:
        state_id = row_to_state[unique_row]
        
        for i in range(R):
            matches = kmpSearch(page_matrix[i], unique_row)
            for j in matches:
                state_matrix[i][j] = state_id
                
    final_matches = []
    
    # VERTICAL KMP
    for j in range(C - c + 1):
        
        column_data = [state_matrix[i][j] for i in range(R)]
        col_matches = kmpSearch(column_data, target_vertical_pattern)
        
        for i in col_matches:
            final_matches.append((i, j))
            
    return final_matches


if __name__ == "__main__":
    input = sys.stdin.readline
    R, C = map(int, input().split())

    page_matrix = [input().strip() for _ in range(R)]
    r, c = map(int, input().split())
    pattern_matrix = [input().strip() for _ in range(r)]

    matches = find_2d_pattern(page_matrix, pattern_matrix)

    matches.sort(key=lambda rc: (rc[1], rc[0]))
    print(len(matches))
    for row, col in matches:
        print(row, col)
