# pyops-lab
A curated set of Python exercises inspired by real-world SRE tasks.

These exercises simulate common SRE scenarios like:
- Parsing logs and alerts
- Validating metrics thresholds
- Automating incident recovery logic
- Simulating system behavior (latency, retries, usage)
- Working with Kubernetes or PostgreSQL data

## 📁 Structure
```bash
pyops-lab/
├── parsing/                     
└── metrics/                    
    ├── pyproject.toml
    ├── metrics/                    
        ├── __init__.py
        ├── run.py  # this contains `if __name__ == "__main__"`
        ├── percentiles_calculator.py
├── pyproject.tml            
└── README.md
````

## 🚀 Getting Started

```bash
git clone https://github.com/Matias316/pyops-lab.git
cd pyops-lab
poetry install 
poetry run pytest          
```

## Running subprojects

All subprojects include entrypoint

```bash
cd pyops-lab

# Example: poetry run -C metrics python metrics/percentiles_calculator.py
poetry run -C <subproject> python <subproject_folder_name>/<utility>
```