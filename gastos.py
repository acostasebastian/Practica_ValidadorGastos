import json
import sys
REGLAS = {
    "aparcamiento": ({"tipo", "centimos"}, 2000),
    "taxi": ({"tipo", "centimos", "motivo"}, 4000),
}
MAX_MOTIVO = 200
def decidir(solicitud):
    if not isinstance(solicitud, dict):
        raise ValueError()
    regla = REGLAS.get(solicitud.get("tipo")) if isinstance(solicitud.get("tipo"), str) else None
    if regla is None:
        raise ValueError()
    campos, limite = regla
    if set(solicitud) != campos:
        raise ValueError()
    centimos = solicitud["centimos"]
    if type(centimos) is not int or centimos <= 0:
        raise ValueError()
    if "motivo" in campos:
        motivo = solicitud["motivo"]
        if not isinstance(motivo, str) or not motivo.strip() or len(motivo) > MAX_MOTIVO:
            raise ValueError()
    estado = "aprobado" if centimos <= limite else "rechazado"
    return {"estado": estado, "centimos": centimos}
def main():
    datos = sys.stdin.buffer.read(4097)
    try:
        if len(datos) > 4096:
            raise ValueError()
        resultado = decidir(json.loads(datos.decode("utf-8")))
    except (ValueError, RecursionError):
        print(json.dumps({"estado": "error", "codigo": "entrada_invalida"}))
        return 2
    print(json.dumps(resultado))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
