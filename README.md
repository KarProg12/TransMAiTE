# TransMAiTE

### SDLXLIFF ↔ JSON / TXT Converter

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/) 
[![GUI](https://img.shields.io/badge/GUI-tkinter%20%2F%20ttk-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Download-Releases-orange.svg)](https://github.com/KarProg12/TransMAiTE/releases)

**TransMAiTE** is a desktop application for exporting translatable segments from Trados `.sdlxliff` files and importing translations back into the original file.

It works with:

- `.sdlxliff` SDL Trados files
- structured `export.json` files
- editable `source.txt` and `target.txt` files
- AI translation tools or external text editors

The app extracts untranslated segments together with their internal XML formatting, lets you translate them outside Trados Studio, and then inserts the translations back into the SDLXLIFF document.

No Python installation or third-party packages are required when using the released `.exe` version.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Output Files](#output-files)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Important Notes](#important-notes)
- [License](#license)

---

## Features

### Export — SDLXLIFF to JSON and TXT

The export action creates a project folder containing:

- `export.json` — segment data and repeated-source information
- `source.txt` — source text, one segment per line
- `target.txt` — initially empty, ready for translation

Exported data includes:

- `trans-unit_id`
- `seg_id`
- segment status
- source text
- existing target text
- internal XML formatting tags such as `<g>` and `<x/>`

The following segments are skipped:

- segments with `locked="true"`
- `Translated`
- `ApprovedTranslation`
- `ApprovedSignOff`
- `RejectedTranslation`
- `RejectedSignOff`

Export uses streaming XML parsing with `xml.etree.ElementTree.iterparse`, so trans-unit elements can be processed and released one at a time.

### Import — TXT to JSON to SDLXLIFF

The import action reads a translated `target.txt`, updates `export.json`, and writes the translations into the SDLXLIFF file.

Import behavior:

- TXT line count must match the number of exported JSON segments
- trailing empty lines in the TXT file are ignored
- empty lines in the middle are preserved as empty translations
- internal newlines are represented as `\n` in TXT files
- `\n` is converted back to a real newline in JSON
- translation tags are parsed as XML when possible
- plain text is used as a fallback for invalid XML content
- imported segment definitions are set to the `Draft` confirmation status
- repeated source text is propagated to matching segments
- propagated segments are marked with `origin="auto-propagated"`
- a backup copy is created on the first import

The app also reports the number of translated segments inserted, while the console reports additional comparison and propagation details.

### Graphical Interface

- standard-library `tkinter` / `ttk` interface
- dark interface theme
- status bar with success and error messages
- separate Export and Import sections
- no external Python GUI packages required
- automatic path filling after selecting the first SDLXLIFF file

After selecting an SDLXLIFF file, TransMAiTE automatically fills:

- the project/output folder
- the original SDLXLIFF path in the Import section
- the `export.json` path

The translated TXT file and output SDLXLIFF file are still selected by the user.

---

## How It Works

```text
.sdlxliff
    ↓ Export
export.json + source.txt + target.txt
    ↓ Translate target.txt or edit export.json
export.json with translated targets
    ↓ Import TXT → JSON → SDLXLIFF
translated .sdlxliff
```

### 1. Export

Select an SDLXLIFF file and an output folder, then press **Create folder and export**.

The exporter:

1. finds `<trans-unit>` elements
2. reads source segment markers
3. checks segment status and lock state
4. preserves existing target text when available
5. writes `export.json`, `source.txt`, and `target.txt`

### 2. Translate

Open `source.txt` and copy the source text into `target.txt`, keeping the same number and order of lines.

You may also edit the `target` values directly in `export.json`.

Keep one segment per line. Use `\n` inside a TXT line if a translation should contain a newline.

### 3. Import

Select:

- the original SDLXLIFF file
- `export.json`
- the translated `target.txt`

Choose the destination SDLXLIFF file and press **Import `.json` to `.sdlxliff`**.

The TXT is first synchronized with JSON. JSON translations are then inserted into matching `<trans-unit>` and segment IDs in the SDLXLIFF XML.

---

## Output Files

### `export.json`

```json
{
  "segments": [
    {
      "trans-unit_id": "123",
      "seg_id": "1",
      "status": "Not Translated",
      "source": "Source text",
      "target": "Translated text"
    }
  ],
  "repetitions": {}
}
```

### `source.txt`

```text
Source text
Another source segment
```

### `target.txt`

```text
Translated text
Another translated segment
```

### Backup

When importing for the first time, TransMAiTE creates:

```text
original_filename.sdlxliff.bak
```

The backup is stored next to `export.json` and is created only if it does not already exist.

---

## Installation

### Released executable

1. Download the latest release.
2. Run the `.exe` file.
3. No Python installation or third-party package installation is required.

### Run from source

Requirements:

- Python 3.11 or newer
- `tkinter` / `ttk`

From a terminal:

```bash
python transmAIte.py
```

Only the Python standard library is used.

---

## Usage

1. Launch TransMAiTE.
2. In **Export**, select the source `.sdlxliff` file.
3. Select or confirm the output project folder.
4. Export the segments.
5. Translate `target.txt` or edit `export.json`.
6. In **Import**, confirm the original SDLXLIFF and JSON paths.
7. Select the translated `target.txt`.
8. Choose the destination `.sdlxliff` file.
9. Import the translations.

---

## Project Structure

```text
TransMAiTE/
├── transmAIte.py  # tkinter/ttk desktop interface
├── converter.py    # SDLXLIFF, JSON, and TXT conversion logic
├── README.md
└── LICENSE
```

### `transmAIte.py`

Provides the graphical interface, path selection, automatic path synchronization, status bar, task execution, and success/error dialogs.

### `converter.py`

Provides all conversion operations:

- export SDLXLIFF → JSON + TXT
- import TXT → JSON
- import JSON → SDLXLIFF
- XML namespace and tag handling
- repeated-segment propagation
- backup creation

---

## Technologies

- Python 3.11+
- `tkinter` / `ttk`
- `xml.etree.ElementTree`
- SDLXLIFF 1.2 XML
- JSON
- plain text TXT files

---

## Important Notes

- Always keep a backup of important SDLXLIFF projects.
- Target TXT files must contain exactly one line per exported segment, except ignored trailing empty lines.
- Segment tags should be preserved when translating with AI tools.
- Importing translations updates segment confirmation status to `Draft`.
- Repeated source text may propagate the same translation to multiple segments.
- Tag mismatches between source and translation are reported in the console.
- The app intentionally creates the backup in the export/project folder, rather than alongside every output file.
- XML names used by Trados are registered again before the output file is written.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
