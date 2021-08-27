import sqlite3 as sql
import pandas as pd


# create and make a connection to the database file
conn = sql.connect('dojo.db')


# we will use pandas for easier file loading to the database
csv_files = ['location', 'region', 'product', 'location_region', 'sales']
for csv in csv_files:
    df = pd.read_csv(f'.//db_files//{csv}.csv')
    df.to_sql(csv, conn, if_exists='replace', index=False)


# cursor is what is used to "drive" queries
c = conn.cursor()


# now that we have the database set up, we can query our data

# simple query to pull all locations and their regions
c.execute('select * from location_region')
# fetchall retreives the results of the most recent execute statement
print(c.fetchall())


# let's pull the names for the locations and regions instead of the ids
# for this we need to join the location, region, and location_region table
# and use the where clause to show the feild that are the same
c.execute("""
    select location_name, region_name
    from location join region join location_region
    where location.location_id == location_region.location_id
        and region.region_id == location_region.region_id    
""")
print(c.fetchall())


# now we will look at some sales data
# similar to the last query we will join the relevant tables and
# show which field are the same
c.execute("""
    select location_name, product_name, lbs, price_per_lb
    from location join location_region join sales join product
    where location.location_id == location_region.location_id
        and location.location_id == sales.location_id
        and sales.product_id = product.product_id 
""")
print(c.fetchmany(20))  # just pull the first 20 (not the top 20; we will do that next)


# let's now look at the total price and sort the values
c.execute("""
    select location_name, product_name, lbs, price_per_lb, (lbs * price_per_lb) price
    from location join location_region join sales join product
    where location.location_id == location_region.location_id
        and location.location_id == sales.location_id
        and sales.product_id = product.product_id 
    order by price desc
""")
print(c.fetchmany(20))  # just pull the first 20 (not the top 20; we will do that next)


# we can print this a little prettier
print(f'Name, Product, Price')
lines = c.fetchmany(50)
for line in lines:
    print(f'{line[0]}, {line[1]}, ${line[4]:.2f}')


# last query we will take some user input for a region and how the sales by product
# lets start by getting the available regions
c.execute('select region_name from region')
# fetchall returns tuple of lists, convert to just a list
regions = [reg[0] for reg in c.fetchall()]
region = ''
while True:
    print('Avaiable regions: ' + ', '.join(regions))  # show the valid regions
    # ask user for input
    region = input('What input would you like to see sales data for? ')
    # if the input is valid, we can break the loop, else ask for input again
    if region not in regions:
        print("Invalid Input!")
    else:
        break

# query the database using the user's input
# we need to introduce the group by clause since the products are
# associated with with locations, not regions
# we also will use the where clause to test for only the region we want
c.execute("""
    select region_name, product_name, (lbs * price_per_lb) price
    from region join location_region join sales join product
    where region.region_id == location_region.region_id
        and location_region.location_id == sales.location_id
        and sales.product_id = product.product_id 
        and region_name = ?
    group by region_name, product_name
    order by price desc
""", (region,))  # when only using one parameter in the query you need an extra comma and the end of the tuple being passed in

results = c.fetchall()
print(f'Results for {region}\nProduct, Price')
print('-'*30)
for line in results:
    print(f'{line[1]}, ${line[2]:.2f}')


# last step we need is to close the connection to the database
conn.close()
