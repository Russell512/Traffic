2024.8.14

1. configuratoin.py增加以.add.xml計算phase
2. evaluate.py中Cr()添加遇到ZeroDivisor的應對(if 全紅燈 ratio = 0, else ratio = 1)
3. 紀錄訓練過程中的objective value並以pyplot繪製, 並以plt.savefig()自動另存圖片

問題:
1. 路網擁有多個多餘的單向、僅一燈號的tlLogic
2. 某些路口與現實不符
3. 目前主幹道的車流無法疏通 -> 引入更優化的rou.xml產生器而非randomTrips.py?

展望:
1. sumocfg以程式生成, 否則假如欲變更.rou.xml檔, 需手動修改.sumocfg及configuration.py
2. 以文字檔輸出優化結果(時間, 分數)