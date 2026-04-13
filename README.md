# 應用生成式 AI 結合 6E 教學模式與自我決定理論對高中生 STEM 學習之影響研究

本儲存庫包含專為碩士論文設計的實驗數據生成模型、統計分析腳本及預期結果可視化工具。本研究旨在探討生成式 AI 介入教學對高中生在 **STEM 學習動機**與**認知負荷**之影響。

---

## 📝 專案概述 (Project Overview)

本研究採用準實驗設計（Quasi-experimental Design），探討生成式 AI 在高中生活科技課程中的應用成效。研究整合以下理論框架：
* **教學模式**：6E 教學法 (Engage, Explore, Explain, Engineer, Enrich, Evaluate)。
* **心理理論**：自我決定理論 (Self-Determination Theory, SDT)。
* **核心工具**：引導式策略型教學AI代理人作為學習鷹架，協助學生進行實作與問題解決。

本專案模擬了 **$N=106$** 名受試者的實驗數據，分為實驗組（Experimental Group, $n=53$）與控制組（Control Group, $n=53$）。

---

## 📊 研究工具與維度 (Instruments)

研究採用兩套標準化量表進行前後測評量：

| 量表名稱 | 題數 | 維度內容 | 計分方式 |
| :--- | :--- | :--- | :--- |
| **學習動機量表** | 34 | 內在動機、勝任感、自主感、關係感 | Likert 5 點 |
| **認知負荷量表** | 10 | 內在負荷 (IL)、外在負荷 (EL)、增生負荷 (GL) | 0-10 分 |

---

## 🚀 技術架構 (Technical Stack)

* **數據生成**：利用 `NumPy` 模擬具備學術統計邏輯的受試者填答數據。
* **統計分析**：使用 `statsmodels` 執行 **線性混合模型 (MixedLM)** 與 **共變數分析 (ANCOVA)**。
* **可視化**：透過 `Plotly` 產出交互式趨勢折線圖，展現前後測之交互作用。
* **論文整合**：自動生成符合學術規範（booktabs）的 LaTeX 統計表格代碼。

---

## 📦 檔案結構 (Repository Structure)

* `generate_fake_data.py`: 模擬受試者原始填答行為，產出具備題項級數據的 CSV 檔。
* `analysis.py`: 核心分析程式，執行統計檢定並產出圖表與 LaTeX 代碼。
* `data_wide.csv`: 寬格式數據，包含 34 題動機與 10 題負荷之原始整數得分。
* `plots/`: 自動存放各研究變項的前後測交互作用趨勢圖。
* `descriptive_stats.tex`: 自動生成的描述性統計與 ANCOVA 結果表格。

---

## ⚙️ 使用說明 (Usage)

### 1. 環境設置
建議使用 Python 3.8+ 版本，並安裝相關依賴套件：
```bash
pip install pandas numpy plotly statsmodels kaleido openpyxl
```

### 2. 執行流程
請依照以下順序執行腳本，以確保數據生成與分析邏輯的一致性：

```bash
# 步驟 A: 生成原始填答數據 (包含 34 題動機量表與 10 題認知負荷量表)
python generate_fake_data.py

# 步驟 B: 執行統計分析、產出交互作用圖並生成 LaTeX 表格代碼
python analysis.py
```

---

## 📜 預期結果 (Expected Findings)

根據目前的模擬數據與初步分析結果，本研究預期之實驗成效如下：

* **動機賦能 (Motivation Enhancement)**：實驗組高中生在接受「生成式 AI 結合 6E 教學法」後，其學習動機後測得分預期將顯著優於對照組 ($p < .001$)。
* **負荷優化 (Cognitive Load Optimization)**：生成式 AI 預期能作為有效的學習鷹架，顯著降低學生在複雜任務中的「外在認知負荷」(EL)，同時提升有助於基模建構的「增生認知負荷」(GL)。
* **心理需求滿足 (Psychological Needs)**：透過 AI 的及時反饋，學生在自我決定理論 (SDT) 中的「勝任感」與「自主感」維度預期將展現出較高的成長趨勢。
* **教學效能轉化**：相較於傳統教學，結合 AI 的 6E 教學模式更能觸發學生的探究動機，並在實作環節（Engineer & Enrich）展現更高的學習投入度。
```
