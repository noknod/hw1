


def read_dirs_file(file_path):
    answer = []
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            line = line.strip()
            if len(line) != 0:
                answer.append(line.strip())
    return set(answer)


f = read_dirs_file('./new_facebook_users.txt')

s = read_dirs_file('./signup.txt')

#print len(f), len(s)

good = []
for row in s:
    if row in f:
       #print row
       good.append(row)

print 1.0 * len(good) / len(f)
