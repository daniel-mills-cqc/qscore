from qat.qpus import QPUHandler
from pytket.backends import Backend
from qat.core import Job, Result
from qat.interop.qiskit import qlm_to_qiskit
from pytket.extensions.qiskit import qiskit_to_tk


def get_pytket_qpu_handler(backend: Backend, max_shots:int = 10) -> QPUHandler:

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
            for shot in pytket_result.get_shots():
                qlm_result.add_sample(self.shot_to_int(shot))

            return qlm_result

        @staticmethod
        def shot_to_int(shot: list[int]) -> int:
            index = 0
            for bit in shot:
                index <<= 1
                index += bit
            return index

    return PytketQPUHandler()
