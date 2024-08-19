環境建立步驟

1.從openstreet map 抓下map.osm

2.使用sumo套件轉乘net.xml

3.使用python randomTrips.py -n demo.net.xml -r routes.rou.xml -e 50 -p 0.1 -l建立rou檔案

4.將net裡面的tllogit部分抓出來，建立spain.add.xml

5.將add.xml中的programID 從0替換成tls

6.使用與hamasin一樣的sumocfg設定