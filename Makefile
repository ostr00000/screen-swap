
PYTHON ?= $(shell which python)
$(info Using python=${PYTHON})

install-pre-commit:
	${PYTHON} -m pip install pre-commit

run-pre-commit:
	${PYTHON} -m pre_commit run --all-files

install_editable:
	${PYTHON} -m pip install -e .

uninstall_editable:
	${PYTHON} -m pip uninstall -y screen_swap
