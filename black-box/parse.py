import ast


def _parse_matrix(m):
    # TODO CHANGE WRITING FUNCTION
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


def parse_qr():
    with open('./qr_decomposition/qr.txt', 'r') as fd:
        data = fd.read()
        cases = data.split('\n\n')
        cases = list(filter(None, cases))
        for i, case in enumerate(cases):
            lines = case.split('\n')
            m = _parse_matrix(lines[0])
            q = _parse_matrix(lines[1])
            r = _parse_matrix(lines[2])
            cases[i] = (m, q, r)
    return cases


def parse_diag():
    with open('./diag/diagonals.txt', 'r') as fd:
        data = fd.read()
        cases = data.split('\n\n')
        cases = list(filter(None, cases))
        for i, case in enumerate(cases):
            lines = case.split('\n')
            v = _parse_matrix(lines[0])
            m = _parse_matrix(lines[1])
            cases[i] = (v, m)

    return cases


def parse_cholesky():
    with open('./cholesky/cholesky.txt', 'r') as fd:
        data = fd.read()
        cases = data.split('\n\n')
        cases = list(filter(None, cases))
        for i, case in enumerate(cases):
            lines = case.split('\n')
            m = _parse_matrix(lines[0])
            ms = _parse_matrix(lines[1])
            cases[i] = (m, ms)

    return cases


def parse_charpoly():

    def _parse_expression(e):
        e = e.replace("x", "lambda")
        e = e.replace("^", "**")
        return "PurePoly(" + e + ", lambda, domain='ZZ')"

    with open('./charpoly/charpolies.txt', 'r') as fd:
        data = fd.read()
        cases = data.split('\n\n')
        cases = list(filter(None, cases))
        for i, case in enumerate(cases):
            lines = case.split('\n')
            m = _parse_matrix(lines[0])
            e = _parse_expression(lines[1])
            cases[i] = (m, e)

    return cases


def parse_removecolrow():
    with open('./remove_rowncol/colrow.txt', 'r') as fd:
        data = fd.read()
        cases = data.split('\n\n')
        cases = list(filter(None, cases))
        for i, case in enumerate(cases):
            lines = case.split('\n')
            m = _parse_matrix(lines[0])
            (j1, j2) = ast.literal_eval(lines[1])
            ms = _parse_matrix(lines[2])
            cases[i] = (m, j1-1, j2-1, ms)

    return cases
