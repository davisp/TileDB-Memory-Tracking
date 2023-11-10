all: data/import.jpg data/consolidation.jpg

data/customer.csv: ./src/generate_customers.sh
	@mkdir -p data/
	./src/generate_customers.sh

data/tpc_array data/import.log: ./src/create_array.py data/customer.csv
	./src/create_array.py data/customer.csv data/tpc_array > data/import.log

data/consolidation.log: ./src/consolidate_array.py data/tpc_array
	rm -f data/tpc_array_copy
	cp -r data/tpc_array data/tpc_array_copy
	./src/consolidate_array.py data/tpc_array_copy > data/consolidation.log

data/import.csv: ./src/log_to_csv.py data/import.log
	./src/log_to_csv.py data/import.log > data/import.csv

data/consolidation.csv: ./src/log_to_csv.py data/consolidation.log
	./src/log_to_csv.py data/consolidation.log > data/consolidation.csv

data/import.jpg data/consolidation.jpg: data/plot.R data/import.csv data/consolidation.csv
	Rscript src/plot.R
