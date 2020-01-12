import ast


def _parse_matrix(m):
    m = m.replace(';', ',')
    m = ast.literal_eval(m)
    return m


def parse_zeros_ones_n_eye(path):
    with open(path, 'r') as fd:
        data = fd.read()
        cases = data.split('\n\n')
        cases = list(filter(None, cases))
        for i, case in enumerate(cases):
            lines = case.split('\n')
            v = tuple(map(int, lines[0].split(',')))
            m = _parse_matrix(lines[1])
            cases[i] = (v, m)
    return cases


def parse_determinants():
    with open('./det/determinants.txt', 'r') as fd:
        data = fd.read()
        cases = data.split('\n\n')
        cases = list(filter(None, cases))
        for i, case in enumerate(cases):
            lines = case.split('\n')
            m = _parse_matrix(lines[0])
            v = float(lines[1])
            cases[i] = (m,  v)

    return cases


def parse_eigenvalues():
    with open('./eigenvalues/eigenvals.txt', 'r') as fd:
        data = fd.read()
        cases = data.split('\n\n')
        cases = list(filter(None, cases))
        for i, case in enumerate(cases):
            lines = case.split('\n')
            m = _parse_matrix(lines[0])
            eigen_vals = [x.replace('+ -', '- ') for x in lines[1:]]
            eigen_vals = [x.replace(' + 0*I', '') for x in eigen_vals]
            cases[i] = (m,  eigen_vals)

    return cases
