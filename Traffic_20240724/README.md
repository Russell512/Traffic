總共有四個.py檔:
1. main.py
2. encoding.py: 將solution的position encode到.net.xml檔的duration，以及將.net.xml檔名寫入.sumocfg檔中
3. sumo_traci.py: 自動將.sumocfg檔導入至sumo-gui中，並輸出tripinfo.xml及fcd.xml
4. eq.py: 讀入模擬結果計算objective value

main.py:<br/>
line 65: 隨機生成N個solution<br/>
line 70: 將所有數字轉換為整數<br/>
line 71: encode_net_xml() 以solution生成.net.xml檔, 例: s0 = [35, 25, 40, 30], 生成"1.net.xml"<br/>
line 72: 再用上行生成的.net.xml生成.sumocfg<br/>
line 73: simulationStart(寫在sumo_traci.py)開啟sumo-gui並開始模擬<br/>
line 74: 計算此solution的value<br/>
<br/><br/>

問題在經過86行開始的Update部分，部分solution可能會包含負數，手動改檔案測試，結果是如果有一些負數可能還跑得動，全部或一堆都改成負數sumo就會報錯了