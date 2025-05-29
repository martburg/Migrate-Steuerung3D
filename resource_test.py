import importlib

modules_to_test = [
    # Standard + External
    "collections", "copy", "ctypes", "datetime", "hashlib", "logging", "logging.handlers",
    "math", "os", "random", "socket", "sys", "time",
    "wx", "numpy", "scipy.integrate", "scipy.interpolate",

    # Panda3D
    "direct.showbase.ShowBase", "direct.directbase", "direct.showutil.Rope",
    "direct.task", "direct.gui.OnscreenText", "direct.tkpanels.Inspector",

    # Local project modules
    "CameraHandlerClass", "CameraHandlerClassA", "GrenzVel",
]

def test_imports():
    results = {}
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            results[module] = "OK"
        except Exception as e:
            results[module] = f"ERROR: {type(e).__name__}: {e}"
    return results

if __name__ == "__main__":
    results = test_imports()
    for mod, status in results.items():
        print(f"{mod:<35} {status}")
