import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

import datetime, time

def convert_to_unixtime(string_date):
	return time.mktime(datetime.datetime.strptime(string_date, "%Y-%m-%d").timetuple())

def get_mae(max_leaf_nodes, predictors_train, predictors_val, targ_train, targ_val):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(predictors_train, targ_train)
    preds_val = model.predict(predictors_val)
    mae = mean_absolute_error(targ_val, preds_val)
    return(mae)

def main():
	data = pd.read_csv('dumps/{filename}'.format(filename='2018-07-22_14:55:09_TIME_SERIES_DAILY_ADJUSTED_compact.csv'))
	print data.columns
	print data.close.head()
	print data[['high', 'low']].describe()

	y = data.high
	predictors = ['timestamp']
	data['timestamp'] = data['timestamp'].map(convert_to_unixtime)
	X = data[predictors]

	train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)
	for max_leaf_nodes in [5, 50, 500, 5000]:
	    my_mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
	    print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %(max_leaf_nodes, my_mae))

	forest_model = RandomForestRegressor()
	forest_model.fit(train_X, train_y)
	melb_preds = forest_model.predict(val_X)
	print(mean_absolute_error(val_y, melb_preds))

if __name__ == '__main__':
    main()
