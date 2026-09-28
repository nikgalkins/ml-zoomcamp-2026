import os
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager

root = Path(__file__).resolve().parent.parent
runtime = root / ".runtime"
os.environ["JUPYTER_RUNTIME_DIR"] = str(runtime / "jupyter-runtime")
os.environ["IPYTHONDIR"] = str(runtime / "ipython")
kernel_dir = runtime / "kernels" / "python3"
kernel_dir.mkdir(parents=True, exist_ok=True)
(kernel_dir / "kernel.json").write_text(
    __import__("json").dumps({
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Python 3", "language": "python"
    }), encoding="utf-8"
)

path = root / "01_intro_homework.ipynb"
nb = nbformat.read(path, as_version=4)
client = NotebookClient(
    nb, timeout=120, kernel_name="python3",
    resources={"metadata": {"path": str(root)}},
    kernel_manager_class=__import__("jupyter_client").KernelManager,
)
client.create_kernel_manager()
client.km.kernel_spec_manager = KernelSpecManager(kernel_dirs=[str(runtime / "kernels")])
client.execute()
nbformat.validate(nb)
nbformat.write(nb, path)

code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
assert all(cell.execution_count is not None for cell in code_cells)
assert not any(output.output_type == "error" for cell in code_cells for output in cell.outputs)
print(f"Executed and saved {len(code_cells)} code cells without errors.")
for cell in code_cells:
    for output in cell.outputs:
        if output.output_type == "stream":
            print(output.text, end="")
