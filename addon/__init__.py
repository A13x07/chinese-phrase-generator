# __init__.py
from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo

def on_generate():
    # Fires only on click, so a collection is loaded — mw.col is safe here.
    # Pipeline trigger goes here later.
    showInfo("Chinese Phrase Generator: skeleton wired up.")

def setup_menu():
    action = QAction("Generate practice phrases", mw)
    action.triggered.connect(on_generate)
    mw.form.menuTools.addAction(action)

setup_menu()