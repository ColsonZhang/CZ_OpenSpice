#!/usr/bin/env python

import logging
import os
import sys
import time
import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.web


class IndexHandler(tornado.web.RequestHandler):

    def get(self, path):
        path = os.path.normpath(path)
        if os.path.join(path, '').startswith(os.path.join('..', '')) or os.path.isabs(path):
            raise tornado.web.HTTPError(403)
        if not os.path.isdir(path):
            raise tornado.web.HTTPError(404)
        self.write('<html>\n<head><title>Index of /')
        escaped_title = tornado.web.escape.xhtml_escape(path if path != '.' else '')
        self.write(escaped_title)
        self.write('</title></head>\n<body>\n<h1>Index of /')
        self.write(escaped_title)
        self.write('</h1>\n<hr />\n<table>\n')
        for f in (['..'] if path != '.' else []) + sorted([i for i in os.listdir(path) if not i.startswith('.')]):
            self.write('<tr><td><a href="')
            absf = os.path.join(path, f)
            self.write(tornado.web.escape.url_escape(f).replace('+', '%20'))
            if os.path.isdir(absf):
                f += '/'
                self.write('/')
            self.write('">')
            self.write(tornado.web.escape.xhtml_escape(f))
            self.write('</a></td><td>')
            lstat_result = os.lstat(absf)
            self.write(tornado.web.escape.xhtml_escape(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lstat_result.st_mtime))))
            self.write('</td><td align="right">')
            self.write(tornado.web.escape.xhtml_escape(str(lstat_result.st_size)))
            self.write('</td></tr>\n')
        self.finish('</table>\n<hr />\n<div>Powered by <a href="https://github.com/m13253/tornado-simple-http-server" target="_blank">TornadoSimpleHTTPServer</a></div></body>\n</html>\n')


def main():
    listen_address = ''
    listen_port = 8000
    try:
        if len(sys.argv) == 2:
            listen_port = int(sys.argv[1])
        elif len(sys.argv) == 3:
            listen_address = sys.argv[1]
            listen_port = int(sys.argv[2])
        assert 0 <= listen_port <= 65535
    except (AssertionError, ValueError) as e:
        raise ValueError('port must be a number between 0 and 65535')
    tornado.log.enable_pretty_logging()
    application = tornado.web.Application(
        [
            ('/(.*/)', IndexHandler),
            ('/()', IndexHandler),
            ('/(.*)', tornado.web.StaticFileHandler, {'path': '.', 'default_filename': ''}),
        ],
        gzip=False,
        static_hash_cache=False,
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(listen_port, listen_address)
    logging.info('Listening on %s:%s' % (listen_address or '[::]' if ':' not in listen_address else '[%s]' % listen_address, listen_port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()