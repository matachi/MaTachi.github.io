title: Solutions to the wargame XSS Challenges at xss-quiz.int21h.jp  
published: 2013-11-28

In this blog post I will describe how to solve (most of) the stages in the XSS
(cross-site scripting) wargame XSS Challenges at <http://xss-quiz.int21h.jp/>.
The only tool I will use is the trusty Firefox.

Stage #1
--------

The server will in its response output the search term into the HTML page.
Simply post

    :::html
    <script>alert(document.domain);</script>

and we will finish stage #1.

Stage #2
--------

This time the server won't put the search term directly into the page. Instead
it will be inserted into the input's value attribute. Therefore we will need to
post

    :::html
    "><script>alert(document.domain);</script>

to first close the input element.

Stage #3
--------

The server is now properly escaping tags (`>` and `<`) from the text field.
Therefore posting

    :::html
    <script>alert(document.domain);</script>

won't do. Even though the select widget has a fixed set of options (Japan,
Germany, USA and United Kingdom), there isn't really anything preventing us
from selecting and posting whatever value we want. Right-click the select
widget and choose *Inspect Element* from the context menu. Then in Firefox's
Inspector tool, double-click the text for one of the options and change it to
JavaScript code above. Put something in the text field and submit the form and
finish the stage.

Stage #4
--------

Right-click in the form and select *Inspect Element* from the context menu to
show Firefox's Inspector tool. Find the hidden input field with the name `p3`.
The default value for this field is `hackme`. In the response from submitting
the form to the server this field's submitted value will be kept. What we want
to do is to submit

    :::html
    "> <script>alert(document.domain);</script>

to the server, since that will break out from the input field and insert the
script into the page.  However, trying to insert that into the input field's
value attribute with Firefox's Inspector tool won't work, because of the `"`
character at the beginning. Instead, insert

    :::html
    &#34> <script>alert(document.domain);</script>

into the attribute's value field (with the `"` character escaped to `&#34`).
Escaping ASCII characters can easily be done through this character encoding
calculator: <http://ha.ckers.org/xsscalc.html>.

Stage #5
--------

The input field's max length limit is just an artificial limit set in the HTML
and nothing that is enforced on the server-side. Simply increase `maxlength` to
something larger than 15 using Firefox's DOM Inspector tool and submit

    :::html
    "> <script>alert(document.domain);</script>

Stage #6
--------

On this stage the tags `>` and `<` are properly escaped on the server to `&gt;`
and `&lt;`. But the rest of the characters aren't. By submitting

    :::html
    123" onmouseover="alert(document.domain);

the input's value attribute will in the response be filled with `123`. But the
element will also have an additional attribute that will show the alert window
when hovering the mouse cursor over the field.

Stage #7
--------

The server is now also escaping quotation marks, like `"` and `'`. However,
they missed to put quotes characters around the input's `value` attribute's
value, meaning that we still easily can add an additional attribute to the
element. By posting

    :::html
    a onmouseover=alert(document.domain);

, `a` will be the field's value and the additional element attribute will be
`onmouseover`. This works because it's not a requirement to put quotes around
an attribute value in HTML.

Stage #8
--------

On this stage we need to take advantage of a technique that was used in the
old, dark days of HTML to make clickable links that executed JavaScript and
didn't leave the page. The solution to this stage is to submit the link

    :::html
    javascript:alert(document.domain);

Christian Heilmann is ranting on these `javascript:` links, among other things,
in his blog post [Perpetuating terrible javaScript
practices](http://christianheilmann.com/2013/10/31/perpetuating-terrible-javascript-practices/).

Stage #9
--------

Solving this stage won't work in any modern browser since it's dependent on
support for UTF-7. The XSS attack is described on [OWASP's wiki
site](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet#UTF-7_encoding>).
Support for [UTF-7 was completely removed from
Firefox](https://bugzilla.mozilla.org/show_bug.cgi?id=414064) several years ago
(per HTML5 spec).

To cheat/skip this stage, open Firefox's Web Console and execute
`alert(document.domain);`. This will show the alert which will trigger the
congratulations message.

Stage #10
---------

Try to submit `adomainbdomain123` and you will see that `ab123` is returned.
It's obvious that the server is removing any instance of the word `domain` from
the search query. A logical solution is to obfuscate the JavaScript expression.

Start with converting `alert(document.domain);` to Base64 with the [Character
Encoding Calculator](http://ha.ckers.org/xsscalc.html) we previously used. Via
the Stack Overflow question [Base64 encoding and decoding in client-side
Javascript](http://stackoverflow.com/q/2820249/595990) we find that all modern
browsers have a global function galled `atob()` to decode Base64 strings, [read
more on Mozilla Developer
Network](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Base64_encoding_and_decoding).
To execute a string as JavaScript, use
[eval()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval).
The result that we will submit is:

    :::html
    "><script>eval(atob('YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ=='));</script>

Stage #11
---------

Since the words `script`, `style` and `on` aren't allowed, we have to think
about something else this time. Apparently it's possible to encode JavaScript
as Base64 and make it execute as an iframe src. From the Stack Overflow
question [Is it possible to "fake" the src attribute of an
iframe?](http://stackoverflow.com/a/3462800/595990) we can read that it's
possible to do:

    :::html
    <iframe src="data:text/html;base64, .... base64 encoded HTML data ....">

Read more about [data URIs on Mozilla Developer
Network](https://developer.mozilla.org/en-US/docs/data_URIs). The HTML data we
want to use is:

    :::html
    <script>parent.alert(document.domain);</script>

`parent.` is needed because we want the alert to execute in the context of the
parent's window. Encoding it as Base64 with the [Character Encoding
Calculator](http://ha.ckers.org/xsscalc.html) results in:

    PHNjcmlwdD5wYXJlbnQuYWxlcnQoZG9jdW1lbnQuZG9tYWluKTs8L3NjcmlwdD4

The code that we will then put into the search box to finish the level is:

    :::html
    "><iframe src="data:text/html;base64,PHNjcmlwdD5wYXJlbnQuYWxlcnQoZG9jdW1lbnQuZG9tYWluKTs8L3NjcmlwdD4="></iframe>

Stage #12
---------

This is yet another level that doesn't seem to work, at least not in a modern
version of Firefox. According to [this
thread](http://sla.ckers.org/forum/read.php?2,24209) a working solution should
be:

    :::html
    ``/onfocus=alert(document.domain)

`` ` `` should work as a substitute for `"` and `/` should work as a delimiter.
This [xss_quiz.txt
document](http://blog.knownsec.com/Knownsec_RD_Checklist/xss/xss_quiz.txt)
suggests that this is a working soultion:

    :::html
    ``onmouseover=alert(document.domain);

However, neither work for me, so I can only assume that this XSS attack doesn't
work any longer. At the first stage of the game it's even written that some
stages only works in IE, and perhaps this is one of them.

To skip the stage, execute `alert(document.domain);` in Firefox's console.

Stage #13
---------

Neither this stage seems to work. On
[OWASP](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet#DIV)
there are some suggestions to put into a style attribute, however they won't
work for me. The
[xss_quiz.text](http://blog.knownsec.com/Knownsec_RD_Checklist/xss/xss_quiz.txt)
file suggests that the following should work:

    :::html
    background-color:#f00;background:url("javascript:alert(document.domain);");

I assume this is also something thas has been fixed.

Stage #14
---------

The point on this stage is also to inject JavaScript through a style attribute,
so I assume this neither will work, as the previous stage.

Stage #15 & Stage #16
---------------------

Unsure if these two work. We are supposed to inject JavaScript through
`document.write()`, but I can't find anything that works.

Stage #19
---------

This stage's vulnerability is the same one that Twitter once had, read more in
the blog post [A Twitter DomXss, a wrong fix and something
more](http://blog.mindedsecurity.com/2010/09/twitter-domxss-wrong-fix-and-something.html).
However, appending

    :::html
    #!javascript:alert(document.domain);

to the URL doesn't work for me. I'm only redirected to

    http://xss-quiz.int21h.jp/javascriptalert(document.domain);

For further reading, OWASP has a really good article on [DOM Based
XSS](https://www.owasp.org/index.php/DOM_Based_XSS).

Conclusion
----------

The first ~11 stages were really fun as problem solving challenges. The latter
ones were a little wonky, I guess it's because this wargame has some years on
its neck.

If you have any tips, suggestion on better or alternative, interesting XSS code,
or solutions to the stages I didn't manage to solve, please leave a comment
below.
