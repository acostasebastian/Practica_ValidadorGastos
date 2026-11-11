"""Q1 · Tecnología: pruebas unitarias de decidir()."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gastos import decidir  # noqa: E402


class AparcamientoTest(unittest.TestCase):
    def test_2000_aprobado(self):
        self.assertEqual(
            decidir({"tipo": "aparcamiento", "centimos": 2000}),
            {"estado": "aprobado", "centimos": 2000},
        )

    def test_2001_rechazado(self):
        self.assertEqual(
            decidir({"tipo": "aparcamiento", "centimos": 2001}),
            {"estado": "rechazado", "centimos": 2001},
        )

    def test_importe_booleano_invalido(self):
        with self.assertRaises(ValueError):
            decidir({"tipo": "aparcamiento", "centimos": True})

    def test_importe_negativo_invalido(self):
        with self.assertRaises(ValueError):
            decidir({"tipo": "aparcamiento", "centimos": -100})

    def test_motivo_no_permitido(self):
        with self.assertRaises(ValueError):
            decidir({"tipo": "aparcamiento", "centimos": 100, "motivo": "x"})


class TaxiTest(unittest.TestCase):
    def test_4000_aprobado(self):
        self.assertEqual(
            decidir({"tipo": "taxi", "centimos": 4000, "motivo": "Cliente"}),
            {"estado": "aprobado", "centimos": 4000},
        )

    def test_4001_rechazado(self):
        self.assertEqual(
            decidir({"tipo": "taxi", "centimos": 4001, "motivo": "Cliente"}),
            {"estado": "rechazado", "centimos": 4001},
        )

    def test_motivo_invalido(self):
        casos = [
            {"tipo": "taxi", "centimos": 100},
            {"tipo": "taxi", "centimos": 100, "motivo": ""},
            {"tipo": "taxi", "centimos": 100, "motivo": "   "},
            {"tipo": "taxi", "centimos": 100, "motivo": 123},
            {"tipo": "taxi", "centimos": 100, "motivo": "a" * 201},
        ]
        for solicitud in casos:
            with self.subTest(solicitud=solicitud), self.assertRaises(ValueError):
                decidir(solicitud)

    def test_motivo_200_caracteres_valido(self):
        self.assertEqual(
            decidir({"tipo": "taxi", "centimos": 100, "motivo": "a" * 200})["estado"],
            "aprobado",
        )

    def test_importe_booleano_invalido(self):
        with self.assertRaises(ValueError):
            decidir({"tipo": "taxi", "centimos": True, "motivo": "Cliente"})


if __name__ == "__main__":
    unittest.main()
