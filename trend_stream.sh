curl -X DELETE http://192.168.11.25:9200/mylist?pretty
{
  "acknowledged" : true
}


curl -XPUT XX.XX.XX.XX:9200/mylist/ -d '
{
  "settings":{
     "index":{
        "analysis":{
           "tokenizer" : {
               "kuromoji" : {
                  "type" : "kuromoji_tokenizer"
               }
           },
           "analyzer" : {
               "japanese" : {
                   "type" : "custom",
                   "tokenizer" : "kuromoji"
               }
           }
        }
     }
  },
  "mappings":{
    "tweet":{
      "properties":{
        "created_at" : {
          "type" : "date",
          "format" : "strict_date_optional_time||epoch_millis"
        },
        "text" : {
          "type" : "string",
          "analyzer": "japanese"
        },
        "track": {
          "type": "string",
          "index": "not_analyzed"
        }
      }
    }
  }
}'
