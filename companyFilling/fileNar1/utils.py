def count_all_shares(allRows):
    total = 0
    for i in allRows:
        total += i.totalShares
    return total