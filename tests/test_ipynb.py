import sys
import subprocess
import tempfile

import nbformat


PY2 = sys.version_info[0] == 2

if PY2 is False:
    from io import StringIO


def _notebook_run(path):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        if PY2 is False:
            content = fout.read().decode('utf-8')
            xio = StringIO(content)
        else:
            xio = fout
        nb = nbformat.read(xio, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
              for output in cell["outputs"]
              if output.output_type == "error"]

    return nb, errors


def test_ipynb():
    if PY2:
        print("Ignored ipynb tests in python 2")
        pass
    else:
        nb, errors = _notebook_run('notebook/life_expectancy.ipynb')
        assert errors == []
