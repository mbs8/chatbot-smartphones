#scrapy crawl --set FEED_EXPORT_ENCODING=utf-8 get-urls -O data/urls.csv
scrapy crawl --set FEED_EXPORT_ENCODING=utf-8 smartphones -O data/products.jl
scrapy crawl --set FEED_EXPORT_ENCODING=utf-8 qa-smartphones -O data/qa.jl
mv data/products.jl data/products.ndjson
mv data/qa.jl data/qa.ndjson