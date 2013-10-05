title: POST to a WordPress JSON REST API from Python  
published: 2013-10-05

In this post I'm gonna show how you can create pages on a WordPress blog from a
Python script.

For this to work, you first have to install the plugin [JSON REST
API](http://wordpress.org/plugins/json-rest-api/) on your WordPress blog. We
will also use the Python library
[Requests](http://docs.python-requests.org/en/latest/index.html) to simplify
making HTTP requests. The [quickstart for
Requests](http://docs.python-requests.org/en/latest/user/quickstart/) contains
a lot of useful information to get started.

What we want to do is to make a [HTTP POST
request](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods)
to the REST API.

With curl installed (`sudo apt-get install curl`) we can make a HTTP POST against the API in the following way:

    :::sh
    curl -v -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"title":"Title","content":"Content","type":"page"}' http://localhost/wp-json.php/posts -u admin:password

This where I found the [curl command
above](http://stackoverflow.com/a/5658904/595990).

Using curl with the verbose
argument (`-v`) is a good way to perform HTTP debugging, for example to see how
a REST API behaves.

The last argument in the curl command above is `-u admin:password`.  This
basically adds a header called `Authorization` to the request, encodes the
string `admin:password` with [Base64](https://en.wikipedia.org/wiki/Base64),
and finally adds `Basic` along with the encoded string to the header field. The
result is the header `Authorization: Basic YWRtaW46cGFzc3dvcmQ=`. This method
of authentication is called [Basic access
authentication](http://en.wikipedia.org/wiki/Basic_access_authentication), and
must in this case be added to be able to create a new WordPress page/post.

WordPress JSON REST API's complete schema can be read on their [Github
page](https://github.com/rmccue/WP-API/blob/master/docs/schema.md), for
additional properties when creating a post etc.

Doing this from Python can be done in the following way:

    :::python
    from base64 import b64encode
    import json
    import requests


    def create_wordpress_page(title, content, publish):
        url = 'http://localhost/wp-json.php/posts'
        auth = b64encode('{}:{}'.format('admin', 'password'))
        payload = {
            'title': title,
            'type': 'page',
            'content_raw': content,
            'status': 'publish' if publish else 'draft',
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Basic {}'.format(auth),
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        response = json.loads(r.content)
        return response['link']


    create_wordpress_page('Title', 'Content', True)

Here we have used the two functions `dumps` and `loads` from the [JSON
module](http://docs.python.org/3.3/library/json.html). `dumps` is used to
encode Python data types to JSON, while `loads` is used to decode JSON.
