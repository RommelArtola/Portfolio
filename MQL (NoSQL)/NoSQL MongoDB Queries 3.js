// Use the sample_weatherdata and the data collection.
use sample_weatherdata
// 1.1  In Module 4 we created a .find() query for the following query. 
// Your task here is to convert that result to a .aggregate() query AND optimize the process 
// using aggregate stages.

db.data.aggregate([ //Optimized via a single match stage/statement...
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




// 1.2 Build a query that filters out the bad data, like you did in the last query.
    // Have the query calculate the average temperature and wind speed for each call letter, 
    // and then present the three columns with professional field names (not _id) 
    // and sort the whole data set by the call letters. (10 points)
    
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
        $group: {
                _id: '$callLetters',
                avgWindSpeed: {$avg: '$wind.speed.rate'},
                avgTemp: {$avg: '$airTemperature.value'}
                }
    },    
    {
        $project: {
                    _id: 0,
                    callLetters: '$_id',
                    avgWindSpeed:1,
                    avgTemp:1
                    }
        },  
    {
        $sort: {callLetters: 1}
    }
]);





// Using the Sample_mflix and movies collection
use sample_mflix
// 2.1 This is going to be a filtering query, using $match. Should result in 20.
db.movies.aggregate([
    {
        $match: {
            $and: [
                  { 'genres': {$in: ['Drama', 'Family'] } },
                  { 'genres': {$ne: 'Short' } },
                  { 'year' : {$gte: 1972, $lte: 1982} },
                  {
                      $or: [
                            {$and: [{'imdb.rating': {$gte: 8.5}}, {'imdb.votes': {$gt: 100}}]},
                            {$and: [{'imdb.rating': {$gte: 9.0}}, {'imdb.votes': {$gt: 200}}]},
                            ]
                   }
                  
                   ]
            }

    },
    {
        $project: {
                    _id:0,
                    title:1,
                    type:1,
                    year:1,
                    'imdbRating': '$imdb.rating',
                    'imdbVotes': '$imdb.votes',
                    'firstGenre': { $arrayElemAt: ['$genres', 0] },
                    'secondGenre': { $arrayElemAt: ['$genres', 1] },
                    'thirdGenre': { $arrayElemAt: ['$genres', 2] },
                    }
    }

]);






// 2.2 Use the sample_supplies database and the sales collection.
use sample_supplies

db.sales.aggregate([
    //Unwinding to flatten
    {
        $unwind: '$items'      
    },
    //Matching/Filtering
    {
        $match: {
                    'items.tags': { $in: ['stationary', 'writing', 'school'] } 
                } 
     },
   //Grouping to get sums/aggregates
   {
       $group: {
                  _id: '$items.name', //aggregation value
                  'quantitySold': { $sum: '$items.quantity' },
                  'salesSum': { $sum: {$multiply: ['$items.quantity', '$items.price'] } }, //sums the product
                  'orderCount': {$sum: 1} //counting the transaction count 
                  
               }
   },
    {
        $project: {
                    _id:0,
                    itemName: '$_id',
                    sales: {
                        Qty: '$quantitySold',
                        Sales:  '$salesSum',
                        Transactions: '$orderCount'
                    }
                   }
     }
]);






// 2.3 Export the results of 2.2 to a separate file.
//Done.
