# Task 12 — Anki Add-on Scaffold

## The task
Create a minimal Anki add-on that loads inside Anki and registers a menu item
under Tools, as the entry point for the existing phrase-generation pipeline.

## Why it's needed
The pipeline currently requires two manual steps: exporting vocabulary from
Anki as a .txt file, and importing the generated phrases back in. Running
inside Anki removes both — the add-on reads the collection directly and
writes new notes back to it.

An add-on does not run in the project's virtual environment. It runs inside
Anki's own bundled Python, which cannot see pip-installed packages. This
changes the dependency strategy for every later task, so the first task is to
confirm the add-on loads at all before any pipeline code is moved across.

## What was done
- Created an `addon/` folder in the repository to hold the add-on source,
  keeping it separate from the standalone pipeline, which still runs.
- Added `__init__.py`, the file Anki looks for when loading an add-on folder.
  A folder without one is ignored.
- Registered a "Generate practice phrases" action on the Tools menu.
- Linked `addon/` into Anki's `addons21` folder with a directory junction, so
  the add-on runs from the repository and edits take effect on the next
  restart without copying files between folders.
- Excluded Anki's generated `meta.json`, `__pycache__/` and `user_files/`
  from version control, as the junction causes Anki to write them into the
  repository.

## Design decisions
**Menu registration at import, work in the handler.** Anki executes an add-on's
module body at startup, before any profile or collection is loaded, so `mw.col`
does not exist at that point. Registering the menu there is safe; the pipeline
call sits inside `on_generate()`, which runs only on click, by which time a
collection is open.

**Qt imports go through `aqt.qt`.** QAction moved from QtWidgets to QtGui in
Qt6. Importing it from Anki's `aqt.qt` shim returns the correct class
regardless of which Qt version Anki is built against.

**The action is parented to `mw`.** Qt then owns the object, so it is not
garbage-collected when `setup_menu()` returns — a common cause of menu items
silently failing to appear.

**The folder is linked as `chinese_phrase_generator`, not
`chinese-phrase-generator`.** Anki imports the add-on folder as a Python
module, and hyphens are not valid in module names, so the link name
deliberately differs from the repository name.

## Verification
Restart Anki. "Tools → Generate practice phrases" appears, and clicking it
shows a confirmation dialog. The add-on is listed under Tools → Add-ons.

## Next
Task 13: vendor jieba and pypinyin into `addon/lib/` and confirm they import
inside Anki's bundled Python.