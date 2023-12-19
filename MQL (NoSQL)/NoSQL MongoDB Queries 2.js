//Use the sample_analytics database and the customers collection.
use sample_analytics
// 1.1 Build a query that lists the customer name and email for customers that are active. JSON
db.customers.aggregate([
    {$match: {'active': {$eq: true} } },
       
    {$project: {name: 1,
                _id: 0,
                'active':1
                }
    }
]);



// 1.2 Build a query that lists the customer name, email, and address for customers in Colorado, they will have 
//    CO in their address field. JSON
db.customers.aggregate([
    {$match: {address: {$regex: /,? ?CO,?/} } }, //Addresses the issue where spaces may have been left out.
    
    {$project: {name: 1,
                email: 1,
                address: 1,
                _id: 0
                }
    }
    
]);





// Use the sample_airbnb database and the listsandreviews collection.
use sample_airbnb
// 2.1 Build a query to list the name, property type, minimum nights, and number of beds and bathrooms.
//    For this trip, you’ll need properties that allow for 5 or fewer nights, have 4 beds, and between 1 
//         and 2 bathrooms. Display the data in a Table view.

db.listingsAndReviews.aggregate([
    {
        $addFields: {
            minimum_nights_int: {$toInt: "$minimum_nights"} 
            //tricky.. had to create a new column to cast str to int. This is pretty fun :)
        }
    },

    {$match: { 'minimum_nights_int': {$lte: 5},
              'beds': {$eq: 4},
              'bathrooms': {$gte: 1.0, $lte: 2.0} 
            }
    },
    {$project: {name: 1,
                property_type: 1,
                minimum_nights_int: 1,
                beds: 1,
                bathrooms: 1,
                _id: 0
                }
    } 

]);





// 2.2 Build a query that shows the name, property type, number of bedrooms, 
//     and reviews for properties that have no reviews. Hide _id field. JSON view.
db.listingsAndReviews.aggregate([
    {$match: {'number_of_reviews': {$lt: 1} }
    },
    
    {$project: {name:1,
                 property_type:1,
                 bedrooms:1,
                 number_of_reviews:1,
                 reviews:1, //show no reviews
                 //reviewCount: {$size: '$reviews'}, Used to double check review count.
                 _id:0
                 }
    }

]);



// 2.3 Build a query that shows the name, property type, minimum nights, amenities, cancellation policy, and beds.
// The list should only include properties that have a flexible or moderate cancellation policy, 
//     at least 4 beds, at least 20 reviews, and it must have Wifi, a refrigerator, and a pool.
// Hint: you’ll need to look at the spelling of some words to make sure you filter this correctly. 
//        Display the data in a JSON view.
db.listingsAndReviews.aggregate([
    {$match: 
            {
                'cancellation_policy': {$in: ['flexible', 'moderate'] },
                'beds': {$gte: 4},
                'number_of_reviews': {$gte: 20},
                'amenities': {$all: [/wifi/i, /pool/i,/refrigerator/i]} //checks for elements regardless of case
            }
    },
    {$project: {_id:0,
                name:1,
                property_type:1,
                minimum_nights:1,
                amenities:1,
                cancellation_policy:1,
                beds:1}}
    
]);
   






// Use the sample_weatherdata and the data collection.
use sample_weatherdata
// 3.1 Build a query that shows the station, call letters, air temperature and wind speed.
// Only includes those documents where the air temperature is extreme. That means temperatures less than -15 or greater than 30. 
//     (These readings are in Celius.) Also, only show readings where the wind speed is greater than or equal to 10.
// Important: You’ll need to also filter out all values that show up as 999.9. 
//    These are situations where the data was not captured.
// Hint: Should only see 12 documents.
db.data.aggregate([
    {
        $match: {
                  $and: [ 
                          {'airTemperature.value': {$ne: 999.9} },
                          {'wind.speed.rate': {$gte:10, $ne: 999.9} },
                          {
                              $or: [ 
                                {'airTemperature.value': {$lt: -15} },
                                {'airTemperature.value': {$gt: 30} }]}
                    ]
                }
    }, 
    {
        $project: {_id:0,
                    st:1,
                    callLetters:1,
                    airTemp: '$airTemperature.value',
                    windSpeed: '$wind.speed.rate'
                }}
]);








// 3.2 Build a query to help your local meteorologist.
// You’ll need to pull all readings that have a dew point value between 10 and 20 
//    and an air temperature value less than or equal to 15 degrees. 
//    The data should also be limited to readings with a visibility distance of less than 5000. 
//    Display the data in a JSON view.
db.data.aggregate([
    {
        $match: {
                'dewPoint.value': {$gte: 10, $lte:20},
                'airTemperature.value': {$lte: 15},
                'visibility.distance.value': {$lte: 5_000}
                }
    },
    {
        $project: {
                    _id: 0 //didn't specify columns, including all but _id
                  }
     }
]);




