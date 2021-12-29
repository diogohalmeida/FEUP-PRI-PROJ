const SolrNode = require("solr-node");
const express = require("express");

var client = new SolrNode({
    host: "127.0.0.1",
    port: "8983",
    core: "books",
    protocol: "http"
})


const router = express.Router();

router.get("/", function(req, res) {
    console.log("Basic web page")
    res.render("index");
})

router.get("/search", (req,res) => {
    const search = req.query["query"];

    const searchQuery = client.query()
    .qop("OR")
    .q(search)
    .addParams({
        wt:"json",
        indent: true,
    }).edismax()
    .mltQuery("qf=" + ["title%5E5","author%5E3","series%5E3","description%5E1"].join("%20"))

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
        
        res.render("book", {data: {
            book: response.docs[0]
            }
        })
    })
    
})


module.exports = router