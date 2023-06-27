#!/usr/bin/python
import rrdtool
ret = rrdtool.create("example.rrd", "--step", "1800", "--start", '0',
 "DS:metric1:GAUGE:2000:U:U",
 "DS:metric2:GAUGE:2000:U:U",
 "RRA:AVERAGE:0.5:1:600",
 "RRA:AVERAGE:0.5:6:700",
 "RRA:AVERAGE:0.5:24:775",
 "RRA:AVERAGE:0.5:288:797",
 "RRA:MAX:0.5:1:600",
 "RRA:MAX:0.5:6:700",
 "RRA:MAX:0.5:24:775",
 "RRA:MAX:0.5:444:797")