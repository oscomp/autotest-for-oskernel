scene_output = """
File /var/tmp/XXX write bandwidth:32273 KB/sec
START bw_file_rd_io_only
0.524288 391.84
END bw_file_rd io_only 0
START bw_file_rd_open2close
balabala
0.524288 341.34
END bw_file_rd open2close 0
START lat_ctx

"size=32k ovr=50.11
2 90.00
4 103.40

32 166.99
END lat_ctx 0
START lat_proc_fork
Process fork+exit: 2592.3333 microseconds
END lat_proc_fork 0
START lat_proc_exec
Process fork+execve: 5612.9000 microseconds
END lat_proc_exec 0
START bw_pipe
Pipe bandwidth: 93.87 MB/sec
END bw_pipe 0
START lat_pipe
Pipe latency: 251.9858 microseconds
END lat_pipe 0
START lat_pagefault
Pagefaults on /var/tmp/XXX: 8.5504 microseconds
END lat_pagefault 1
START lat_mmap
0.524288 231
END lat_mmap 0
    """
