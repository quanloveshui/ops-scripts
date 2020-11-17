#生成随机数



def random_code(length):
    codes = []
    for i in range(length):
        num = random.randrange(length)
        if i == num:
            code = random.randint(0,9)
            codes.append(str(code))
        else:
            capital_codes = list(range(65,91))
            capital_codes.extend(list(range(97,123)))
            tem_code = random.choice(capital_codes)
            codes.append(chr(tem_code))
    rand_code = "".join(codes)
    return rand_code
