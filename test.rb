require 'twitter'
client = Twitter::REST::Client.new do |config|
    config.consumer_key        = "6clMQc5LA3irCE7JSgM3AC0jL"
    config.consumer_secret     = "vDFGq7hrwrUgTfRmvui59dMdABNtGg1lwaN14SMdphvMyBToTv"
    config.access_token        = "327039781-0mljdsIiAZ0EV6ZqsLJXCOKjuhLrwZ3xFCUx4269"
    config.access_token_secret = "r9T1w5ENSGpP9KBnApqTEsaXWe0Ja49TTw20NR4h416GS"
end

client.search("to:justinbieber marry me", :result_type => "recent").take(500).collect do |tweet|
      puts "#{tweet.user.screen_name}: #{tweet.text}"
end

