# printscrape
This script downloads random screenshots from https://prntscr.com/ (a.k.a. Lightshot)

You can set the number of threads by specyfying the -t (--threads) argument. It is 5 by default.

You can specify a charset mask for links generating with the argument -c (--charset). Here are the rules of making a mask:
* the number of chars for one link is 6
* every character is placed within curly brackets ("{}") 
* possible wildcards: ?d - [0-9], ?s - [a-z], ?a - [0-9a-z]
* you can also set a letter, a number, or the range of numbers or letters in curly brackets (possible examples: {a-d0-5}, {a0-9},{a0},{0-1f})
* you must place each character specification one by one like this: {d}{?s}{?s}{?a}
* you may omit characters in the mask, specifying only few of them; others will be fully random ("?a")
