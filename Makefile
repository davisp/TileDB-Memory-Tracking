all: table.csv

data/customer.csv: ./src/generate_customers.sh
	@mkdir data/
	./src/generate_customers.sh

data/tpc_array: ./src/create_array.py data/customer.csv
	./src/create_array.py data/customer.csv data/tpc_array

data/consolidation.log: ./src/consolidate_array.py data/tpc_array
	./src/consolidate_array.py data/tpc_array > data/consolidation.log

table.csv: ./src/log_to_csv.py data/consolidation.log
	./src/log_to_csv.py data/consolidation.log > table.csv

