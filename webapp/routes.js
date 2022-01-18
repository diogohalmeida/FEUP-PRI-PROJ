const SolrNode = require("solr-node");
const express = require("express");

var client = new SolrNode({
    host: "127.0.0.1",
    port: "8983",
    core: "books",
    protocol: "http"
})

var reviewsClient = new SolrNode({
    host: "127.0.0.1",
    port: "8983",
    core: "reviews",
    protocol: "http"
})


const router = express.Router();

router.get("/", function(req, res) {
    res.render("index")
})

router.get("/search", (req,res) => {
    if (req.query["query"] == "")
        search = "*";
    else
        search = req.query["query"];
    let queryFields = []
    let requestVariables = []

    for (field in req.query){
        if(field == "query" || field == "query_reviews" || field == "reviewAuthor")
            continue
        queryFields.push(field + "%5E" + req.query[field])
        requestVariables.push(field)
    }

    final_query = "qf=" + queryFields.join("%20")

    if("query_reviews" in req.query && req.query["query_reviews"] != "" && !("reviewAuthor" in req.query)){
        final_query += "&fq=%7B!join%20from%3Dbook_id%20fromIndex%3Dreviews%20%20to%3Did%7Dtext:" + req.query["query_reviews"].replace(/\s/g,"%20")
    }

    if("reviewAuthor" in req.query && req.query["reviewAuthor"] != ""){
        final_query += "&fq=%7B!join%20from%3Dbook_id%20fromIndex%3Dreviews%20%20to%3Did%7Duser:" + req.query["query_reviews"].replace(/\s/g,"%20")
        requestVariables.push("reviewAuthor")
    }

    const searchQuery = client.query()
    .qop("OR")
    .q(search)
    .addParams({
        wt:"json",
        indent: true,
    }).edismax()
    .mltQuery(final_query)

    client.search(searchQuery, function(err, result){
        if (err) {
            console.log(err)
            return
        }
        const response = result.response

        res.render("index", {data: {
            userQuery: search,
            books: response.docs,
            oldRequest: requestVariables
            }
        })
    })

})

function get_recommend_books(book, reviews, res){
    if(book["recommended_books"] != undefined){
        recommended_books_q = book["recommended_books"].replaceAll(","," id:")
        recommended_books_q = "id:" + recommended_books_q
        const searchQuery = client.query()
        .qop("OR")
        .q(recommended_books_q)
        .addParams({
            wt:"json",
            indent: true,
        })

        client.search(searchQuery, function(err, result){
            if (err) {
                console.log(err)
                return
            }
            const response = result.response

            get_books_in_series(book, reviews, response.docs, res)
        })
    }
    else{
        get_books_in_series(book, reviews, [], res)
    }
}

function get_books_in_series(book, reviews, recommended_books, res){
    if(book["books_in_series"] != undefined){
        let books_in_series_q = book["books_in_series"].replaceAll(","," id:")
        books_in_series_q = "id:" + books_in_series_q

        const searchQuery = client.query()
        .qop("OR")
        .q(books_in_series_q)
        .addParams({
            wt:"json",
            indent: true,
        })

        client.search(searchQuery, function(err, result){
            if (err) {
                console.log(err)
                return
            }
            const response = result.response

            res.render("book", {data: {
                book: book,
                recommended_books: recommended_books,
                books_in_series: response.docs,
                reviews: reviews
                }
            })
        })
    
    }
    else{
        res.render("book", {data: {
            book: book,
            recommended_books: recommended_books,
            books_in_series: [],
            reviews: reviews
            }
        })
    }
}

function get_reviews(book, res){
    const searchQuery = reviewsClient.query().q('book_id:' + book["id"])

    reviewsClient.search(searchQuery, function(err, result){
        if (err){
            console.log(err)
            return
        }

        const response = result.response

        get_recommend_books(book, response.docs, res)

    })
}

router.get("/book/:id", (req, res) => {

    const book_id = req.params.id

    const searchQuery = client.query().q('id:' + book_id)

    client.search(searchQuery, function(err, result){
        if (err) {
            console.log(err)
            return
        }


        const response = result.response

        get_reviews(response.docs[0], res)
               
    })
    
})


module.exports = router