All those are suppose to be in the Mongo Shell:

## Select a database
    use sample_airbnb

## Find entries
    db.listingsAndReviews.find({    
        }).limit(5).pretty();

## Find entries with critera
    db.listingsAndReviews.find({
        beds:5    
    }).limit(5).pretty();


## Insert
    db.notecards.insert({
        'title':'My first note',
        'content':'The quick brown fox jumps over the lazy dog',
        'tags':'important'
    });

    db.listingsAndReviews.find({
        //empty object mean to find everything
    }),{name:1,
    description:1
    }).limit(5).pretty()

    select from listing and only the name,number of bedroom and bathroom
    db.listingsAndReviews.find({

    },{name:1,
    bedrooms:1,
    bathrooms:1
    }).limit(5).pretty()

    Find all listings that have 2 bedrooms:
    db.listingsAndReviews.find({
        bedrooms:2
    },{name:1,bedrooms:1}).limit(10).pretty()

    Find all listings that has property_type of apartments
    db.listingsAndReviews.find({
        property_type:'Apartment'
    },{name:1,property_type:1,bedrooms:1}).limit(10).pretty()

    Find all listings that are aprtments and have 2 bedrooms

    db.listingsAndReviews.find({
        property_type:'Apartment',
        bedrooms:2
    },{name:1,property_type:1,bedrooms:1}).limit(10).pretty()

    Find all the listing with two bathrooms and is a private room
    db.listingsAndReviews.find({
        room_type:'Private room',
        bedrooms:2
    },{name:1,room_type:1,bedrooms:1}).limit(10).pretty()

    Find listings by substring

    similiar to `SELECT * FROM employees WHERE jobTitle LIKE %sales%

    db.listingsAndReviews.find({
        name:{$regex:'nice room'},$option:'i'}
    },{name:1}).limit(10).pretty();

    ###critera with a range

    Similiar to `SELECT*FROM students WHERE score >=50 aAND score<=30`

    Find all listings that have more than 2 bedrooms
    db.listingsAndReviews.find({
        bedrooms:{
            $gt:2
        }
    },{name:1,bedrooms:1}).limit(10).pretty()

    we use `gt` for greater than, `gte` for greater than or equal
    we use `lt` for lesser than,`lte` for lesser than or equal
    
    Find all listings that have 2 or 3 bedrooms:

    db.listingsAndReviews.find({
        bedrooms:{
            $gte:2,
            $lte:3
        }
    },{name:1,bedrooms:1}).limit(10).pretty()

    # Find all listings that have 2 or 3 bedrooms and have 2 or mnore bathrooms

    db.listingsAndReviews.find({
        bedrooms:{
            $gte:2,
            $lte:3
        },
        bathrooms:{
            $gte:2
        }
    },{name:1,bedsrooms:1,bathrooms:1}).limit(10).pretty()

Find all listings tha are in canada

db.listingsAndReviews.find({
    'address.country':'Canada'
},{name:1,'address.country':1}).limit(10).pretty()

db.listingsAndReviews.find({
    'host.host_listings_count':{
        $gt:2
    }
},{name:1,'host.host_listings_count':1}).limit(10).pretty()

### Find by an item in an array
    db.listingsAndReviews.find({
        amenities:'Hot tub'
    },{name:1,amenities:1}).limit(5).pretty()

### Find listings that have wifi and laptop friendly workspace

db.listingsAndReviews.find({
    amenities:{
        $all:['Wifi','Laptop friendly workspace']
    }
},{name:1,amenities:1}).limit(5).pretty()


Find listings that have a doorman OR that the host greets you
db.listingsAndReviews.find({
    amenities:{
        $in:['Doorman','Host greets you']
    }
},{name:1,amenities:1}).limit(5).pretty()

## GROUP by

    db.listingsAndReviews.aggregate([
        {$group:{
                _id:'$property_type',
                count:{
                    $sum:1
                }
        }}
    ]);

a)
db.movies.find({

}).count()

b)
db.movies.find({
    year:{
    $lt:2000
    }
}).count()

c)
db.movies.find({
    'countries':['USA']
},{title:1,countries:1}).limit(10).pretty()

d)

db.movies.find({
    'countries':{
        $nin:['USA']
    }
},{title:1,countries:1}).limit(10).pretty()

e)
db.movies.find({
    'awards.wins':{
        $gte:3
    }
},{title:1,'awards.wins':1}).limit(10).pretty()

f)
db.movies.find({
    'awards.nominations':{
        $gte:3
    }
},{title:1,'awards.nominations':1}).limit(10).pretty()



g)
db.movies.find({
    'cast':'Tom Cruise'  `this will give us the movie that tom cruise is in it`
    
},{title:1}).limit(10).pretty()

h)
db.movies.find({
    'directors':'Charles Chaplin'
    
},{title:1}).limit(10).pretty()

3a)
db.theaters.find({
    'location.address.state':'AZ'
    
},{theaterId:1,'location.address.state':1}).pretty()

