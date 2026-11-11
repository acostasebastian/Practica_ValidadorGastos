"""Pruebas del punto de partida: aparcamiento (Q1, Q2) y entradas rechazadas (Q4)."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "gastos.py"
sys.path.insert(0, str(SCRIPT.parent))

from gastos import decidir  # noqa: E402

ERROR = {"estado": "error", "codigo": "entrada_invalida"}


def ejecutar(texto):
    """Invoca gastos.py con el mismo intérprete y envía la entrada como bytes UTF-8."""
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=texto.encode("utf-8"),
        capture_output=True,
        timeout=10,
    )


class DecisionAparcamientoTest(unittest.TestCase):
    """Q1 · Tecnología: pruebas unitarias de decidir()."""

    def test_2000_aprobado(self):
        esperado = {"estado": "aprobado", "centimos": 2000}
        self.assertEqual(decidir({"tipo": "aparcamiento", "centimos": 2000}), esperado)

    def test_2001_rechazado(self):
        esperado = {"estado": "rechazado", "centimos": 2001}
        self.assertEqual(decidir({"tipo": "aparcamiento", "centimos": 2001}), esperado)

    def test_importe_booleano_invalido(self):
        with self.assertRaises(ValueError):
            decidir({"tipo": "aparcamiento", "centimos": True})

    def test_importe_negativo_invalido(self):
        with self.assertRaises(ValueError):
            decidir({"tipo": "aparcamiento", "centimos": -100})


class ProcesoAparcamientoTest(unittest.TestCase):
    """Q2 · Negocio: interfaz completa por subprocess."""

    def test_2000_aprobado(self):
        proc = ejecutar('{"tipo":"aparcamiento","centimos":2000}')
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout), {"estado": "aprobado", "centimos": 2000})

    def test_2001_rechazado(self):
        proc = ejecutar('{"tipo":"aparcamiento","centimos":2001}')
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout), {"estado": "rechazado", "centimos": 2001})


class ProcesoRechazoTest(unittest.TestCase):
    """Q4 · Tecnología: entradas que el contrato ya rechaza."""

    def test_tamano_excesivo(self):
        base = '{"tipo":"aparcamiento","centimos":2000}'
        texto = base + " " * (4097 - len(base.encode("utf-8")))
        self.assertEqual(len(texto.encode("utf-8")), 4097)
        proc = ejecutar(texto)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout), ERROR)

    def test_campo_extra(self):
        proc = ejecutar('{"tipo":"aparcamiento","centimos":2000,"motivo":"reunión"}')
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout), ERROR)


if __name__ == "__main__":
    unittest.main()
