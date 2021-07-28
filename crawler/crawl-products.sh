scrapy crawl --set FEED_EXPORT_ENCODING=utf-8 get-urls -O urls.csv
scrapy crawl --set FEED_EXPORT_ENCODING=utf-8 smartphones -O products.jl
scrapy crawl --set FEED_EXPORT_ENCODING=utf-8 qa-smartphones -O qa.jl
mv products.jl products.ndjson
mv qa.jl qa.ndjson