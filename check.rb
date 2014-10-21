users = Hash.new { |h,k| h[k] = []}
size = 0
File.readlines("dataset/lastfm/base_listens.dat").each do |line|
    splitted = line.split(',')
    users[splitted[0]] << splitted[1]
    size += 1
end

puts users.keys.size
#puts sum
#puts users.keys.size
#puts sum.to_f / users.keys.size

#puts users.map { |user_id, hash| hash.keys.size }.sort.uniq
