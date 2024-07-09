# Traffic

## gwgo.py-1st 2024/7/10
line 5~14: 定義Solution類別, 包含position和value
    position即包含每個phase的duration
    value是objective value, 以現在這程式是愈低愈好。以update_objective_value方法更新此評分 (如line 68和line 100), 未來套用SUMO模型結果計算分數

line 16~29: 計算Social-Interaction(GO)的過程函式

line 31~41: Hunting()
line 43~55: Social-Interaction()
line 57~58: Hunting-Interaction()

! 重要 !
line 60~109: GWGO()
    line 63: 創建N個Solution物件
    line 68: 更新各Solution的objective value
    line 69~72: 抓出最好的三個Solution要丟進Hunting()

    line 91: Hunting()回傳p
    line 94: Social-Interaction()回傳xi
    line 96: Hunting-Interaction()將p和xi相加, 並設為此solultion的position

    line 99~104: 重複上面line 68~72

line 113~123: 各參數的設置

line 127~128: 固定random seed方便測試結果, 可註解掉看其他隨機結果

line 130: 固定numpy輸出為5位小數, 並不以科學記號表示(1.23e-05)

line 131~155: 輸出結果
    line 146: 使用GWGO()函式
