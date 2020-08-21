# slowloris.py - Simple slowloris in Python

## What is Slowloris?
Slowloris is basically an HTTP Denial of Service attack that affects threaded servers. It works like this:

1. We start making lots of HTTP requests.
2. We send headers periodically (every ~15 seconds) to keep the connections open.
3. We never close the connection unless the server does so. If the server closes a connection, we create a new one keep doing the same thing.

This exhausts the servers thread pool and the server can't reply to other people.

## How to install and run?

* `git clone https://github.com/gkbrk/slowloris.git`
* `cd slowloris`
* `python3 slowloris.py example.com`

## 参数列表：
```
usage: slowloris.py [-h] [-p PORT] [-m METHOD] [-uri URI] [-pl PAYLOAD] [-s SOCKETS] [-v] [-ua] [-x]
                    [--proxy-host PROXY_HOST] [--proxy-port PROXY_PORT] [--https] [--sleeptime SLEEPTIME]
                    [host]

Slowloris, low bandwidth stress test tool for websites

positional arguments:
  host                  Host to perform stress test on // 主机ip地址

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port of webserver, usually 80 // 主机端口，默认80
  -m METHOD, --method METHOD // 请求方法，默认GET
                        HTTP method
  -uri URI, --uri URI   HTTP uri // 请求路径，默认跟路径/
  -pl PAYLOAD, --payload PAYLOAD // 请求体，默认随机数
                        HTTP payload
  -s SOCKETS, --sockets SOCKETS // 线程数，默认150，建议10000+
                        Number of sockets to use in the test
  -v, --verbose         Increases logging // 开启日志debug
  -ua, --randuseragents // 开启随机user-agents
                        Randomizes user-agents with each request
  -x, --useproxy        Use a SOCKS5 proxy for connecting // 是否启用代理
  --proxy-host PROXY_HOST
                        SOCKS5 proxy host
  --proxy-port PROXY_PORT
                        SOCKS5 proxy port
  --https               Use HTTPS for the requests
  --sleeptime SLEEPTIME
                        Time to sleep between each header sent.
```

## 例如
* `python slowloris.py example.com -p 8080 -m POST -uri /test -s 10000 -ua -v`


### SOCKS5 proxy support

However, if you plan on using the `-x` option in order to use a SOCKS5 proxy for connecting instead of a direct connection over your IP address, you will need to install the `PySocks` library (or any other implementation of the `socks` library) as well. [`PySocks`](https://github.com/Anorov/PySocks) is a fork from [`SocksiPy`](http://socksipy.sourceforge.net/) by GitHub user @Anorov and can easily be installed by adding `PySocks` to the `pip` command above or running it again like so:

* `sudo pip3 install PySocks`

You can then use the `-x` option to activate SOCKS5 support and the `--proxy-host` and `--proxy-port` option to specify the SOCKS5 proxy host and its port, if they are different from the standard `127.0.0.1:8080`.

## Configuration options
It is possible to modify the behaviour of slowloris with command-line arguments.

## License
The code is licensed under the MIT License.
