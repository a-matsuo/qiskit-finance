# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""The European Call Option Expected Value."""
from typing import Tuple

from qiskit.circuit import QuantumCircuit
from qiskit.algorithms.amplitude_estimators import EstimationProblem
from qiskit_finance.applications.estimation.estimation_application import EstimationApplication
from qiskit_finance.circuit.library.payoff_functions.european_call_delta_objective \
    import EuropeanCallDeltaObjective


class EuropeanCallDelta(EstimationApplication):
    """The European Call Option Delta.
    Evaluates the variance for a European call option given an uncertainty model.
    The payoff function is f(S, K) = max(0, S - K) for a spot price S and strike price K.
    """

    def __init__(self, num_state_qubits: int, strike_price: float, bounds: Tuple[float, float],
                 uncertainty_model: QuantumCircuit) -> None:
        """
        Args:
            num_state_qubits: The number of qubits used to encode the random variable.
            strike_price: strike price of the European option
            bounds: The bounds of the discretized random variable.
            uncertainty_model: A circuit for encoding a problem distribution
        """
        self._european_call_delta = EuropeanCallDeltaObjective(num_state_qubits=num_state_qubits,
                                                               strike_price=strike_price,
                                                               bounds=bounds)
        self._european_call = self._european_call_delta.compose(uncertainty_model, front=True)
        self._num_state_qubits = uncertainty_model.num_qubits

    def to_estimation_problem(self):
        problem = EstimationProblem(state_preparation=self._european_call,
                                    objective_qubits=[self._num_state_qubits],
                                    post_processing=self._european_call_delta.post_processing)
        return problem