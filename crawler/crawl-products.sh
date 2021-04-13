scrapy crawl --set FEED_EXPORT_ENCODING=utf-8 smartphones -o products.jl
scrapy crawl --set FEED_EXPORT_ENCODING=utf-8 qa-smartphones -o qa.jl
mv products.jl products.ndjson
mv qa.jl qa.ndjson