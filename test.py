#!/usr/bin/env python3
import configparser
import numpy as np
import time
from kaohsiung_env import KaoNetEnv

def main():
    # 讀取配置檔案
    config = configparser.ConfigParser()
    config.read('config_ma2c_nclm_kao.ini')
    env_config = config['ENV_CONFIG']
    
    # 指定 port = 650，這樣會生成 most_650.sumocfg 等檔案，
    # 並且 SUMO 連線埠將為 DEFAULT_PORT + 650 (例如 8000+650=8650)
    port = 650

    # 建立環境，output_path 必須存在或自行建立
    env = KaoNetEnv(env_config, port=port, output_path='./output/', is_record=False, record_stat=False)
    
    # 呼叫 reset() 初始化環境並取得初始狀態
    print("=== Reset Environment ===")
    initial_state = env.reset(gui=False)  # gui=True 可讓你透過 sumo-gui 觀察模擬
    # env.node_names 是一個包含所有 node ID 的列表
    for node_id, obs in zip(env.node_names, initial_state):
        print(f"{node_id}: {obs}")
    
    # 推進模擬數個步驟，並印出每個 node 的觀察值
    num_steps = 720
    print("\n=== Simulation Steps ===")
    for step in range(num_steps):
        # 為簡單起見，對每個 node 隨機選擇一個動作（動作空間長度存於 env.n_a_ls 中）
        actions = [np.random.randint(0, env.n_a_ls[i]) for i in range(env.n_agent)]
        state, reward, done, global_reward = env.step(actions)
        print(f"\nStep {step+1}: Global Reward = {global_reward}")
        for node_id, obs in zip(env.node_names, state):
            print(f"{node_id}: {obs}")
        if done:
            print("Simulation finished.")
            break
        time.sleep(0.5)  # 暫停一下以便觀察

    # 模擬結束後關閉連線
    env.terminate()

if __name__ == '__main__':
    main()
