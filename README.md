# Block World Planning Agent

> **Solver for the planning problem** called _"Blocks World"_ from the **Artificial Intelligence** course (Federal University of Ceará - UFC, 2025.2).

> [!IMPORTANT]\
> This applications runs **Python 3.14.0**.

## How to Run?

> [!NOTE]\
> Assuming your environment is Linux, the following steps are completely valid.
> However, if it is not, **please refer to the link at the end of the section**.

First, create Python virtual enviroment using the following command:

```bash
python -m venv <env-directory>

# for example, something like...
python -m venv .venv
```

Immediately after that, activate the virtual environment with the command `source ./<env-directory>/bin/activate` to ensure that no dependencies are persistently installed on your machine.

Then, install the dependencies:

```bash
pip install -r ./requirements.txt
```

It is now possible to run the application with:

```bash
# to run only instance 4-0
python ./main.py --instance=4-0 --algorithm=BFS

# or run multiple instances with a single algorithm
python ./main.py --instance=[4-0,7-0,9-0] --algorithm=A*
```

> [!IMPORTANT]\
> It is mandatory to provide the flags `--instance=` (the **STRIPS** instance to be executed,
> which is identified by the pattern `r'^\d-\d$'` or `r'^\[\d+-\d+(,\d+-\d+)*\]$'` and is contained in `./assets/planningsat`) and `--algorithm=`
> (the search algorithm that will operate on the instance).

Finally, don't forget to disable your virtual environment (venv).

```bash
# with just one command...
deactivate
```

> [!TIP]\
> If you have any questions, please consult:
> [(Python Land) Python venv: How To Create, Activate, Deactivate, And Delete](https://python.land/virtual-environments/virtualenv#google_vignette)
