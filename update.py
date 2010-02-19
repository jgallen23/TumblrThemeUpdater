#!/bin/usr/env python
import httplib, mimetypes, mimetools, urllib2, cookielib, urllib
from multipart import Multipart
import re
import os

class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self,req,fp,code,msg,headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

def update_theme(email, password, blog_name, file_path):

    cj = cookielib.CookieJar()
    handler = urllib2.HTTPHandler(debuglevel=0)
    opener = urllib2.build_opener(RedirectHandler(), handler, urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    login_url = "http://www.tumblr.com/login"
    login_post_data = {
        'email': email,
        'password': password
    }

    login_req = urllib2.Request(login_url, urllib.urlencode(login_post_data))
    urllib2.urlopen(login_req).read()

    dashboard_req = urllib2.Request("http://www.tumblr.com/customize/%s", blog_name)
    custom_html = urllib2.urlopen(dashboard_req).read()

    form_key = re.compile("form_key.*?value=\"(.*?)\"").findall(custom_html)[0]

    customize_url = "http://www.tumblr.com/customize/%s" % blog_name

    m = Multipart()
    m.field("edit_tumblelog[custom_theme]", open(file_path, 'r').read())
    m.field("form_key", form_key)

    ct, body = m.get()
     
    request = urllib2.Request(url=customize_url,
            headers={'Content-Type':ct, 'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12", 'Connection': 'keep-alive'},
        data=body)
    reply = urllib2.urlopen(request)
    reply.read()

def main():
    from optparse import OptionParser
    usage = "usage: %prog -u [email] -p [passwd] -b [blog name] -f [html file]"
    parser = OptionParser(usage)
    parser.add_option("-e", "--email", action = "store", type = "string", dest = "email")
    parser.add_option("-p", "--passwd", action = "store", type = "string", dest = "passwd")
    parser.add_option("-b", "--blog", action = "store", type = "string", dest = "blog")
    parser.add_option("-f", "--file", action = "store", type = "string", dest = "file_path")

    (options, args) = parser.parse_args()
    if options.email and options.passwd and options.blog and options.file_path:
        if os.path.exists(options.file_path):
            update_theme(options.email, options.passwd, options.blog, options.file_path)
            print "done"
        else:
            print "File doesn't exist"
    else:
        parser.print_help()


if __name__ == "__main__": main()
