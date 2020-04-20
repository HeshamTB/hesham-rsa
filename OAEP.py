#From: https://stackoverflow.com/questions/39964383/implementation-of-i2osp-and-os2ip

def i2osp(x, xLen):
        if x >= 256**xLen:
            raise ValueError("integer too large")
        digits = []

        while x:
            digits.append(int(x % 256))
            x //= 256
        for i in range(xLen - len(digits)):
            digits.append(0)
        return digits[::-1]

def os2ip(X):
        xLen = len(X)
        X = X[::-1]
        x = 0
        for i in range(xLen):
            x += X[i] * 256**i
        return x

