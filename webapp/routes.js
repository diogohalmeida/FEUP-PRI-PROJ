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
    console.log("Basic web page")
    res.render("index");
})

router.post

router.get("/search", (req,res) => {
    const search = req.query["query"];
    let queryFields = []

    for (field in req.query){
        if(field == "query")
            break
        queryFields.push(field + "%5E" + req.query[field])
    }

    const searchQuery = client.query()
    .qop("OR")
    .q(search)
    .addParams({
        wt:"json",
        indent: true,
    }).edismax()
    .mltQuery("qf=" + queryFields.join("%20"))

    client.search(searchQuery, function(err, result){
        if (err) {
            console.log(err)
            return
        }
        const response = result.response

        res.render("index", {data: {
            userQuery: search,
            books: response.docs
            }
        })
    })

})

router.get("/book/:id", (req, res) => {

    const book_id = req.params.id

    const searchQuery = client.query().q('id:' + book_id)

    client.search(searchQuery, function(err, result){
        if (err) {
            console.log(err)
            return
        }
        const response = result.response
        console.log(response.docs)
        recommended_books_q = response.docs[0]["recommended_books"].replaceAll(","," id:")
        recommended_books_q = "id:" + recommended_books_q
        const searchQueryRB = client.query()
        .qop("OR")
        .q(recommended_books_q)
        .addParams({
            wt:"json",
            indent: true,
        })

        client.search(searchQueryRB, function(err, resultRB){
            if (err) {
                console.log(err)
                return
            }
            const responseRB = resultRB.response
            books_in_series_q = response.docs[0]["books_in_series"].replaceAll(","," id:")
            books_in_series_q = "id:" + books_in_series_q
            const searchQueryBIS = client.query()
            .qop("OR")
            .q(books_in_series_q)
            .addParams({
                wt:"json",
                indent: true,
            })

            const reviewsQuery = reviewsClient.query().q('book_id:' + book_id)

            reviewsClient.search(reviewsQuery, function(err, reviewsResult){
                if (err){
                    console.log(err)
                    return
                }

                const reviewsResponse = reviewsResult.response

                client.search(searchQueryBIS, function(err, resultBIS){
                    if (err) {
                        console.log(err)
                        return
                    }
                    const responseBIS = resultBIS.response
                    res.render("book", {data: {
                        book: response.docs[0],
                        recommended_books: responseRB.docs,
                        books_in_series: responseBIS.docs,
                        reviews: reviewsResponse.docs
                        }
                    })
                })
            })
            
        })

        
    })
    
})


module.exports = router