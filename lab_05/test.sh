wrk -t10 -c10 -d15s --latency -s get_nocache.lua http://localhost:8000
wrk -t10 -c10 -d15s --latency -s get_cache.lua http://localhost:8000