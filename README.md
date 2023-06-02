# GIS_KARTO

## Semesteruebung

### Ablauf der Datenanalyse

1. [results_data.py](src/get_data/results_data.py) &rarr; [results_bfs.geojson](export/results/results_bfs.geojson)
2. [bike_data.py](src/get_data/bike_data.py) &rarr; [bikes.geojson](export/velo/bikes.geojson)
3. [accidents_data](src/get_data/accidents_data.py) &rarr; [accidents.geojson](export/accidents/accidents.geojson)
4. [count_accidents](src/count_accidents.py) &rarr; [master_with_accidents.geojson](export/master/master_with_accidents.geojson)
5. Zwischenschritt in ArcGIS (Aufsummierung Velowege pro Gemeinde)
6. [add_bike.py](src/add_bike.py) &rarr; [master_acc_bike.geojson](export/master/master_acc_bike.geojson)
7. [results_data.py](src/get_data/results_data.py) &rarr; [results_bfs.geojson](export/results/results_bfs.geojson)
8. Zwischenschritt in QGIS (Ausummierung der Verkehrswege pro Gemeinde)
9. [values.py](src/map_values.py) &rarr; [final_values.geojson](export/final_values.geojson)
10. [corr.py](src/corr.py)
11. [plots.py](src/plots.py) &rarr; [plots/](export/plots/)
