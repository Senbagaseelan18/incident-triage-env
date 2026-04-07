.PHONY: help install test run validate docker-build docker-run clean

help:
	@echo "Incident Triage Environment - Commands"
	@echo "========================================"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make validate     - Validate environment setup"
	@echo "  make run          - Run inference (all tasks)"
	@echo "  make run-easy     - Run inference on easy task"
	@echo "  make run-medium   - Run inference on medium task"
	@echo "  make run-hard     - Run inference on hard task"
	@echo "  make server       - Start FastAPI server"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docker-push  - Push to Docker registry"
	@echo "  make clean        - Clean build artifacts"

install:
	pip install -r requirements.txt

test:
	python -m unittest discover -s tests -p "test_*.py" -v

validate:
	python validate.py

run: run-easy run-medium run-hard

run-easy:
	python inference.py --task task_easy --episodes 3

run-medium:
	python inference.py --task task_medium --episodes 3

run-hard:
	python inference.py --task task_hard --episodes 3

server:
	python -m server.main

docker-build:
	docker build -t incident-triage-env:latest .

docker-run:
	docker run -it -p 7860:7860 incident-triage-env:latest

docker-push:
	docker tag incident-triage-env:latest $(DOCKER_REPO)/incident-triage-env:latest
	docker push $(DOCKER_REPO)/incident-triage-env:latest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/ build/ dist/ *.egg-info/
