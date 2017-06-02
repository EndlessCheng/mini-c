even = 0
odd = 0
i = 1
while i < 10 {
    print i
    if i % 2 == 0 {
        even = even + i
    } else {
        odd = odd + i
    }
    print "even"
    print even
    print "odd"
    print odd
    i = i + 1
}
print even
print odd
