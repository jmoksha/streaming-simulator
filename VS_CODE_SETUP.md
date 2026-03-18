# 🔧 VS CODE SETUP GUIDE

## 📂 COMPLETE FILE STRUCTURE

```
streaming_simulator/                    ← ROOT FOLDER (Open this in VS Code)
│
├── 📄 START_HERE.md                    ⭐ Read first
├── 📄 QUICKSTART.md                    Quick setup (5 min)
├── 📄 README.md                        Full guide
├── 📄 INDEX.md                         Navigation
├── 📄 MANIFEST.md                      File listing
├── 📄 ARCHITECTURE.md                  Design patterns
├── 📄 PROJECT_SUMMARY.md               Features
├── 📄 DELIVERY.md                      Checklist
│
├── 📂 src/                             ← CORE MODULES
│   ├── __init__.py                     Package init
│   ├── markov_model.py                 Markov chain (413 lines)
│   ├── simulation.py                   Simulations (539 lines)
│   └── visualization.py                Visualizations (649 lines)
│
├── 📂 app/                             ← DASHBOARD
│   └── streamlit_dashboard.py          Main app (738 lines)
│
├── 📂 notebooks/                       ← JUPYTER
│   └── analysis.ipynb                  Analysis (200+ cells)
│
├── 📂 data/                            ← DATA
│   └── transition_matrix.csv           Default matrix
│
├── 📄 test_project.py                  Test suite
├── 📄 requirements.txt                 Dependencies
├── 📄 .gitignore                       Git config
└── 📄 VS_CODE_SETUP.md                 This file

```

---

## 🎯 OPEN IN VS CODE

### Method 1: Open Folder (Recommended)
1. **File** → **Open Folder**
2. Navigate to: `/mnt/user-data/outputs/streaming_simulator/`
3. Click **Select Folder**

### Method 2: Command Line
```bash
cd /mnt/user-data/outputs/streaming_simulator
code .
```

### Method 3: Direct Open
```bash
code /mnt/user-data/outputs/streaming_simulator
```

---

## 📝 KEY FILES TO EDIT IN VS CODE

### Python Files (Executable)
| File | Lines | Purpose |
|------|-------|---------|
| `src/markov_model.py` | 413 | Markov chain core |
| `src/simulation.py` | 539 | Simulations |
| `src/visualization.py` | 649 | Visualizations |
| `app/streamlit_dashboard.py` | 738 | Dashboard UI |
| `test_project.py` | 333 | Tests |

### Documentation Files (Read)
| File | Read | Purpose |
|------|------|---------|
| `START_HERE.md` | ⭐ First | Overview |
| `README.md` | Second | Full guide |
| `QUICKSTART.md` | Quick | 5-min setup |
| `ARCHITECTURE.md` | Deep | Design |

### Configuration Files
| File | Edit | Purpose |
|------|------|---------|
| `requirements.txt` | Sometimes | Dependencies |
| `data/transition_matrix.csv` | Optional | Default matrix |
| `.gitignore` | Rarely | Git config |

---

## ▶️ RUN COMMANDS IN VS CODE

### Option 1: Terminal in VS Code

1. **View** → **Terminal** (or Ctrl + `)
2. Navigate to project:
   ```bash
   cd /mnt/user-data/outputs/streaming_simulator
   ```

### Option 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Option 3: Run Streamlit Dashboard
```bash
streamlit run app/streamlit_dashboard.py
```

### Option 4: Run Tests
```bash
python test_project.py
```

### Option 5: Run Jupyter Notebook
```bash
jupyter notebook notebooks/analysis.ipynb
```

### Option 6: Run Python Script Directly
```bash
# In VS Code, right-click any .py file
# Select "Run Python File in Terminal"
# Or press Ctrl+Shift+D
```

---

## 🔍 CODE NAVIGATION IN VS CODE

### Useful Extensions (Install These)
1. **Python** (Microsoft)
   - IntelliSense, debugging, linting
   - Install: Search in Extensions

2. **Jupyter** (Microsoft)
   - For `.ipynb` files
   - Install: Search in Extensions

3. **Markdown Preview** (Built-in)
   - View `.md` files formatted
   - Click preview icon in editor

### Navigation Shortcuts
| Action | Shortcut |
|--------|----------|
| Go to file | Ctrl+P |
| Go to definition | Ctrl+Click |
| Find symbol | Ctrl+Shift+O |
| Search project | Ctrl+Shift+F |
| Open terminal | Ctrl+` |
| Format code | Shift+Alt+F |

---

## 📂 FOLDER STRUCTURE IN VS CODE

### What Each Folder Contains

**`src/`** - Core Python modules
- `markov_model.py` ← Markov chain implementation
- `simulation.py` ← Monte Carlo & Poisson
- `visualization.py` ← All plotting functions
- `__init__.py` ← Package setup

**`app/`** - Web dashboard
- `streamlit_dashboard.py` ← Interactive app

**`notebooks/`** - Jupyter analysis
- `analysis.ipynb` ← 200+ cells of analysis

**`data/`** - Configuration
- `transition_matrix.csv` ← Default 6×6 matrix

**Root folder** - Documentation & config
- `README.md` ← Complete guide
- `requirements.txt` ← Dependencies
- `test_project.py` ← Tests
- `*.md` files ← Documentation

---

## 🚀 TYPICAL VS CODE WORKFLOW

### Step 1: Open Project
```bash
code /mnt/user-data/outputs/streaming_simulator
```

### Step 2: Install Dependencies
```bash
# In VS Code terminal
pip install -r requirements.txt
```

### Step 3: Explore Code
- Open `src/markov_model.py`
- Read docstrings (Ctrl+Hover)
- Check method signatures (Ctrl+K Ctrl+I)

### Step 4: Run Dashboard
```bash
# In VS Code terminal
streamlit run app/streamlit_dashboard.py
```

### Step 5: Run Tests
```bash
# In VS Code terminal
python test_project.py
```

### Step 6: Jupyter Notebook
```bash
# In VS Code terminal
jupyter notebook notebooks/analysis.ipynb
```

---

## 🔧 DEBUGGING IN VS CODE

### Python Debugging Setup

1. **Create `.vscode/launch.json`**:
   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: Current File",
               "type": "python",
               "request": "launch",
               "program": "${file}",
               "console": "integratedTerminal"
           },
           {
               "name": "Python: Module",
               "type": "python",
               "request": "launch",
               "module": "streamlit",
               "args": ["run", "app/streamlit_dashboard.py"],
               "console": "integratedTerminal"
           }
       ]
   }
   ```

2. **Set Breakpoints**: Click left margin on line number

3. **Run Debugger**: F5 (or Run → Start Debugging)

---

## 📖 RECOMMENDED READING ORDER IN VS CODE

1. **Click file, Ctrl+Shift+V to preview markdown**:
   - `START_HERE.md` (overview)
   - `QUICKSTART.md` (setup)
   - `README.md` (full guide)

2. **Read source code** (in order):
   - `src/markov_model.py` (understand core)
   - `src/simulation.py` (understand simulation)
   - `src/visualization.py` (understand plotting)
   - `app/streamlit_dashboard.py` (understand UI)

3. **Explore Jupyter**:
   - Open `notebooks/analysis.ipynb`
   - Click cells to run
   - Modify and experiment

---

## 💡 VS CODE TIPS

### VS Code Settings for Python
1. **View** → **Command Palette** (Ctrl+Shift+P)
2. Type: `Python: Select Interpreter`
3. Choose your Python version

### Format Code Automatically
1. **View** → **Command Palette**
2. Type: `Format Document`
3. Or press: Shift+Alt+F

### Run Code Selection
1. Select code lines
2. Right-click → **Run Selection in Python Terminal**
3. Or Shift+Enter

### IntelliSense Help
1. Type code
2. Ctrl+Space for suggestions
3. Hover over code for documentation

---

## 📂 FILE DESCRIPTIONS FOR VS CODE

### Python Modules

**`src/markov_model.py`** (413 lines)
- `MarkovChainModel` class
- `compute_steady_state()` method
- `check_ergodicity()` method
- Comprehensive docstrings

**`src/simulation.py`** (539 lines)
- `SimulationEngine` class
- `PoissonArrivalProcess` class
- `SimulationResult` dataclass
- `run_simulation()` method

**`src/visualization.py`** (649 lines)
- `MarkovChainVisualizer` class
- `SimulationVisualizer` class
- 13 plotting methods
- Interactive dashboards

**`app/streamlit_dashboard.py`** (738 lines)
- Streamlit application
- Sidebar controls
- 4 main tabs
- Real-time metrics

### Notebooks

**`notebooks/analysis.ipynb`** (200+ cells)
- Setup & imports
- Markov chain analysis
- Simulation examples
- Sensitivity analysis
- Key insights

### Data

**`data/transition_matrix.csv`** (6×6)
- Default transition matrix
- 6 states
- Realistic probabilities
- Editable

---

## 🔧 COMMON VS CODE TASKS

### Task 1: Edit Transition Matrix
1. Open: `data/transition_matrix.csv`
2. Edit probabilities in spreadsheet view
3. Save: Ctrl+S
4. Re-run dashboard to see changes

### Task 2: Add Custom Metrics
1. Open: `src/simulation.py`
2. Find: `get_metrics()` method
3. Add new calculation
4. Save and run tests

### Task 3: Create New Visualization
1. Open: `src/visualization.py`
2. Add new method to visualizer class
3. Use matplotlib/plotly
4. Test in dashboard or notebook

### Task 4: Modify Dashboard
1. Open: `app/streamlit_dashboard.py`
2. Edit layout or add new elements
3. Save: Ctrl+S
4. Dashboard auto-reloads

---

## ✅ VERIFY INSTALLATION

### Terminal Commands
```bash
# Check Python
python --version

# Check pip
pip --version

# Install dependencies
pip install -r requirements.txt

# Verify imports
python -c "import numpy, pandas, streamlit; print('✓ All installed')"

# Run tests
python test_project.py

# Start dashboard
streamlit run app/streamlit_dashboard.py
```

---

## 🎯 VS CODE WORKSPACE SETUP

### Create Workspace File

1. **File** → **Save Workspace As**
2. Name: `streaming_simulator.code-workspace`
3. Save in project root

### Workspace Contents
```json
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black",
        "[python]": {
            "editor.defaultFormatter": "ms-python.python",
            "editor.formatOnSave": true
        }
    }
}
```

---

## 📊 PROJECT STRUCTURE SUMMARY

```
streaming_simulator/  ← Open this folder in VS Code
├── Core Code (src/)
│   ├── markov_model.py
│   ├── simulation.py
│   ├── visualization.py
│   └── __init__.py
├── Dashboard (app/)
│   └── streamlit_dashboard.py
├── Analysis (notebooks/)
│   └── analysis.ipynb
├── Data (data/)
│   └── transition_matrix.csv
├── Tests
│   └── test_project.py
├── Config
│   ├── requirements.txt
│   └── .gitignore
└── Docs
    ├── START_HERE.md
    ├── README.md
    ├── QUICKSTART.md
    ├── ARCHITECTURE.md
    └── ...
```

---

## 🚀 QUICK START IN VS CODE

1. **Open folder**: `File` → `Open Folder` → select project
2. **Install**: Open terminal, run `pip install -r requirements.txt`
3. **Run**: Terminal, run `streamlit run app/streamlit_dashboard.py`
4. **Code**: Edit files in editor
5. **Test**: Terminal, run `python test_project.py`
6. **Learn**: Read `START_HERE.md` in preview

---

## ✨ YOU'RE READY!

All files are in `/mnt/user-data/outputs/streaming_simulator/`

**Just open the folder in VS Code and start coding!** 🎉

