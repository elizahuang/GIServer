## GIServer

* 接splunk hostname, 拿timestamp時間, 查機器類型, 廠商的mail, serial_number(index=bare_metal) (mapping查機器類型)
    * 連兩個client（一個是1-1的splunk server, 一個是admin的client）
    * 傳給client拿log(string存成檔案) """mailx script linux #popen""" (包成function)
    * 寄mail給廠商

* 24 threads python

## 啟動server方式
* `python app.py [port]` eg. `python app.py 8080`
