local usernames = {}
local file = io.open("usernames.txt", "r")
for line in file:lines() do
    usernames[#usernames + 1] = line
end
file:close()

request = function()
    local idx = math.random(1, #usernames)
    local path = "/users/" .. usernames[idx]
    return wrk.format("GET", path)
end
