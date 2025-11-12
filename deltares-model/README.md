Assumptions:
- I've assumed that the flow weighted concentration should be at least equal to the initial
concentration
- I've assumed that reaches.csv always has reach A on the first row and reach B on the second
- I've assumed that the csv file are in the right location, potentially that should be checked


How to run it:
cd deltares-model/
poetry run python src/deltares_model/hydrology_simulation.py