import csv
from operator import itemgetter

class Inventory():                    
    def __init__(self, csv_filename):
        with open(csv_filename) as f: 
            reader = csv.reader(f)
            rows = list(reader)
        self.header = rows[0]        
        self.rows = rows[1:]

        for row in self.rows:              
            row[-1] = int(row[-1])

        self.id_to_row = {}                        
        for row in self.rows:                       
            self.id_to_row[row[0]] = row

        self.prices = set()                          
        for row in self.rows:                        
            self.prices.add(row[-1])
        
        self.rows_by_price = sorted(self.rows, key=itemgetter(-1))
    
    def get_laptop_from_id(self, laptop_id):
        for row in self.rows:                 
            if row[0] == laptop_id:
                return row
        return None   
    
    def get_laptop_from_id_fast(self, laptop_id):  
        if laptop_id in self.id_to_row:           
            return self.id_to_row[laptop_id]
        return None
    
    def check_promotion_dollars(self, dollars):    
        for row in self.rows:                   
            if row[-1] == dollars:
                return True
        for row1 in self.rows:                  
            for row2 in self.rows:
                if row1[-1] + row2[-1] == dollars:
                    return True
        return False                        
    
    def check_promotion_dollars_fast(self, dollars):
        if dollars in self.prices:                   
            return True
        for price in self.prices:                    
            if dollars - price in self.prices:
                return True
        return False                                
    
    def find_laptop_with_price(self, target_price):
        range_start = 0                                   
        range_end = len(self.rows_by_price) - 1                       
        while range_start < range_end:
            range_middle = (range_end + range_start) // 2  
            value = self.rows_by_price[range_middle][-1]
            if value == target_price:                            
                return range_middle                        
            elif value < target_price:                           
                range_start = range_middle + 1             
            else:                                          
                range_end = range_middle - 1 
        if self.rows_by_price[range_start][-1] != target_price:                  
            return -1                                      
        return range_start
    
    def find_first_laptop_more_expensive(self, target_price): 
        range_start = 0                                   
        range_end = len(self.rows_by_price) - 1                   
        while range_start < range_end:
            range_middle = (range_end + range_start) // 2  
            price = self.rows_by_price[range_middle][-1]
            if price > target_price:
                range_end = range_middle
            else:
                range_start = range_middle + 1
        if self.rows_by_price[range_start][-1] <= target_price:                  
            return -1                                   
        return range_start

inventory = Inventory('laptops.csv')                   
print("Number of laptops in inventory: ", len(inventory.rows))
print(inventory.header)              
for i in range(2):
    print(inventory.rows[i])
print("\n   1.a Laptop'info of the given ID: ", inventory.get_laptop_from_id('3362737'))
print("   1.a Laptop'info of the given ID: ", inventory.get_laptop_from_id('3362736'))
print("\n   1.b Laptop'info of the given ID (fast way): ", inventory.get_laptop_from_id_fast('3362737'))
print("   1.b Laptop'info of the given ID (fast way): ", inventory.get_laptop_from_id_fast('3362736'))        
print("\n   2.a Was or wasn't promotion price fitted with 1, 2 laptop's price?: ", inventory.check_promotion_dollars(1000))    
print("   2.a Was or wasn't  promotion price fitted with 1, 2 laptop's price?: ", inventory.check_promotion_dollars(442))       
print("\n   2.b Was or wasn't  promotion price fitted with 1, 2 laptop's price?: ", inventory.check_promotion_dollars_fast(1000)) 
print("   2.b Was or wasn't  promotion price fitted with 1, 2 laptop's price?: ", inventory.check_promotion_dollars_fast(442))  
print("\n   3.a Index of the most expensive laptop that user can buy: ", inventory.find_first_laptop_more_expensive(1000)) 
print("   3.a Index of the most expensive laptop that user can buy: ", inventory.find_first_laptop_more_expensive(10000))

import time                                                         
import random                                                       
inventory = Inventory('laptops.csv')                                
	
ids = [str(random.randint(1000000, 9999999)) for _ in range(10000)] 

total_time_no_dict = 0                                              
for identifier in ids:                                              
    start = time.time()                                             
    inventory.get_laptop_from_id(identifier)                        
    end = time.time()                                               
    total_time_no_dict += end - start                               
    
total_time_dict = 0                                                 
for identifier in ids:                                              
    start = time.time()                                             
    inventory.get_laptop_from_id_fast(identifier)                   
    end = time.time()                                               
    total_time_dict += end - start                                  

print("\nTotal time of function: ", total_time_no_dict)                                           
print("Total time of function having constant syntax: ", total_time_dict)
print("""    => We can see a significant improve in performance. If we divide 0.588 by 0.002 we see that the new method is about 294 times faster for this input size.""")
	
prices = [random.randint(100, 5000) for _ in range(100)] 

total_time_no_set = 0                                    
for price in prices:                                     
    start = time.time()                                  
    inventory.check_promotion_dollars(price)             
    end = time.time()                                    
    total_time_no_set += end - start                     
    
total_time_set = 0                                       
for price in prices:                                     
    start = time.time()                                  
    inventory.check_promotion_dollars_fast(price)        
    end = time.time()                                    
    total_time_set += end - start                        
    
print("\nTotal time of function: ", total_time_no_set)                                 
print("Total time of function having constant syntax: ", total_time_set)
print("""    => We can see a significant improve in performance. If we divide 0.7781 by 0.0002 we see that the new method is about 2593 times faster for this input size.""")