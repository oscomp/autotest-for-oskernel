import sys

testcase = 'test2'

std_ans = [
    '[test2]free heap size is'
]

def test(output):
    ans = []
    score = 0
    test_log = open("/coursegrader/testdata/input/"+testcase +"_log","w+")
    with open(output, 'r') as ans_file:
        for line in ans_file:
            if '[test2]' in line:
                ans.append(line)
    std_size = len(std_ans)
    ans_size = len(ans)
    count = 0
    for i in range(0,std_size):
        if(i >= ans_size):
            test_log.write("We expect more output")
            break
        if std_ans[i] in ans[i][0:-1]:
            test_log.write("Accept:"+ans[i])
            count = count + 1
        else:
            test_log.write("Expect:\""+std_ans[i]+"\"--but we get:\""+ans[i][0:-1]+"\"\n")
    if count == std_size:
        score += 100
    if std_size < ans_size:
            test_log.write("Redundant output")
    print(score)
    test_log.close()
    ans_file.close()
    return score

if __name__ == '__main__':
    test(sys.argv[1])
