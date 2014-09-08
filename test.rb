require 'twitter'
client = Twitter::Streaming::Client.new do |config|
    config.consumer_key        = "6clMQc5LA3irCE7JSgM3AC0jL"
    config.consumer_secret     = "vDFGq7hrwrUgTfRmvui59dMdABNtGg1lwaN14SMdphvMyBToTv"
    config.access_token        = "27039781-0mljdsIiAZ0EV6ZqsLJXCOKjuhLrwZ3xFCUx4269"
    config.access_token_secret = "r9T1w5ENSGpP9KBnApqTEsaXWe0Ja49TTw20NR4h416GS"
end

client.sample do |object|
      puts object.text if object.is_a?(Twitter::Tweet)
end
