title: Regex golf at regex.alf.nu
published: 2014-02-02

In this blog post I will summarize some cool and interesting "solutions" to the
regular expression challenges at <http://www.regex.alf.nu/>. I write solutions
inside quotation marks because to some of the levels there are better solutions
found, but there may also be even better unknown solutions.

I have found many of the solutions in the comments to this Github Gist:
<https://gist.github.com/jpsim/8057500>.  It's a fun game, and I enjoy reading
what tricks other people have come up with. I'm not a regex l33t by any means,
but I think this game is a fun way to see what nifty things you can accomplish
with regex. There is also a discussion thread [at Hacker
News](https://news.ycombinator.com/item?id=6941231) about the game.

If you need to brush up your regular expression skills, check out Mozilla
Developer Network's [article on the
subject](https://developer.mozilla.org/en/docs/Web/JavaScript/Guide/Regular_Expressions).

I also found a cool regex visualizer on <http://regexp.quaxio.com/>.

And by the way, if you can't get enough of golf, there is also a very well-made
game called [Vim Golf](http://vimgolf.com/).

1. Plain Strings
----------------

The solution to this level is simply `foo`, which earns you 207 points.

2. Anchors
----------

All words in the left column end with the letter k. Therefore the level is
simply won with `k$`, giving you 208 points.

3. Ranges
---------

The left column's words only contain the letters a to f. Writing this with a
regex yields `^[a-f]+$` and scores us 202 points.

4. Backrefs
-----------

All words in the left column follow a pattern where three letters in sequence
appear two times within the word. For example **barbar**y and
**hea**vy**hea**ded.

Selecting strings following this pattern can be made with the regex
`(...).*\1`, worth 201 points.

5. Abba
-------

Here we want to select words that *don't* contain letter sequences looking like
an**alla**gmatic, hippogr**iffi**n and uncl**assa**bly. Therefore we will use
`?!` in regex to negate our selection.

Here is a solution using negation: `^(?!.*(.)(.)\2\1)`, worth 193 points. I
found this solution in [this Stack Overflow
answer](http://stackoverflow.com/a/20774803/595990).

As a side note, we can't simply write `(?!(.)(.)\2\1)`, because `x(?!y)` really
means "select x only if it isn't followed by y." In our case: "select the start
`^` only if isn't followed by the pattern inside the parenthesises."

6. A man, a plan
----------------

Here the mission is to match palindromes, even if it isn't possible as
described in [this Stack Overflow
answer](http://stackoverflow.com/a/247933/595990).

However, it's possible to match palindromes of limited length, in this case
with `^(.?)(.?)(.?).?\3\2\1$`, worth 168 points.

An even better solution is `^(.)[^p].*\1$`, worth 177 points. The main part to
understand is `^(.).*\1$` which matches words that start and end with the same
letter, as palindromes obviously do. Since only the word sporous from the right
column starts and ends with the same letter, we filter it out with `[^p]`.

7. Prime
--------

A very cool solution to this level is `^(?!(..+?)\1+$)`, worth 285 points. What
it will do is to match a number of x:es that is a multiple of two numbers, i.e.
not a prime number. Then it negates the result, yielding us a selection of all
strings from the left column.

8. Four
-------

The pattern here is a letter repeated four times with one other letter between
each of the pairs. For example M**a**k**a**r**a**k**a** and
odont**o**n**o**s**o**l**o**gy. Regex to match this pattern: `(.).\1.\1.\1`,
worth 198 points.

To save a letter and score an additional point, use `(.)(.\1){3}`.

9. Order
--------

When you think about it, a fairly obvious solution to this level is

    :::text
    ^a*b*c*d*e*f*g*h*i*j*k*l*m*n*o*p*q*r*s*t*u*v*w*x*y*z*$

as answered [on Stack Overflow](http://stackoverflow.com/a/14343382/595990),
giving us 156 points.

A slightly trimmed down version, without the unused letters, is worth 166
points and looks like:

    :::text
    ^a*b*c*d*e*f*g*h*i*k*l*m*n*o*p*r*s*t*w*y*z*$

A cool cheat I found to this level is `^[^o].....?$`, worth 198 points. This
works because the words in the left column are only 5 or 6 letters long in
constrast to the right column's words which are at least 7 letters long except
for oriole. oriole is filtered out with `[^o]`.

10. Triples
-----------

This is probably the hardest level. The goal is to write a regular expression
that matches multiples of 3. I found [a blog
post](http://quaxio.com/triple/) describing how this problem can be written as
a finite state machine. The huge solution the author ends up with is

    :::text
    ^([0369]|[258][0369]*[147]|[147]([0369]|[147][0369]*[258])*[258]|[258][0369]*[258]([0369]|[147][0369]*[258])*[258]|[147]([0369]|[147][0369]*[258])*[147][0369]*[147]|[258][0369]*[258]([0369]|[147][0369]*[258])*[147][0369]*[147])*$

This yields us 401 points.

But there is apparently a short, little cheat

    :::text
    00($|3|6|9|12|15)|4.2|.1.+4|55|.17

that is worth 596 points.

11. Glob
--------

Short little 397 points cheat: `[bncrw][bporn]|^p|c$|ta`

12. Balance
-----------

When a tag is opened with `<` it needs to be properly closed with `>`. A regex
for this is:

    :::text
    ^(<(<(<(<(<(<<>>)*>)*>)*>)*>)*>)*$`

286 points will this give us.

13. Powers
----------

A first solution, worth 45 points, is:

    :::text
    ^(x|xx|xxxx|x{8}|x{16}|x{32}|x{64}|x{128}|x{256}|x{512}|x{1024})$

With the following clever solution we will get 56 points:

    :::text
    ^((((((((((x)\10?)\9?)\8?)\7?)\6?)\5?)\4?)\3?)\2?)\1?$

However, I saw an even more clever and nifty solution worth 80 points:

    :::text
    ^(x|(xx){1,8}|x{32}|(x{64})+)$

14. Long count & 15. Long count v2
----------------------------------

To match the complete string in the left column, we can use the regex worth 253
points `((.+)0 ?\2[1]){8}`. However, we can skip the space and question mark in
the middle of the regex, which will score us two additional points but won't
match the complete left string. This yields us `((.+)0\2[1]){8}`. The regex
will basically match pairs of 4 digit sequences where only the last digit
changes, like in the case of 101**0** 101**1**.

16. Alphabetical
----------------

My solution, worth only 50 points:

    :::text
    ^(ae\w+ )*(as\w+ )*(ar\w+ )*(ea\w+ )*(en\w+ )*(er\w+ )*(es\w+ )*(rea\w+ )*(ren\w+ )*(rer\w+ )*(rese\w+ )*(rest\w+ )*(ret\w+ )*(sea\w+ )*(sen\w+ ?)*(ser\w+ )*(snarer ?)*(sta\w+ )*(strata )*(street)*(tan\w+ )*(tar\w+ ?)*(tas\w+ )*(teaser ?)*(tester)*(ten\w+ ?)*(tester )*(testes ?)*(tsetse)*$

It only works for this case, it's very long and it's ugly.

A pretty nifty and complex cheat, worth 286 points, is:

    :::text
    ^(?!.* ((.*)t.* \2[es]|(.*)s.* \3[nr]|(.*)r.* \4[en]))

However, AlanDeSmet on Github has [this
solution](https://gist.github.com/jpsim/8057500/#comment-983028):

    :::text
    ^(?!.*\b((.*)b.*\b\2[a]|(.*)c.*\b\3[ab]|(.*)d.*\b\4[a-c]|(.*)e.*\b\5[a-d]|(.*)f.*\b\6[a-e]|(.*)g.*\b\7[a-f]|(.*)h.*\b\8[a-g]|(.*)i.*\b\9[a-h]|(.*)j.*\b\10[a-i]|(.*)k.*\b\11[a-j]|(.*)l.*\b\12[a-k]|(.*)m.*\b\13[a-l]|(.*)n.*\b\14[a-m]|(.*)o.*\b\15[a-n]|(.*)p.*\b\16[a-o]|(.*)q.*\b\17[a-p]|(.*)r.*\b\18[a-q]|(.*)s.*\b\19[a-r]|(.*)t.*\b\20[a-s]|(.*)u.*\b\21[a-t]|(.*)v.*\b\22[a-u]|(.*)w.*\b\23[a-v]|(.*)x.*\b\24[a-w]|(.*)y.*\b\25[a-x]|(.*)z.*\b\26[a-y]))

He writes:

> **Alphabetical (-109) "Pure" solution:** Should work for any number of words
> of any length limited to characters [a-z]. I haven't even considered the case
> where the words are of varying lengths, but my brain is done for tonight. But
> by my own standards, this is a cheat-free solution, and I haven't seen any
> others that meet that standard. Pity that it scores so abysmally.
