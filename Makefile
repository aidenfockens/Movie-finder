# Define variables
REACT_DIR=movie-frontend
FLASK_APP=app.py 
FLASK_PORT=5001
NOTEBOOKS = data_analysis/create_model.ipynb data_analysis/visualize_data.ipynb
PY_SCRIPTS=$(NOTEBOOKS:.ipynb=.py)

# Targets
.PHONY: install install-flask install-react install-notebooks convert-notebooks run-notebooks start-react start-flask clean notebooks webapp

# Install dependencies for both React and Flask
install: install-react install-flask install-notebooks

# Install React dependencies
install-react:
	cd $(REACT_DIR) && npm install

# Install Flask dependencies
install-flask:
	pip install -r requirements.txt

# Install Notebook dependencies
install-notebooks:
	pip install jupyter nbconvert matplotlib scikit-learn xgboost pandas

convert-notebooks:
	jupyter nbconvert --to script $(NOTEBOOKS)

run-notebooks: convert-notebooks
	@echo "Running notebooks as scripts..."
	@for script in $(PY_SCRIPTS); do python $$script; done

# Start React app
start-react:
	cd $(REACT_DIR) && npm start

# Start Flask app
start-flask:
	export FLASK_APP=$(FLASK_APP) && export FLASK_ENV=development && flask run --port=$(FLASK_PORT)

# Clean generated files
clean:
	rm -rf $(REACT_DIR)/node_modules
	rm -rf __pycache__
	rm -rf instance
	rm -f *.db
	rm -f $(REACT_DIR)/build
	rm -f data_analysis/*.py
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Notebooks workflow
notebooks: install-notebooks run-notebooks

# Web application workflow

webapp: install
	@make start-flask &
	@make start-react &
	
