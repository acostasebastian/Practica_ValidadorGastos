"""Q2 · Negocio y Q4 · Tecnología: pruebas de la interfaz completa por subprocess."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "gastos.py"
ERROR = {"estado": "error", "codigo": "entrada_invalida"}
MOTIVO_SENSIBLE = "DNI 00000000T tarjeta 4111111111111111 (ficticio)"


def ejecutar(entrada):
    if isinstance(entrada, dict):
        entrada = json.dumps(entrada, ensure_ascii=False)
    if isinstance(entrada, str):
        entrada = entrada.encode("utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)], input=entrada, capture_output=True, timeout=10
    )
    return proc


class TaxiInterfazTest(unittest.TestCase):
    """Q2: taxi con motivo aprobado/rechazado y sin motivo error 2."""

    def test_4000_con_motivo_aprobado(self):
        proc = ejecutar({"tipo": "taxi", "centimos": 4000, "motivo": "Visita a cliente"})
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout), {"estado": "aprobado", "centimos": 4000})

    def test_4001_con_motivo_rechazado(self):
        proc = ejecutar({"tipo": "taxi", "centimos": 4001, "motivo": "Visita a cliente"})
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout), {"estado": "rechazado", "centimos": 4001})

    def test_sin_motivo_error(self):
        proc = ejecutar({"tipo": "taxi", "centimos": 4000})
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout), ERROR)


class RobustezInterfazTest(unittest.TestCase):
    """Q4: tamaño excedido y confidencialidad del motivo."""

    def test_entrada_mayor_de_4096_bytes(self):
        base = {"tipo": "taxi", "centimos": 100, "motivo": ""}
        relleno = 4097 - len(json.dumps(base).encode("utf-8"))
        entrada = json.dumps({**base, "motivo": "x" * relleno}).encode("utf-8")
        self.assertEqual(len(entrada), 4097)
        proc = ejecutar(entrada)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout), ERROR)
        self.assertEqual(proc.stderr, b"")

    def test_motivo_sensible_no_aparece_en_error(self):
        proc = ejecutar({"tipo": "taxi", "centimos": -1, "motivo": MOTIVO_SENSIBLE})
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout), ERROR)
        for salida in (proc.stdout, proc.stderr):
            self.assertNotIn(b"00000000T", salida)
            self.assertNotIn(b"4111111111111111", salida)

    def test_motivo_sensible_no_aparece_en_respuesta_valida(self):
        proc = ejecutar({"tipo": "taxi", "centimos": 100, "motivo": MOTIVO_SENSIBLE})
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout), {"estado": "aprobado", "centimos": 100})
        for salida in (proc.stdout, proc.stderr):
            self.assertNotIn(b"00000000T", salida)
            self.assertNotIn(b"4111111111111111", salida)


if __name__ == "__main__":
    unittest.main()
