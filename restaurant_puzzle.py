'''
   Script to solve the Jurgensville Restaurant Puzzle

   Because it is the Internet Age, but also it is a recession,
   the Comptroller of the town of Jurgensville has decided to
   publish the prices of every item on every menu of every
   restaurant in town, all in a single CSV file (Jurgensville
   is not quite up to date with modern data serialization methods).
   In addition, the restaurants of Jurgensville also offer Value
   Meals, which are groups of several items, at a discounted price.
   The Comptroller has also included these Value Meals in the file.
   The file's format is:

   for lines that define a price for a single item:
       restaurant ID, price, item_label

   for lines that define the price for a Value Meal (there can be any
   number of items in a value meal)
       restaurant ID, price, item_1_label, item_2_label, ...

   All restaurant IDs are integers, all item labels are underscore
   (no space) separated letters, and the price is a decimal number.

   Given a town's price file and a list of item labels that someone
   wants to eat for dinner, the script outputs the restaurant they should
   go it and the total cost it will cost them. It is fine to purchase
   extra items, as long as the total cost is minimized.

'''

from collections import defaultdict
import csv
import sys

data_dict = defaultdict(list)

def populateMenuDict(file_data):
        '''
        Function to populate menu values into a dictionary
        from the item file

        args:
        file_data(str): File with prices of items

        except:
        None

        returns:
        None

        '''
        
	with open(file_data,"r") as f_data:
		data_reader = csv.reader(f_data)
		for row in data_reader:
			d = {}
			d[row[1]] = row[2].strip() 
			data_dict[row[0]].append(d)
	
	f_data.close()


def identifyRestaurant(list_items):
        '''
        Function to identify best restaurant
        for a list of items to be purchased.

        args:
        list_items(list): List of items to be purchased

        except:
        None

        returns:
        None

        '''
        
	final_rest_id = 0
	final_price = 0.0
	curr_price = 0.0

	p = []
	
	for rest_id in data_dict:
		for comb in data_dict[rest_id]:
			p = [ price for price,food_label in comb.items() if food_label in list_items ]
			if p:
				curr_price += float(p[0])

		if (curr_price < final_price or final_price == 0) and curr_price != 0.0:
			final_price = curr_price
			final_rest_id = rest_id
		curr_price = 0.0
	
	if final_rest_id == 0 and final_price == 0.0:
		print "Nil"
	else: 
		print str(final_rest_id) + " " + str(final_price)

if __name__ == '__main__':
	file_data = sys.argv[1]
	list_items = [ x for x in sys.argv[2:] ]
	
	populateMenuDict(file_data)
	identifyRestaurant(list_items)
