#!/usr/bin/env python2

import sys
from src.app import app

if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    app.run(debug=True, host=host)
