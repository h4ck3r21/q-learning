def merge_weights(w1, w2):
    for x, row in enumerate(w1):
        for y, item in enumerate(row):
            w1[x][y] = (w1[x][y] + w2[x][y])
    w2 = w1
