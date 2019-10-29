const {Client}= require('elasticsearch')
var AWS = require('aws-sdk');

var region = 'us-east-1';
//var domain = 'https://search-red-7pbocoy2q5ikdw7dsb6j3a3amu.us-east-1.es.amazonaws.com';
//var domain = 'https://search-marble-elasticsearch-test-e3urdt7kb667o7verxgn6bjoee.us-east-1.es.amazonaws.com'


async function run () {

  var es = new AWS.ES({region: 'us-east-1'});
  // es.listDomainNames(function(err, data) {
  //   if (err) console.log(err, err.stack); // an error occurred
  //   else     console.log(data);           // successful response
  // });
  
  var params = {
    DomainName: 'marble-elasticsearch-test' /* required */
  };
  var es_endpoint = '';
  results = await es.describeElasticsearchDomain(params).promise();
  es_endpoint = 'https://' + results['DomainStatus']['Endpoint']
  // const options = {
  //     host: domain,
  //     port:443,
  //     protocol:'https',
  //     connectionClass: require('http-aws-es'),
  //     awsConfig: new AWS.Config({ region })
  // };
  // const client = Client(options);
  
  const options = {
    host: es_endpoint
  }
  const client = Client(options);

  const index_settings = {'number_of_shards': 1, 'number_of_replicas': 1}
  const index_mappings = {'properties':{'character':{'type':'text',},'quote':{'type':'text',},'season':{'type':"integer",}}}

  // Let's start by indexing some data
  await client.index({
    index: 'game-of-thrones',
    // type: '_doc', // uncomment this line if you are using Elasticsearch ≤ 6
    body: {
      settings: index_settings,
      mappings: index_mappings,
      character: 'Ned Stark',
      quote: 'Winter is coming.',
      season: 1
    }
  })

  await client.index({
    index: 'game-of-thrones',
    // type: '_doc', // uncomment this line if you are using Elasticsearch ≤ 6
    body: {
      settings: index_settings,
      mappings: index_mappings,
      character: 'Daenerys Targaryen',
      quote: 'I am the blood of the dragon.',
      season: 2
    }
  })

  await client.index({
    index: 'game-of-thrones',
    // type: '_doc', // uncomment this line if you are using Elasticsearch ≤ 6
    body: {
      settings: index_settings,
      mappings: index_mappings,
      character: 'Tyrion Lannister',
      quote: 'A mind needs books like a sword needs a whetstone.',
      season: 3
    }
  })

  // here we are forcing an index refresh, otherwise we will not
  // get any result in the consequent search
  await client.indices.refresh({ index: 'game-of-thrones' })

  // Let's search!
  const body = await client.search({
    index: 'game-of-thrones',
    // type: '_doc', // uncomment this line if you are using Elasticsearch ≤ 6
    body: {
      query: {
        match: { quote: 'Winter'}
      }
    }
  })

  console.log(body.hits.hits)


  //Delete all docs under this index
  const del = await client.deleteByQuery({
    index: 'game-of-thrones',
    // type: '_doc', // uncomment this line if you are using Elasticsearch ≤ 6
    body: {
        query: {
          match_all: {}
        }
    }
  }, function (error, response) {
      console.log(response);
  });
}

//console.log("NOT DOING WORK")
run().catch(console.log)