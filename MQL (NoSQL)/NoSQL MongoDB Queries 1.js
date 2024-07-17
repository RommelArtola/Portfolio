//Sample Analytics and Customers
use sample_analytics
const analytics  = db.getSiblingDB("sample_analytics")
// 2.1 Build a query that selects all the data in the sample_analytics database and customers collection. JSON View
analytics.getCollection("customers").find({})


// 2.2 Build a query that shows customers’ name, address, and email only (make sure to hide the _id field). 
// Table View
analytics.getCollection('customers').find({},{
    _id: 0,
    name:1,
    address:1,
    email:1
})

// 2.3 Build a query that shows customers’ name and birthdate, sorted by birthdate (descending). Table View
analytics.getCollection('customers').find({},{
    name:1,
    birthdate:1
}).sort({birthdate:-1})


// 2.4 Build a query that shows customers’ name, username, and accounts with the accounts elements 
// listed as columns for all rows. Table View
analytics.getCollection('customers').aggregate([
    {$project: {
        name:1,
        username:1,
        accounts:1
        }
    }
   ]
)



//Sample Restaurants and Restaurants
use 'sample_restaurants'
const rest = db.getSiblingDB("sample_restaurants")
// 3.1 Build a query that shows the street, zipcode, and type of cuisine fields. 
// Expand the address column to see all the sub parts. Sort the list by zipcode and cuisine. Table View
rest.getCollection('restaurants').aggregate([
    {
        $project: {
        'street_addr': '$address.street',
        'zipcode_addr': '$address.street',
        'cuisine': 1
        }
    },
    {
        $sort: {
            'address.zipcode':1,
            'cuisine':1
            }
    }
])


// 3.2 Build a query that shows the restaurant name, cuisine, borough, building, and street. 
// Sort the dataset by borough. JSON View
rest.getCollection('restaurants').aggregate([
    {
        $project:
        {
            'name':1,
            'cuisine':1,
            'borough':1,
            'building': '$address.building',
            'street': '$address.street'
            }
        },
        {
            $sort: {
                'borough':1
            }
         }
  ]
)




// 3.3 Build a query that provides a distinct list of cuisines. JSON View
rest.getCollection('restaurants').distinct('cuisine')



// 3.4 Build a query that lists a distinct list of zipcodes for the restaurants. Table View
rest.getCollection('restaurants').distinct('address.zipcode')

