from qat.qpus import QPUHandler
from pytket.backends import Backend
from qat.core import Job, Result
from qat.interop.qiskit import qlm_to_qiskit
from pytket.extensions.qiskit import qiskit_to_tk
from pytket.utils import expectation_from_counts
from pytket.circuit.display import render_circuit_jupyter


def get_pytket_qpu_handler(backend: Backend, max_shots:int = 10000) -> QPUHandler:

    class PytketQPUHandler(QPUHandler):

        def submit_job(self, job: Job) -> Result:

            qiskit_circuit = qlm_to_qiskit(job.circuit)
            pytket_circuit = qiskit_to_tk(qiskit_circuit)
            pytket_circuit = backend.get_compiled_circuit(
                circuit=pytket_circuit,
                optimisation_level=2,
            )

            n_shots = job.nbshots
            if n_shots == 0: n_shots = max_shots

            pytket_result = backend.run_circuit(
                circuit=pytket_circuit,
                n_shots=n_shots,
            )

            qlm_result = Result()
            qlm_result.value = expectation_from_counts(pytket_result.get_counts())

            return qlm_result

    return PytketQPUHandler()
