from qat.qscore.benchmark import QScore
from qat.plugins import ScipyMinimizePlugin
from pytket_qpu_handler import get_pytket_qpu_handler
from pytket.extensions.qiskit import AerBackend

QPU = ScipyMinimizePlugin(method="COBYLA", tol=1e-4, options={"maxiter": 300}) | get_pytket_qpu_handler(AerBackend())

benchmark = QScore(QPU, size_limit=10, depth=1)
benchmark.run()
