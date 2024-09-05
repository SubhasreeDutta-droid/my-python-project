# PyLS - Python File Listing Utility

**PyLS** is a Python-based command-line utility that mimics the basic functionality of the `ls` command. It allows users to list directories and files from a structured JSON file while providing additional options such as long format listing, sorting by time, filtering by type (file or directory), and more.

## Features

- List directory contents.
- Options to display output in a long listing format (`-l`).
- Reverse the order of displayed contents (`-r`).
- Sort contents by modification time (`-t`).
- Filter results to only display files or directories (`--filter`).
- Navigate JSON directory structure via relative paths.
- Human-readable file sizes.

## Installation

### Prerequisites

- Python 3.7 or higher
- Git (to clone the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/SubhasreeDutta-droid/my-python-project.git
cd my-python-project
### set up a virtual env.
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

install dependencies.
pip install .
