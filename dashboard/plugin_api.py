"""Public Desktop/dashboard REST mount; scoped by the host's profile middleware."""
import importlib
import importlib.util
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter()


def _adapter():
    from hermes_constants import get_hermes_home
    # Dashboard APIs are loaded as standalone modules by Hermes. Import our
    # package under a unique name, never mutate sys.path or shadow host modules.
    name = "hermes_handoff_desktop_package"
    if name not in sys.modules:
        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location(name, root / "__init__.py", submodule_search_locations=[str(root)])
        if spec is None or spec.loader is None:
            raise ValueError("plugin package unavailable")
        package = importlib.util.module_from_spec(spec)
        sys.modules[name] = package
        spec.loader.exec_module(package)
    native = importlib.import_module(name + ".server.hermes_handoff")
    opening = importlib.import_module(name + ".server.handoff_open")
    desktop = importlib.import_module(name + ".server.handoff_desktop")
    return desktop.HandoffDesktop(opening.HandoffOpening(native.HermesHandoff(get_hermes_home())))


@router.post("/opening")
def opening(body: dict):
    try:
        return _adapter().handle(body)
    except (ValueError, OSError):
        raise HTTPException(status_code=409, detail="Handoff refused. Check prepared attempt, exact origin/profile/workspace and tool policy; uncertain starts require manual recovery.") from None
