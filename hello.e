even = odd = 0
i = 1
while i < 10 {
    log i
    if i % 2 == 0 {
        even = even + i
    } else {
        odd = odd + i
    }
    log even
    log odd
    i = i + 1
}
log even
log odd
log even + odd
log "" + (even + odd) * 100 + "%"
